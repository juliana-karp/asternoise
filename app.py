# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 10:50:08 2023

@author: Juliana Karp
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

apptitle = 'asternoise'

st.set_page_config(page_title=apptitle, page_icon="🌌")

#app title & welcome
st.markdown('# Welcome to :violet[asternoise], a CCD noise visualization and teaching tool!')

#explain what a CCD is
st.markdown('## What is a :violet[charged-couple device] (CCD)?')
st.image('ccd_image.jpg', caption='Image source: https://www.borntoengineer.com')
st.markdown('CCDs are the most common imaging instrument today. They are used \
            in phone cameras, digital cameras, and modern telescopes.')
st.markdown('A CCD is an electronic device which uses semiconductors to \
            detect incident photons above a certain energy threshhold. \
            The semiconductors begin in a de-excited ground state,\
            meaning that the electrons in their outer shell are \
            bound to the atom in the valence band. When an \
            incident photon hits the semiconductor, \
            its energy is absorbed, which causes an electron \
            in the valence band to jump energy levels up to the\
            conduction band. Over time, as many photons hit the\
            semiconductor, these negative charges accumulate and \
            create a global negative electric charge in the material\
            whose magnitude is proportional to the number of incident\
            absorbed photons.')
st.markdown('In order to record an image, the CCD is divided into many\
            tiny square wells, each with their own semiconductor. \
            These wells become the pixels on a digital image. Within \
            each individual well, the charge buildup is summed, so in \
            order to obtain higher resolution data, the same total CCD \
            surface area must be divided into a greater number of wells. \
            Finally, using an analog-to-digital converter (ADC), the \
            charge buildups in each well are read out, recorded \
            digitally, and stored in data formats we are familiar with.')

#explain different types of noise
st.markdown('## What :violet[noise sources] exist?')
st.markdown('### Background Sky Noise')
st.markdown('The background behind objects of interest is never zero. \
            It is also more complicated than just one singular value which \
            can be subtracted from the dataset. It can be visualized as a \
            gaussian profile of random values distributed about a mean, \
            which the user can choose below. In each pixel, a random \
            value from the gaussian will be chosen as the background \
            sky value.')
back_sky = st.slider('Mean Background Sky Value', 0.0, 20.0, 0.0)

#write a function to create a gaussian
def gaussian(x, peak, std):
    
    '''
    Function to create gaussian distribution.
    
    Parameters
    ----------
    x: 1d float array
        values along the x-axis to create gaussian function against.
    peak: float
        x-value of gaussian peak.
    std: float
        standard deviation of gaussian peak.
    
    Returns
    -------
    gauss: 1d float array
        gaussian function of x centered at peak with standard deviation std.
    '''
    
    gauss = np.exp(-1.*(x-peak)**2/(2*std**2))
    
    return gauss

#display gaussian based on user's choice of mean sky value (peak)
x_vals = np.arange(0,20,0.1)
gauss = gaussian(x_vals, back_sky, 2)
fig, ax = plt.subplots()
ax.plot(x_vals, gauss)
ax.set_title('Probabilistic Distribution of Background Sky Values')
ax.set_xlabel('Background Sky Value')
ax.set_ylabel('Likelihood')
st.pyplot(fig)

st.markdown('### Read Noise')
st.markdown('At the end of each exposure, the excess charge which \
            has been accumulated in each pixel well must be read \
            out before it can be converted to a digital format by \
            the analog-to-digital converter (ADC). This process occurs \
            pixel by pixel, and therefore takes some time. The ADC is \
            an electrical component which produces its own heat, \
            meaning that it can add noise to the data that it is \
            recording. This noise is called read noise, and is present \
            in every image recorded by CCDs.')

#add formula for noise addition
st.markdown('## How do different types of noise :violet[add] with each other?')
st.markdown('Let S be the signal, while N is the total noise. If \
            B is the noise from the sky background and R is the \
            read noise, then the total signal to noise can be \
            written as:')
st.markdown('### $S \div N = S \div \sqrt{S + B + R^2}$')
st.markdown('The signal and sky background values are a function \
            of the exposure time, but the read noise is an instrinsic \
            value of the CCD and does not depend on exposure time.')

#define signal-dominated, noise-dominated regions
st.markdown('* When $S/N$ scales with $S / \sqrt{S}$, we say the \
            data is :violet[signal-limited]. The signal-to-noise \
            ratio increases with more light collection power, \
            meaning increased exposure time and larger aperture \
            telescopes can increase this ratio.')
