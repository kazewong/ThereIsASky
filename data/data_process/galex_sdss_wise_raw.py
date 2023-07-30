from astroquery.sdss import SDSS
from astroquery.ipac.irsa import Irsa
from astroquery.ipac.irsa.ibe import Ibe
from astroquery.mast import Observations

from astropy import units as u
from astropy.coordinates import SkyCoord

output_folder = '/mnt/home/wwong/ceph/AstroProject/ThereIsASky/custom/'  # Replace with the desired output folder
tag = 'galex_sdss_wise_raw'

sql = "select top 10 z, ra, dec, bestObjID from specObj where class = 'galaxy' and z < 0.3 and zWarning = 0"

# Step 1: Select a galaxy from the SDSS database and retrieve its images and spectrum
res = SDSS.query_sql(sql)

ra = res['ra']
dec = res['dec']

c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')

# sdss_images = SDSS.get_images(coordinates=c)
galex_data = Observations.query_criteria(coordinates=c, radius="0.02 deg", obs_collection="Galex")
wise_data = Irsa.query_region(c[0], catalog="allwise_p3as_psd", spatial="Cone", radius=0.02 * u.deg)
wise_images = Ibe.query_region(coordinate=c[0], mission="wise", dataset="wise.wise_allwise_p3am_cdd")
