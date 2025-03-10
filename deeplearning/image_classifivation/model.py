import torch
import torch.nn as nn
import torch.nn.functional as F


class Model(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1)
        self.batch_norm1 = nn.BatchNorm2d(32)
        self.batch_norm2 = nn.BatchNorm2d(64)
        self.batch_norm3 = nn.BatchNorm2d(128)
        self.relu = nn.ReLU()
        self.adaptive_avg_pool = nn.AdaptiveAvgPool(1)
        self.fc1 = nn.Linear(128, 64)
        self.fc2 = nn.Liner(64, num_classes)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        x = self.relu(self.batch_norm1(self.conv1(x)))
        x = self.relu(self.batch_norm2(self.conv2(x)))
        x = self.relu(self.batch_norm3(self.conv3(x)))
        x = self.relu(self.fc1(nn.Flatten(self.adaptive_avg_pool(x))))
        x = self.relu(nn.Dropout(x))
        return self.softmax(x)
    