import astropy.io.fits as pf
import numpy as np
import os
import h5py
from multiprocessing import Pool


dir = '/mnt/ceph/users/neisner/latte/output_LATTE/data/s0006/'
output_name = '/mnt/home/wwong/ceph/Dataset/ThereIsASky/tess/sector_length_234.h5'

file_list = os.listdir(dir)

segment_length = 234 # 15678 /234 = 67 segments, 67 is a prime number

def split_segment(array, segment_length):
    return np.split(array, np.arange(0, len(array), segment_length))[1:-1]

def get_continous_index(array, segment_length):
    nan_index = np.isnan(array)
    where_nan = np.argwhere(nan_index)[:, 0]
    diff_nan = np.diff(where_nan)
    nan_longer_than_segment = np.argwhere(diff_nan > segment_length)[:, 0]
    return where_nan, nan_longer_than_segment

def get_continous_segments(array, where_nan, nan_longer_than_segment, segment_length):
    continous_array = [array[(where_nan[i]+1):(where_nan[i+1]-1)] for i in nan_longer_than_segment]
    continous_array = np.concatenate(list(map(lambda x: split_segment(x,segment_length), continous_array)))
    return continous_array

def make_training_example(data_path: str):

    data = pf.open(data_path)
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

    where_nan, nan_longer_than_segment = get_continous_index(flux, segment_length)
    continous_flux = get_continous_segments(flux, where_nan, nan_longer_than_segment, segment_length)
    continous_time = get_continous_segments(time, where_nan, nan_longer_than_segment, segment_length)
    continous_bkg = get_continous_segments(bkg, where_nan, nan_longer_than_segment, segment_length)
    continous_sap_flux = get_continous_segments(sap_flux, where_nan, nan_longer_than_segment, segment_length)

    return {'ticid': ticid, 'sector': sector, 'tessmag': tessmag, 'teff': teff, 'srad': srad, 'time': continous_time, 'flux': continous_flux, 'bkg': continous_bkg, 'sap_flux': continous_sap_flux}

metadata = []
label = []
data = []

def process_file(file_path):
    metadata = np.empty((0, 2))
    label = np.empty((0, 3))
    data = np.empty((4, 0, segment_length))
    try:
        example = make_training_example(dir+file_path)
        metadata = np.repeat(np.array([example['ticid'], example['sector']])[None], example['time'].shape[0], axis=0)
        label = np.repeat(np.array([example['tessmag'], example['teff'], example['srad']])[None], example['time'].shape[0], axis=0)
        data = np.array([example['time'], example['flux'], example['bkg'], example['sap_flux']])
    except:
        pass

    return metadata, label, data

file_list[0] = file_list[0]+'aklsfj'

def multiprocess_data(file_list):
    with Pool(24) as p:
        metadata, label, data = zip(*p.map(process_file, file_list))
        p.close()
    return metadata, label, data

metadata, label, data = multiprocess_data(file_list)


metadata = np.concatenate(metadata,axis=0)
label = np.concatenate(label,axis=0).astype(np.float32)
data = np.concatenate(data,axis=1)
with h5py.File(output_name, 'w') as f:
    meta_data_group = f.create_group('metadata')
    meta_data_group.create_dataset('ticid', data=metadata[0])
    meta_data_group.create_dataset('sector', data=metadata[1])

    label_group = f.create_group('label')
    label_group.create_dataset('tessmag', data=label[0])
    label_group.create_dataset('teff', data=label[1])
    label_group.create_dataset('srad', data=label[2])

    data_group = f.create_group('data')
    data_group.create_dataset('time', data=data[0])
    data_group.create_dataset('flux', data=data[1])
    data_group.create_dataset('bkg', data=data[2])
    data_group.create_dataset('sap_flux', data=data[3])

# time_clean = time[np.isfinite(time) * np.isfinite(flux)]
# flux_clean = flux[np.isfinite(time) * np.isfinite(flux)]

# # Make Lomb-Scargle periodogram
# from astropy.timeseries import LombScargle
# import numpy as np

# deltaf = 0.5/(np.max(time_clean) - np.min(time_clean))
# maxf = 0.5 / np.median(time_clean[1:] -time_clean[:-1]) # assumes data are ordered in time
# fgrid = np.arange(deltaf, maxf, deltaf)
# amp_wg = LombScargle(time_clean, flux_clean).power(fgrid) 