import torchvision
from torch.utils.data import Dataset
import h5py

class GalaxyZooImageDataset(Dataset):

    def __init__(self,
                path: str,
                transform= lambda x: (x/255)*2 - 1):
        self.data = h5py.File(path, 'r')['images']
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data[idx]
        if self.transform:
            sample = self.transform(sample)
        return sample

    def get_shape(self):
        return self.data.shape[1:]

