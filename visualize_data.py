# data downloaded from MAST: https://archive.stsci.edu/

"""
Created on Wed Apr 12 11:43:34 2023

@author: Juliana Karp
"""

def rescale_img(array, func='sqrt', a_min=None, a_max=None):
    
    '''
    Function to rescale data according to a given
    function and minimum and maximum values.
    
    Parameters
    ----------
    filters: array of 3 strings
        paths to individual files of raw data from
        3 different filters, in order: blue, green, red.
    func: str
        scaling of final image, options: sqrt, asinh, log10, loge.
        default = sqrt.
    a_min: float
        minimum value to scale to in this filter. default = None.
    a_max: float
        maximum value to scale to in this filter. default = None.
        
    Returns
    -------
    with_noise: 2d float array
        model with noise added from each input source.	
    '''
	
    import numpy as np
	
    #cut out all values beyond the minimum and maximum we want
    if a_min == None:
        a_min = array.min()
    if a_max == None:
        a_max = array.max()
    
    array = np.clip(array, a_min, a_max)
    array = array - a_min
    array[np.where(array < 0)] = 0
    
    #rescale based on the given function
    if func == 'sqrt':
        array = np.sqrt(array)
    if func == 'asinh':
        array = np.arcsinh(array)
    if func == 'log10':
        array = np.log10(array)
    if func == 'loge':
        array = np.log(array)
    
    return array

import numpy as np

def visualize(filters, func='sqrt', a_min=np.zeros(3),
                      a_max=np.ones(3)):
    
    '''
    Function to compile 2D array of data to be used as base model
    from 3 input layers of data taken from 3 different wavelength filters.
    
    Parameters
    ----------
    filters: array of 3 strings
        paths to individual files of raw data from
        3 different filters, in order: blue, green, red.
    func: str
        scaling of final image, options: sqrt, asinh, log10, loge.
        default = sqrt.
    a_min: array of 3 floats
        minimum value to scale to in each filter. default = [0,0,0].
    a_max: array of 3 floats
        maximum value to scale to in each filter. default = [0,0,0].
        
    Returns
    -------
    img_mean: 2d float array
        combined and rescaled image based on 3 input filters and parameters.	
    '''

    from astropy.io import fits 
    import numpy as np

    #define which filter will be red, green, and blue respectively
    b_img = fits.getdata(filters[0])
    g_img = fits.getdata(filters[1])
    r_img = fits.getdata(filters[2])
    
    #adjust size of data so that each filter has the same shape
    shapes = np.array([b_img.shape, g_img.shape, r_img.shape])
    shape_to = np.min(shapes, axis=0)
    s_x = shape_to[0]
    s_y = shape_to[1]
    b_img = b_img[:s_x,:s_y]
    g_img = g_img[:s_x,:s_y]
    r_img = r_img[:s_x,:s_y]
    
    #overlay them by color
    img = np.zeros((g_img.shape[0], g_img.shape[1], 3), dtype=float)
    img[:,:,0] = rescale_img(r_img, a_min=a_min[0], a_max=a_max[0], func=func)
    img[:,:,1] = rescale_img(g_img, a_min=a_min[1], a_max=a_max[1], func=func)
    img[:,:,2] = rescale_img(b_img, a_min=a_min[2], a_max=a_max[2], func=func)
    
    #take the mean along the third axis to get a 2 dimensional image
    img_mean = np.mean(img, axis=2) 
    
    #zoom in on galaxy in ngc 1433 data
    if img_mean.shape == (2094, 1784):
        img_mean = img_mean[900:1200,900:1225]
    
    return img_mean