st.markdown('* When $S/N$ scales with $S / \sqrt{B}$, we say the \
            data is :violet[background-limited]. If the data is \
            background-limited, it is often in the case of faint \
            targets. Imaging during darker phases of the moon can help \
            decrease noise in this scenario.')
st.markdown('* When $S/N$ scales with $S / R$, we say the data is \
            :violet[detector-limited]. If the data is read-noise \
            dominated, it is beneficial to take data over longer \
            exposure times or obtain a more read-noise efficient CCD.')
   
#create sidebar for noise level controls
st.markdown('## Noise Addition :violet[Visualization]')
st.markdown('How do these different types of noise impact an image?')
st.markdown("### Noise Parameter Control Panel")
st.markdown('Please use the menu below to select which base model you \
            want to use and to adjust the levels of different noise \
            sources. The visualization will appear below.')

#select which model you want to use
select_model = st.selectbox('Which base model would you like to use?',
                                    ['Random noise', 'NGC 3132',
                                     'NGC 1433'])

#display whichever base model the user has selected
if select_model == 'Random noise':
    #create a random model of noise of size 250,250
    #and values spanning from 0 to 100
    img = np.random.rand(250,250)
    img = img*100
    
    #plot particularities
    title = 'Random Noise Base Model'
    cmap = 'hot'
    
if select_model == 'NGC 3132':
    #import the data, it will be of size 2500,2500
    
    filter1 = 'https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:JWST/product/jw02733-o001_t001_nircam_clear-f356w_i2d.fits'
    filter2 = 'https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:JWST/product/jw02733-o001_t001_nircam_f405n-f444w_i2d.fits'
    filter3 = 'https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:JWST/product/jw02733-o001_t001_nircam_f444w-f470n_i2d.fits'
    
    filters = [filter1, filter2, filter3]
    
    #define parameters for the visualization
    a_min = np.array([0,0,0])
    a_max = np.array([50,50,20])
    func = 'sqrt'
    
    #plot particularities
    title = 'NGC 3132 JWST NIRCam'
    cmap = 'afmhot'
    
if select_model == 'NGC 1433':
    #import the data, it will be of size 2500,2500
    
    filter1 = 'https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:JWST/product/jw02107-o005_t005_miri_f770w_i2d.fits'
    filter2 = 'https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:JWST/product/jw02107-o005_t005_miri_f1000w_i2d.fits'
    filter3 = 'https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:JWST/product/jw02107-o005_t005_miri_f1130w_i2d.fits'
    
    filters = [filter1, filter2, filter3]
    
    #define parameters for the visualization
    a_min = np.array([10,10,0])
    a_max = np.array([500,1000,100])
    func = 'sqrt'
    
    #plot particularities
    title = 'NGC 1433 JWST MIRI'
    cmap = 'hot'

#create sliders for each type of noise
sky_value = st.slider('Mean Sky Value (electrons/pixel)', 0.0, 20.0, 0.0)
read_noise = st.slider('CCD Read Noise (electrons/pixel)', 0.0, 50.0, 0.0)
exposure_time = st.slider('Exposure Time (seconds)', 1.0, 200.0, 100.0)

#compile the image
if select_model != 'Random noise':
    from visualize_data import visualize
    img = visualize(filters, a_min=a_min, a_max=a_max, func=func)

#add all the slider noise values using the add_noise function    
from add_noise import sliders
with_noise = sliders(img, exposure_time, sky_value, read_noise)

#visualize it
fig, ax = plt.subplots()
ax.imshow(with_noise, aspect='equal', vmin=0, vmax=10, origin='lower')
cbar = fig.colorbar((ax.pcolormesh(with_noise, cmap=cmap)), ax=ax,
                    fraction=0.1, aspect=30)
cbar.ax.tick_params(labelsize=8)
ax.set_title(title, fontsize=15)
ax.tick_params(axis='both', labelsize=8)
st.pyplot(fig)

st.markdown('The data used as models above was recorded by \
            NASA\'s James Webb Space Telescope\'s Mid-Infrared \
            Instrument (MIRI) and Near Infrared Camera (NIRCam). \
            It was retrieved from the Barbara A. Mikulski Archive \
            for Space Telescopes (MAST) at the following link: \
            https://mast.stsci.edu/portal/Mashup/Clients/Mast/Portal.html.')
st.markdown('The app was coded by Juliana Karp.')