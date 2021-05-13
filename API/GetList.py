import requests
from time import sleep
import pandas as pd
import json

requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接



    # proxies = {
    # 'http': 'https://sovea.top:7890',
    # 'https': 'https://sovea.top:7890',
    # }
proxies = {
    'http': '127.0.0.1:7890',
    'https': '127.0.0.1:7890',
    }

def getList(inputUserName):
    # 构造一个请求头
    headers = {
    'authority': 'www.instagram.com',
    'method': 'GET',
    'path':'/' + inputUserName + '/?__a=1',
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'ig_did=22291BA2-9977-490C-AD8F-77A545179274; ig_nrcb=1; mid=YHzigAALAAHQHRdBBPtschF7FrI5; datr=RKmbYFUJAadmRXOsfon0kDpt; ds_user_id=47793281340; sessionid=47793281340%3AguIQJ9uNbBZRZc%3A18; csrftoken=p1t3NmYWzv1xAH7CZRiJnJdhsdm5LaPf; rur=VLL',
    }

    response = requests.get('https://www.instagram.com/' + inputUserName + '/?__a=1',  headers=headers,proxies=proxies).text
    res = json.loads(response)
    userID = res['graphql']['user']['id']
    print(userID)
    userN = res['graphql']['user']['username']
    print(userN)
    followerList=[]
    followingList=[]

    for x in range(0,2):
        end_cursor = ''
        has_next = True
        queryhash = ''
        fileName = ''
        edgeFoll = ''
        if x == 0:
            queryhash = '5aefa9893005572d237da5068082d8d5'
            #fileName = "followerList.csv"
            edgeFoll = 'edge_followed_by'
        if x == 1:
            queryhash = 'd04b0a864b4b54837c0d870b0e77e076'
            #fileName = "followingList.csv"
            edgeFoll = 'edge_follow'
    # print(queryhash + "     " +  fileName + "    ")
        while has_next:
        # id是需要替换的，每一个用户的 id 不一样
        # 粉丝和关注的queryhash不一样
        # 'query_hash', 'd04b0a864b4b54837c0d870b0e77e076'
        # 是关注列表的hash
        # 粉丝列表的query
        # 5aefa9893005572d237da5068082d8d5

            params = (
                ('query_hash', queryhash),
                ('variables',
                '{"id":"' + userID + '","include_reel":true,"fetch_mutual":false,"first":12,"after":"' + end_cursor + '"}'),
            )
            response = requests.get('https://www.instagram.com/graphql/query/', headers=headers, params=params,proxies=proxies).text

            res = json.loads(response)
            has_next = res['data']['user'][edgeFoll]['page_info']['has_next_page']
        # 获取的是json的hasnext的值
            print(has_next)
            end_cursor = res['data']['user'][edgeFoll]['page_info']['end_cursor']
        # 更新cursor的值，下一页就是这个
            edges = res['data']['user'][edgeFoll]['edges']

            # out = open("../data/human/"+fileName, "a+", newline="", encoding="utf-8-sig")
            # csv_writer = csv.writer(out, dialect="excel")

            # for i in edges:
            #       row = [i['node']['id'], i['node']['username'], i['node']['full_name']]
            #       csv_writer.writerow(row)

            if x==0:
                for i in edges:
                    followerList.append(i['node']['username'])
            if x==1:
                for i in edges:
                    followingList.append(i['node']['username'])

            # out.close()
        
            sleep(10)
        if x == 0:
            print("=============爬取粉丝列表FINISH==============")

        if x == 1:
            print("=============爬取关注列表FINISH==============")
    List = [followerList,followingList]
    print("=============爬虫FINISH==============")
    sleep(5)
    return List