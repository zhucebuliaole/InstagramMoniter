'''
@File  :predictor.py
@Author:qileLiang
@Email ：liangqile@outlook.com
@Date  :2021/4/30 10:10
'''
import torch
from sklearn import metrics

from Net import Net
import pandas as pd

df = pd.read_csv('../data/TestSet.csv', encoding='utf8', engine='python', chunksize=None)
# print(df)
# df.sample(frac=1)
test_y = df['label']
features = list(df.columns)
features.remove('label')
del df['label']
features.remove('user_id')
del df['user_id']
features.remove('is_joined_recently')
del df['is_joined_recently']
features.remove('counter')
del df['counter']
num_features = len(features)

# 正则化
# standardize = lambda x: (x - x.mean()) / x.std()
# for feature in features:
#     df[feature] = df[feature].pipe(standardize)
x_test = torch.from_numpy(df.to_numpy()).float()
net = Net(num_features)
net.load_state_dict(torch.load('../net_weights.pth', map_location=torch.device('cpu')))
# net = torch.load('net.pth')
net.eval()
test = net(x_test)
print(test)
nn_prob = torch.sigmoid(test)
nn_pred = nn_prob.round()
nn_prob = nn_prob.squeeze(dim=1).detach().numpy()
nn_pred = nn_pred.squeeze(dim=1).detach().numpy()
print(nn_prob)
print(nn_pred)
print("MyModel:", "Acc:", round(metrics.accuracy_score(test_y, nn_pred), 4))