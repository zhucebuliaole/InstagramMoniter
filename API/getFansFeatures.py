from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, request
import csv
import scrapy
import json
import requests
from time import sleep
import pandas as pd
import GetFeature
import GetList

app = Flask(__name__)
api = Api(app)


class scraper(Resource):
   def post(self):
      data = request.get_data()
      jsonData = json.loads(data)
      username = jsonData['username']

      List = GetList.getList(username)
      # print(List)
      if(len(List)!=0):
         followerList = List[0]
         followingList = List[1]

         GetFeature.runThread(len(followerList),followerList,0)
         GetFeature.runThread(len(followingList),followingList,1)

         resultData = {}
         resultData['result'] = []
         resultData['has_list'] = 1
         df = pd.read_csv("DataSet.csv", usecols=[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],names=['user_name_len','full_name_len','intro_len','external_url','is_joined_recently','is_private','is_verified','is_business_account','highlight_reel_count','following_count','followed_count','post_count','avg_comment','avg_like','avg_post_len','avg_#','avg_@','var_comment','var_like','var_post_len','var_#','var_@'])
         print(df['user_name_len'].tolist())
         for i in range(0,len(df['user_name_len'].tolist())):
            resultData['result'].append({'user_name_len':df['user_name_len'].tolist()[i]}) 
            resultData['result'][i]['full_name_len'] = df['full_name_len'].tolist()[i]
            resultData['result'][i]['intro_len'] = df['intro_len'].tolist()[i]
            resultData['result'][i]['external_url'] = df['external_url'].tolist()[i]
            resultData['result'][i]['is_joined_recently'] = df['is_joined_recently'].tolist()[i]
            resultData['result'][i]['is_private'] = df['is_private'].tolist()[i]
            resultData['result'][i]['is_verified'] = df['is_verified'].tolist()[i]
            resultData['result'][i]['is_business_account'] = df['is_business_account'].tolist()[i]
            resultData['result'][i]['highlight_reel_count'] = df['highlight_reel_count'].tolist()[i]
            resultData['result'][i]['following_count'] = df['following_count'].tolist()[i]
            resultData['result'][i]['followed_count'] = df['followed_count'].tolist()[i]
            resultData['result'][i]['post_count'] = df['post_count'].tolist()[i]
            resultData['result'][i]['avg_comment'] = df['avg_comment'].tolist()[i]
            resultData['result'][i]['avg_like'] = df['avg_like'].tolist()[i]
            resultData['result'][i]['avg_post_len'] = df['avg_post_len'].tolist()[i]
            resultData['result'][i]['avg_#'] = df['avg_#'].tolist()[i]
            resultData['result'][i]['avg_@'] = df['avg_@'].tolist()[i]
            resultData['result'][i]['var_comment'] = df['var_comment'].tolist()[i]
            resultData['result'][i]['var_like'] = df['var_like'].tolist()[i]
            resultData['result'][i]['var_post_len'] = df['var_post_len'].tolist()[i]
            resultData['result'][i]['var_#'] = df['var_#'].tolist()[i]
            resultData['result'][i]['var_@'] = df['var_@'].tolist()[i]
            
         print(resultData['result'])
         return json.dumps(resultData)
      else:
         resultData = {}
         resultData['has_list'] = 0
         return json.dumps(resultData)

api.add_resource(scraper,'/scraperTask')

if __name__ == '__main__':
   app.run(debug = True)