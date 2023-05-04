# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 14:40:27 2023

@author: Juliana Karp
"""

def sliders(model, exposure_time, sky_value, read_noise):
    
    '''
    Function to add CCD noise to base model image based on noise type and level.
    
    Parameters
    ----------
    model: 2d float array
        data to be used as base model upon which to add noise.
    exposure_time: float
        telescope exposure time in seconds.
    sky_value: float
        average brightness of background sky to be added on to model data.
    read_noise: float
        value of noise created by CCD readout process.
        
    Returns
    -------
    with_noise: 2d float array
        model with noise added from each input source.
    '''
    
    import numpy as np
    
    model_size = np.shape(model)
    
    #sample background sky values from a gaussian centered at the value 
    #chosen by the user
    sky_arr = np.random.normal(loc=sky_value, scale=5, size=model_size)
    
    #sample flux from a gaussian
    flux_arr = model + np.random.normal(loc=0, scale=0.5, size=model_size)
    
    #add the sky values to the model data
    with_sky = flux_arr + sky_arr
    
    #convert all negative values to 0 so that the sqrt function can handle them
    neg = with_sky < 0
    with_sky[neg] = 0
    
    #add poisson noise and read noise to the model+sky
    poisson_noise = np.sqrt(with_sky*exposure_time + read_noise**2)
    
    with_noise = flux_arr * exposure_time + poisson_noise
    
    #convert all negative values to 0
    #because a pixel can't have negative electrons
    neg = with_noise < 0
    with_noise[neg] = 0
    
    return with_noise