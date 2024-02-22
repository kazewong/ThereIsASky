import h5py
from astropy.io import fits
import glob
import os
import numpy as np

def read_central_spectra_fits(file: str):
    with fits.open(file) as hdul:
        flux = hdul[1].data
        mask = hdul[2].data

    return flux, mask

def read_cube_fits(file: str):
    with fits.open(file) as hdul:
        cube = hdul[1].data
        mask = hdul[3].data
        mid_point = int(hdul[1].header['NAXIS1']/2)
        print(mid_point)
        cube = cube[:, mid_point-16:mid_point+16, mid_point-16:mid_point+16]
        mask = mask[:, mid_point-16:mid_point+16, mid_point-16:mid_point+16]
    return cube, mask

cube_directory = '/mnt/ceph/users/wwong/Dataset/ThereIsASky/sdss/MaNGA/cubes/v3_1_1/'
spectra_directory = '/mnt/home/wwong/ceph/AstroProject/ThereIsASky/data/ThereIsASky/sdss/MaNGA/spectra/'
output_path = '/mnt/home/wwong/ceph/AstroProject/ThereIsASky/data/ThereIsASky/sdss/MaNGA/matched_spectra_cubes_trimmed_small.hdf5'

cube_filenames = glob.glob(
    os.path.join(cube_directory, '**', '*.fits.gz'),
    recursive=True
)

spectra_filenames = os.listdir(spectra_directory)

spectra_array = []
cube_array = []
plate_number_array = []

# Let's trust the wavelength is the same for all spectra and cubes

wavelength = fits.open(spectra_directory+spectra_filenames[0])[0].data

for spectrum in spectra_filenames[:1000]:
    plate_number = spectrum[spectrum.find("0.3.2-")+6:spectrum.find(".fits")]
    if map(lambda x: plate_number in x, cube_filenames):
        print('Match!')
        spectra = read_central_spectra_fits(spectra_directory+spectrum)
        index = np.where(list(map(lambda x: plate_number in x, cube_filenames)))[0][0]
        cube = read_cube_fits(cube_filenames[index])
        spectra_array.append(spectra)
        cube_array.append(cube)
        plate_number_array.append(plate_number.ljust(11))
    else:
        print('No match!')
        print(plate_number)

with h5py.File(output_path, 'w') as f:
    f.create_dataset('wavelength', data=wavelength)
    f.create_dataset('spectra', data=spectra_array)
    f.create_dataset('cube', data=cube_array)
    f.create_dataset('plate_number', data=plate_number_array)