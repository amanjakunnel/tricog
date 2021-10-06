import torch
from torch import nn
from torch.utils.data import DataLoader
from d2l import torch as d2l
import pandas as pd

class CustomCSVDataset():
    def __init__(self, datafile):
        sets = pd.read_csv(datafile, header=None)
        self.labels = sets[sets.columns[-1]]
        features = sets.iloc[:, :-1]
        max = features.max()
        self.features = features/max

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        feature = torch.tensor(self.features.iloc[idx, :]).float()
        label = torch.tensor(self.labels[idx]).long()
        return feature, label

train = CustomCSVDataset("FinOutput.csv")
test = CustomCSVDataset("TestOutput.csv")

train_iter = DataLoader(train, batch_size=32, shuffle=True)
test_iter = DataLoader(test, batch_size=32, shuffle=True)

net = nn.Sequential(nn.Flatten(), nn.Linear(1080, 256), nn.ReLU(), nn.Linear(256, 2))

def init_weights(m):
    if type(m) == nn.Linear:
        nn.init.normal_(m.weight, std=0.01)

net.apply(init_weights)

batch_size, lr, num_epochs = 32, 0.01, 1
loss = nn.CrossEntropyLoss()
trainer = torch.optim.SGD(net.parameters(), lr=lr)
net.train()
d2l.train_ch3(net, train_iter, test_iter, loss, num_epochs, trainer)