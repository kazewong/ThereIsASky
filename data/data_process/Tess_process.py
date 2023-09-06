import astropy.io.fits as pf
import numpy as np

dir = '/mnt/ceph/users/neisner/latte/output_LATTE/data/s0006/'

data = pf.open(dir+'tess2018349182500-s0006-0000000261061538-0126-s_lc.fits')

ticid = data[0].header['TICID']
sector = data[0].header['SECTOR']
tessmag = data[0].header['TESSMAG']
teff = data[0].header['TEFF']
srad = data[0].header['RADIUS']


time = data[1].data['TIME']
flux = data[1].data['PDCSAP_FLUX'] # pre-search data conditioning flux
bkg = data[1].data['SAP_BKG'] # background flux
sap_flux = data[1].data['SAP_FLUX'] # raw flux
quality = data[1].data['QUALITY'] # quality flags

time_clean = time[np.isfinite(time) * np.isfinite(flux)]
flux_clean = flux[np.isfinite(time) * np.isfinite(flux)]

# Make Lomb-Scargle periodogram
from astropy.timeseries import LombScargle
import numpy as np

deltaf = 0.5/(np.max(time_clean) - np.min(time_clean))
maxf = 0.5 / np.median(time_clean[1:] -time_clean[:-1]) # assumes data are ordered in time
fgrid = np.arange(deltaf, maxf, deltaf)
amp_wg = LombScargle(time_clean, flux_clean).power(fgrid) 