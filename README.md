# asternoise

### ```asternoise``` is a teaching tool designed for Yale University's ASTR 255: Introduction to Astronomical Research course.

It explains the ways in which different factors influence the noise levels in an astronomical image captured by a charged-couple device (CCD), and allows the user to visualize these effects on three different base models. The models are: 1) a random noise model, 2) a three-layer composite image of NGC 3132 captured by the James Webb Space Telescope (JWST)'s Near Infrared Camera (NIRCam), and 3) a three-layer composite image of NGC 1433 captured by JWST's Mid-Infrared Instrument (MIRI). The data was retrieved from the Barbara A. Mikulski Archive for Space Telescopes (MAST) at the following link: https://mast.stsci.edu/portal/Mashup/Clients/Mast/Portal.html.

### Setup Requirements
The ```asternoise``` package is written in ```Python```. It requires the installation of the following ```Python``` packages: ```numpy```, ```astropy```, ```streamlit```, and ```matplotlib```.

### To Use
To launch the app, the code must be downloaded in an environment which contains the packages required above. Then, in a command terminal, navigate to the ```asternoise``` folder and type the command "```streamlit run app.py```". This will launch the app in a browser window.