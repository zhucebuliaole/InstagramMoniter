"""
@File  :tabNet.py
@Author:qileLiang
@Email ：liangqile@outlook.com
@Date  :2021/5/12 11:11
@Description：train our model by tabNet 
"""
from pytorch_tabnet.tab_model import TabNetClassifier

import torch
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score

import pandas as pd
import numpy as np

import os
from pathlib import Path

from matplotlib import pyplot as plt

train = pd.read_csv('data/FinalDataSetResult2.csv', encoding='utf8', engine='python', chunksize=None)

# 划分测试集，训练集，验证集
if "Set" not in train.columns:
    train["Set"] = np.random.choice(["train", "valid", "test"], p=[.8, .1, .1], size=(train.shape[0],))
train_indices = train[train.Set == "train"].index
valid_indices = train[train.Set == "valid"].index
test_indices = train[train.Set == "test"].index

nunique = train.nunique()
types = train.dtypes

categorical_columns = []
categorical_dims = {}
for col in train.columns:
    if types[col] == 'object' or nunique[col] < 3:
        print(col, train[col].nunique())
        l_enc = LabelEncoder()
        train[col] = train[col].fillna("VV_likely")
        train[col] = l_enc.fit_transform(train[col].values)
        categorical_columns.append(col)
        categorical_dims[col] = len(l_enc.classes_)
    else:
        train.fillna(train.loc[train_indices, col].mean(), inplace=True)
print("\n")
print(nunique)

unused_feat = ['Set']

features = [col for col in train.columns if col not in unused_feat + ['label']]

cat_idxs = [i for i, f in enumerate(features) if f in categorical_columns]

cat_dims = [categorical_dims[f] for i, f in enumerate(features) if f in categorical_columns]

print(features)
print(cat_idxs)
print(cat_dims)

clf = TabNetClassifier(cat_idxs=cat_idxs,
                       cat_dims=cat_dims,
                       cat_emb_dim=1,
                       optimizer_fn=torch.optim.Adam,
                       optimizer_params=dict(lr=2e-2),
                       scheduler_params={"step_size": 10,  # how to use learning rate scheduler
                                         "gamma": 0.93},
                       scheduler_fn=torch.optim.lr_scheduler.StepLR,
                       mask_type='entmax'  # "sparsemax"
                       )

X_train = train[features].values[train_indices]
# X_train = np.delete(X_train,24,axis=1)
y_train = train['label'].values[train_indices]

X_valid = train[features].values[valid_indices]
# X_valid = np.delete(X_valid,24,axis=1)
y_valid = train['label'].values[valid_indices]

X_test = train[features].values[test_indices]
# X_test = np.delete(X_test,24,axis=1)
y_test = train['label'].values[test_indices]

clf.fit(
    X_train=X_train, y_train=y_train,
    eval_set=[(X_train, y_train), (X_valid, y_valid)],
    eval_name=['train', 'valid'],
    eval_metric=['auc'],
    max_epochs=1000, patience=50,
    batch_size=1028, virtual_batch_size=128,
    num_workers=0,
    weights=1,
    drop_last=False
)

fig, (ax1, ax2) = plt.subplots(2)

ax1.plot(clf.history['loss'])
ax2.plot(clf.history['train_auc'], label="train")
ax2.plot(clf.history['valid_auc'], label="valid")
plt.show()

preds = clf.predict_proba(X_test)
# preds中第2个数据是为人类的概率，第1个数据是为机器人的概率
test_auc = roc_auc_score(y_score=preds[:, 1], y_true=y_test)
print(y_test)
print("-------------------------------------------")
print(preds)
print(f"FINAL TEST SCORE FOR InstagramBot : {test_auc}")

# save tabnet model
saving_path_name = "./tabnet_model_test_1"
saved_filepath = clf.save_model(saving_path_name)
print(saved_filepath)

# define new model with basic parameters and load state dict weights
loaded_clf = TabNetClassifier()
loaded_clf.load_model(saved_filepath)

loaded_preds = loaded_clf.predict_proba(X_test)
loaded_test_auc = roc_auc_score(y_score=loaded_preds[:, 1], y_true=y_test)
loaded_test_acc = accuracy_score(y_true=y_test, y_pred=np.round(loaded_preds[:, 1]))
loaded_test_f1 = f1_score(y_test, y_pred=np.round(loaded_preds[:, 1]))

print(f"LOAD-MODEL TEST SCORE FOR InstagramBot : auc: {loaded_test_auc} acc: {loaded_test_acc} f1: {loaded_test_f1}")

print(clf.feature_importances_)
