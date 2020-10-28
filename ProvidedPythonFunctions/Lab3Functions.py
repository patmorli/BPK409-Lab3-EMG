#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 13:14:55 2020

@author: patrickmayerhofer

This library was created for the use in the open source Wearables Course BPK409, Lab3 - EMG
For more information: 
    https://docs.google.com/document/d/e/2PACX-1vTr1zOyrUedA1yx76olfDe5jn88miCNb3EJcC3INmy8nDmbJ8N5Y0B30EBoOunsWbA2DGOVWpgJzIs9/pub
"""

import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
import pandas as pd



""" This function does an FFT and returns the power spectrum of data
    Input: Data, sampling frequency
    Output: Power, the respective frequencies of the power spectrum
   """
def get_power(data, sfreq):
    sig_fft = fftpack.fft(data)
    
    # And the power (sig_fft is of complex dtype)
    power = np.abs(sig_fft)
    
    # The corresponding frequencies
    sample_freq1 = fftpack.fftfreq(data.size, d=1/sfreq)
    frequencies = sample_freq1[sample_freq1 > 0]
    power = power[sample_freq1 > 0]
    return power, frequencies


""" This function makes you choose beginning and end of a muscle activation with a plot by clicking.
    It is specifically made for the three BPK409 datasets (weights, mvc, fatigue)
    Input: mvc_emg_filtered, weights_emg_filtered, fatigue_emg_filtered
    Output: the 3 starts of the 3 mvc bursts, 3 ends of mvc burts, and same for weights fatigue
    mvc_start, mvc_end, weights_start, weights_end, fatigue_start, fatigue_end
   """
def get_bursts(mvc_emg_filtered, weights_emg_filtered, fatigue_emg_filtered):   
    def get_individual_burst(x):
        def tellme(s):
            print(s)
            plt.title(s, fontsize=16)
            plt.draw()
            
        plt.clf()
        plt.setp(plt.gca(), autoscale_on=True)
        plt.plot(x)
       
        tellme('Click once to start zoom')
        plt.waitforbuttonpress()
        
        while True:
            tellme('Select two corners of zoom, enter/return key to finish')
            pts = plt.ginput(2, timeout=-1)
            if len(pts) < 2:
                break
            (x0, y0), (x1, y1) = pts
            xmin, xmax = sorted([x0, x1])
            ymin, ymax = sorted([y0, y1])
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
          
            
        tellme('Choose start of activity')    
        s = plt.ginput(1)
        tellme('Choose end of activity')   
        e = plt.ginput(1)
        s1 = s[0]
        e1 = e[0]
        start = int(s1[0].astype(int))
        end = int(e1[0].astype(int))
        plt.show()
        
        return start,end
    number_bursts = 3
    mvc_start = np.empty(number_bursts)
    mvc_end = np.empty(number_bursts)
    weights_start = np.empty(number_bursts)
    weights_end = np.empty(number_bursts)
    fatigue_start = np.empty(number_bursts)
    fatigue_end = np.empty(number_bursts)
    for i in range(number_bursts):
        mvc_start[i], mvc_end[i] = get_individual_burst(mvc_emg_filtered)
    for i in range(number_bursts): 
        weights_start[i], weights_end[i] = get_individual_burst(weights_emg_filtered)
    for i in range(number_bursts): 
        fatigue_start[i], fatigue_end[i] = get_individual_burst(fatigue_emg_filtered)  
       
    mvc_start = mvc_start.astype(int)
    mvc_end = mvc_end.astype(int)
    weights_start = weights_start.astype(int)
    weights_end = weights_end.astype(int)
    fatigue_start = fatigue_start.astype(int)
    fatigue_end = fatigue_end.astype(int)
    
    return mvc_start, mvc_end, weights_start, weights_end, fatigue_start, fatigue_end

""" This function imports three files of the MVC experiment, three files of the weights experiment,
    and three files of the fatigue experiment. It creates one variable for each (MVV, weights, fatigue)
    and normalizes the time axis. The variables need to be in the working directory as
    Weight1, Weight2, Weight3, MVC1, MVC2, MVC3, Fatigue1, Fatigue2, Fatigue3
    Input: 
    Output: weights, mvc, fatigue
   """
   
def import_data(separator):
    """ This function is when you put together several datasets,
    but each dataset always starts with a time of 0.
    Input: dataframe that also has a column 't'
    Output: continuous time over all datasets
   """
    def time_norm(data):
        a = list(data.iloc[:]['t'])
        b = list(data.iloc[:]['t'])
        
        for u in range(len(a)-1):
            if a[u]>a[u+1]:
                if b[u]>b[u+1]:
                    offset = a[u]-a[u+1]+1
                    a[u+1] = offset + a[u+1]
                    u += 1
                else:
                    a[u+1] = offset + a[u+1]
                    u += 1
                      
        output = pd.DataFrame({'emg': data.emg, 't': a})
        output.reset_index(inplace = True, drop = True)
        return output
    
    """import data and put weights in one variable and mvc in one variable"""
    column_names = [
      'emg',
      't',  
    ]
    # Creating an empty Dataframe with column names only
    weights_raw = pd.DataFrame(columns=column_names)
    mvc_raw = pd.DataFrame(columns=column_names)
    fatigue_raw = pd.DataFrame(columns=column_names)
    
    # read all mvc, weight, and fatigue files 
    for i in range(3):
        # create string for path
        weights_string = 'Weight' + str(i+1) + '.txt'
        mvc_string = 'MVC' + str(i+1) + '.txt'
        fatigue_string = 'Fatigue' + str(i+1) + '.txt'
        
        weights_raw = weights_raw.append(pd.read_csv(
            weights_string,
             sep=separator, names=column_names, skiprows= 50,
             skipfooter = 50
            ))
        mvc_raw = mvc_raw.append(pd.read_csv(
            mvc_string,
             sep=separator, names=column_names, skiprows= 50, 
             skipfooter = 50
            ))
        fatigue_raw = fatigue_raw.append(pd.read_csv(
            fatigue_string,
             sep=separator, names=column_names, skiprows= 50, 
             skipfooter = 50
            ))
    # timing needs changing as, the appended data starts from 0 again
    weights = time_norm(weights_raw)
    mvc = time_norm(mvc_raw)
    fatigue = time_norm(fatigue_raw)
    return weights, mvc, fatigue