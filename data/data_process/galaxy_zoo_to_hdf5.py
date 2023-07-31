import h5py
from PIL import Image
from io import BytesIO
from zipfile import ZipFile
import numpy as np
from threading import Lock
from multiprocessing import Pool

# As much as I want to use the zip directly, it seems using multiple processes and nodes are unstable.
path = '/mnt/home/wwong/ceph/Dataset/ThereIsASky/galaxyzoo/images_gz2.zip'
length = 1024

dataset = ZipFile(path, 'r')
name_list = dataset.namelist()
name_list = list(filter(lambda x: name_list[2] not in x, name_list))[1:-4]
dataset.close()
N_entry = len(name_list)

idx_list = np.arange(0, N_entry,1024)

def process_data(start):
    dataset = ZipFile(path, 'r')
    name_list = dataset.namelist()
    name_list = list(filter(lambda x: name_list[2] not in x, name_list))[1:-4]
    result = []
    for idx in range(start, min(start+length,N_entry)):
        img = Image.open(BytesIO(dataset.read(name_list[idx])))
        img = np.array(img)
        result.append(img)
    dataset.close()
    return np.stack(result)


def multiprocess_data(idx_list):
    with Pool(112) as p:
        tensor = p.map(process_data, idx_list)
        p.close()
    return tensor

data = multiprocess_data(idx_list)
data = np.concatenate(data, axis=0).transpose(0,3,1,2)

output_path = '/mnt/home/wwong/ceph/Dataset/ThereIsASky/galaxyzoo/images_gz2.hdf5'
with h5py.File(output_path, 'w') as f:
    f.create_dataset("images", data=data)
