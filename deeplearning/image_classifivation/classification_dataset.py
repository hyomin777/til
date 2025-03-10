import os
from torch.utils.data import Dataset
import torchvision.transforms as transforms
from PIL import Image


class ClassificationDataset(Dataset):
    def __init__(
            self,
            dataset_dir="/classification_dataset",
            transform=None
    ):
        super().__init__()
        self.image_abs_path = dataset_dir
        self.transform = transform

        if self.transform is None:
            self.transform = transforms.Compose([
                transforms.Resize(256),
                transforms.RandomCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])
        
        self.label_list = os.listdir(self.image_abs_path)
        self.label_list.sort()
        self.x_list = []
        self.y_list = []

        for label_index, label_str in enumerate(self.label_list):
            img_path = os.path.join(self.image_abs_path, label_str)
            img_list = os.listdir(img_path)
            for img in img_list:
                self.x_list.append(os.path.join(img_path, img))
                self.y_list.append(label_index)
        
    def __len__(self):
        return len(self.x_list)

    def __getitem__(self, idx):
        image = Image.open(self.x_list[idx])
        
        if image.mode is not "RGB":
            imgae = image.convert("RGB")
        if self.transform is not None:
            image = self.transform(image)
        
        return image, self.y_list[idx]
    
    def __save_label_map__(self, dst_text_path="label_map.txt"):
        label_list = self.label_list

        f = open(dst_text_path, 'w')
        for i in range(len(label_list)):
            f.write(label_list[i] + "\n")
        f.close()
    
    def __num_classes__(self):
        return len(self.label_list)