import astropy.io.fits as fits
import numpy as np
import h5py 

top_dir = '/mnt/ceph/users/wwong/Dataset/ThereIsASky/sdss/MaStar/'

mastarall = fits.open(f'{top_dir}mastarall-v3_1_1-v1_7_7.fits')
params = fits.open(f'{top_dir}mastar-goodvisits-v3_1_1-v1_7_7-params-v2.fits')[1].data
spectra = fits.open(f'{top_dir}mastar-goodspec-v3_1_1-v1_7_7.fits')[1].data

teff, logg, feh = params['TEFF_MED'], params['LOGG_MED'], params['FEH_MED']
ngroups = params['NGROUPS']   #used to remove stars without valid parameter entries.

ksel = np.where((ngroups != 0))[0]
print(len(mastarall[2].data[ksel]))   #how many spectra are selected

length = spectra['WAVE'][0]
flux = spectra['FLUX']

labels = {'teff': teff[ksel], 'logg': logg[ksel], 'feh': feh[ksel]}

with h5py.File(f'{top_dir}mastar.hdf5', 'w') as f:
    f.create_dataset('data', data=flux)
    group = f.create_group('labels')
    for key, value in labels.items():
        group.create_dataset(key, data=value)
    
    f.attrs['wavelength_grid'] = length