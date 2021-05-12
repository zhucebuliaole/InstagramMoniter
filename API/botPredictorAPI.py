"""
@File  :botPredictorAPI.py
@Author:qileLiang
@Email ：liangqile@outlook.com
@Date  :2021/5/9 16:19
@Description：A RESTful API for bot detection
"""
import torch
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, request
from Net import Net
import json
import pandas as pd

app = Flask(__name__)
api = Api(app)
num_features = 21
net = Net(num_features)
net.load_state_dict(torch.load('../net_weights.pth', map_location=torch.device('cpu')))
net.eval()


class predictResults(Resource):
    def post(self):
        data = request.get_data()
        jsonData = json.loads(data)
        df = pd.DataFrame(jsonData.items())
        df = df.drop(axis=1,columns=0)
        df = df.transpose()
        df.astype(float)
        xPredict = torch.from_numpy(df.to_numpy()).float()
        result = net(xPredict)
        resultData = {}
        resultData['result'] = torch.sigmoid(result).round().item()
        return json.dumps(resultData)



api.add_resource(predictResults, '/predictTasks')

if __name__ == '__main__':
    app.run()
