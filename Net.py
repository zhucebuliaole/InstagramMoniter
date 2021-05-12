'''
@File  :Net.py
@Author:qileLiang
@Email ：liangqile@outlook.com
@Date  :2021/4/30 11:19
'''
import torch.nn as nn

class Net(nn.Module):
    def __init__(self, num_features):
        super().__init__()
        self.dout = nn.Dropout(p=0.5)
        self.fc1 = nn.Linear(num_features, 500)
        self.pr1 = nn.PReLU()
        self.bn1 = nn.BatchNorm1d(500)
        self.fc2 = nn.Linear(500, 200)
        self.pr2 = nn.PReLU()
        self.bn2 = nn.BatchNorm1d(200)
        self.fc3 = nn.Linear(200, 200)
        self.pr3 = nn.PReLU()
        self.bn3 = nn.BatchNorm1d(200)
        self.out = nn.Linear(200, 1)

    def forward(self, input_):
        out = self.dout(self.bn1(self.pr1(self.fc1(input_))))
        out = self.dout(self.bn2(self.pr2(self.fc2(out))))
        out = self.dout(self.bn3(self.pr3(self.fc3(out))))
        out = self.out(out)
        return out