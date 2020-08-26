#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 13:14:55 2020

@author: patrickmayerhofer

These functions are specifically for BPK 409 - Wearable Technology and Human Physiology
"""

import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt



""" This function makes an FFT and returns the power spectrum of data
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

def get_bursts(x):
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
