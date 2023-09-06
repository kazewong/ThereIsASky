import astropy.table as at
import numpy as np
import os

golden_sample_path = '/mnt/ceph/users/gaia/dr3/csv/GoldSampleFgkmStars/GoldSampleFgkmStars.csv.gz'
golden_sample = at.Table.read(golden_sample_path, format="ascii.ecsv")
golden_source_id = golden_sample['source_id']
golden_teff = golden_sample['teff_gspspec']
golden_logg = golden_sample['logg_gspspec']

continous_spectrum_path = '/mnt/ceph/users/gaia/dr3/csv/XpContinuousMeanSpectrum'
continous_spectrum_dir = os.listdir(continous_spectrum_path)

def find_golden_spectra(path: str):
    data = at.Table.read(path, format="ascii.ecsv")
    source_id = data['source_id']
    match_id = np.in1d(golden_source_id, source_id)
    teff_matched = golden_teff[match_id]
    logg_matched = golden_logg[match_id]
    match_id = np.in1d(source_id, golden_source_id)
    bp = data[match_id]['bp_coefficients']
    rp = data[match_id]['rp_coefficients']
    return teff_matched, logg_matched, bp, rp

test = find_golden_spectra(continous_spectrum_path+'/'+continous_spectrum_dir[0])