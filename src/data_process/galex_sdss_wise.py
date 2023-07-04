from astroquery.sdss import SDSS
from astroquery.skyview import SkyView
from astropy import coordinates as coords

# Step 1: Select a galaxy from the SDSS database and retrieve its images and spectrum
ra = 123.456  # Replace with the right ascension (RA) of your target galaxy
dec = 45.678  # Replace with the declination (Dec) of your target galaxy
radius = '5 arcsec'
# pos = coords.SkyCoord(f'{ra} {dec}', unit='deg')  # Create a SkyCoord object for the target galaxy
pos = coords.SkyCoord('0h8m05.63s +14d50m23.3s', frame='icrs')

# Query SDSS for images
sdss_images = SDSS.query_region(pos, radius=radius, spectro=False)
# Query SDSS for spectrum
sdss_spectrum = SDSS.query_region(pos,radius=radius, spectro=True)

# Step 2: Find corresponding images in WISE and GALEX and download the data
# Retrieve WISE images
# wise_images = SkyView.get_images(position=f'{ra} {dec}', survey=['WISE'], pixels=512)
# # Retrieve GALEX images
# galex_images = SkyView.get_images(position=f'{ra} {dec}', survey=['GALEX'], pixels=512)

# Step 3: Put all the downloaded data into the same folder
output_folder = '/mnt/home/wwong/ceph/AstroProject/ThereIsASky/custom'  # Replace with the desired output folder

# # Save SDSS images and spectrum to the output folder
SDSS.save_images(output_folder, sdss_images)
SDSS.save_spectra(output_folder, sdss_spectrum)

# # Save WISE and GALEX images to the output folder
# for idx, image in enumerate(wise_images):
#     image_name = f'WISE_image_{idx}.fits'  # Modify the naming convention if desired
#     image.writeto(f'{output_folder}/{image_name}')

# for idx, image in enumerate(galex_images):
#     image_name = f'GALEX_image_{idx}.fits'  # Modify the naming convention if desired
#     image.writeto(f'{output_folder}/{image_name}')
