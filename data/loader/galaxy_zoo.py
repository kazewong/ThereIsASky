import torchvision
from PIL import Image
from io import BytesIO
from zipfile import ZipFile
from torch.utils.data import Dataset

class GalaxyZooImageDataset(Dataset):

    def __init__(self,
                path: str,
                transform= torchvision.transforms.ToTensor()):
        self.zip_file = ZipFile(path)
        self.transform = transform
        name_list = self.zip_file.namelist()
        self.name_list = list(filter(lambda x: name_list[2] not in x, name_list))[1:]

    def __len__(self):
        return len(self.name_list)

    def __getitem__(self, idx):
        img = Image.open(BytesIO(self.zip_file.read(self.name_list[idx])))
        if self.transform:
            img = self.transform(img)
        return img