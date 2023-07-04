from astroquery.sdss import SDSS
from astroquery.ipac.irsa import Irsa
from astroquery.mast import Observations

from astroquery.skyview import SkyView
from astropy import coordinates as coords

# Step 1: Select a galaxy from the SDSS database and retrieve its images and spectrum
ra = 123.456  # Replace with the right ascension (RA) of your target galaxy
dec = 45.678  # Replace with the declination (Dec) of your target galaxy
radius = '5 arcsec'
# pos = coords.SkyCoord(f'{ra} {dec}', unit='deg')  # Create a SkyCoord object for the target galaxy
pos = coords.SkyCoord('0h8m05.63s +14d50m23.3s', frame='icrs')

channels = ['SDSSg',
            'SDSSi',
            'SDSSr',
            'SDSSu',
            'SDSSz',
            'WISE 3.4',
            'WISE 4.6',
            'WISE 12',
            'WISE 22',
            'GALEX Near UV',
            'GALEX Far UV']

# Step 2: Find corresponding images in WISE and GALEX and download the data
# Retrieve WISE images
images = SkyView.get_images(position=pos, survey=channels, pixels=512)

# Step 3: Put all the downloaded data into the same folder
output_folder = '/mnt/home/wwong/ceph/AstroProject/ThereIsASky/custom'  # Replace with the desired output folder

