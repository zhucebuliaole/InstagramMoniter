# encoding: utf-8
import csv
import scrapy
import json
import requests
from time import sleep

# 构造一个用户输入id
inputUserName = input('请输入希望爬取的用户名:')
print(inputUserName)

# 构造一个请求头
headers = {
    'authority': 'www.instagram.com',
    'method': 'GET',
    'path':'/' + inputUserName + '/?__a=1',
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'ig_nrcb=1; ig_did=13D44984-180C-4DF5-847C-B4AA1862D868; mid=YFL3YQAEAAG4nGfE7_yJ74JMyLur; fbm_124024574287414=base_domain=.instagram.com; shbid=6949; shbts=1616810931.6809547; rur=RVA; csrftoken=r8stYGg5OH8YWwMpad0f2mryZvcLKeAN; ds_user_id=11673735787; sessionid=11673735787%3ASCC0wmwlQpDuG0%3A16; fbsr_124024574287414=MNYm-o37xuDp72fU6tqqeTMVOxZatFrdA7a1dxAmahA.eyJ1c2VyX2lkIjoiMTAwMDEyNjQ1MTgwMTg2IiwiY29kZSI6IkFRQ1VmMWRuLVNKUVA2VklLTk5TeVA0MU05dEY4ellzdlFSM3cxbzVPbDFCWmxWcHpERzdxVFZTNG0zWXVTV2NNYVhOYXJ3QkJPVEtYSXVsMXJKbndUX3pYS0ZhOEhPQ3FaMzg2d2Yxb3A4U3FmT1RYSmc3eklBcklUQUJvT3JPelhoa1FMbGIzMWlzOVozQkVYRUtGLVpUSGVGa2N5eENMOHZNMWJrSFkxZi10OFowLW8xbG5PZm5SVldyY2VFWE1ZbWwzLXRLdXA5bEdDTjlObVRsNHFhMEpMdlYtVXBxVWhSYmpfcWFaMUpLTnpqOGxNSGlKcWhQTnVKZU9QRlRHNzNKZUpsZ1FZQ2FnN2toU0duRHNNbnZUT05Pc2ZLYnlBWlZWSmlUNnFWbk1sdGRpTExleTZ4MjhUUGVKdkJ2dG5MQWtvWUt1NmFEZjZwT290QUs0dGl4Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUM5TW9wTG1qdldnQVpBRDZqS3VuUDRTUjVKRURoRTB3NHlkQ0F2T01vWXZCTlpBRFc4cHMxeEhXWWJNbkhhQ3hSc2JUNURCWkJkcU9DcFZFVFpCTGhJQU1aQUFPUXJzaTgxUFVyZjRRdmxReEhCWkFaQjJPNkE0UlgxQmVYS2tobldHWXh3b2Q0YTBQdWN6aHByTmEwQ21pSHNtb0c1WWthR0FnQ05XbUNWIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE2MTY4MTU2OTh9; fbsr_124024574287414=MNYm-o37xuDp72fU6tqqeTMVOxZatFrdA7a1dxAmahA.eyJ1c2VyX2lkIjoiMTAwMDEyNjQ1MTgwMTg2IiwiY29kZSI6IkFRQ1VmMWRuLVNKUVA2VklLTk5TeVA0MU05dEY4ellzdlFSM3cxbzVPbDFCWmxWcHpERzdxVFZTNG0zWXVTV2NNYVhOYXJ3QkJPVEtYSXVsMXJKbndUX3pYS0ZhOEhPQ3FaMzg2d2Yxb3A4U3FmT1RYSmc3eklBcklUQUJvT3JPelhoa1FMbGIzMWlzOVozQkVYRUtGLVpUSGVGa2N5eENMOHZNMWJrSFkxZi10OFowLW8xbG5PZm5SVldyY2VFWE1ZbWwzLXRLdXA5bEdDTjlObVRsNHFhMEpMdlYtVXBxVWhSYmpfcWFaMUpLTnpqOGxNSGlKcWhQTnVKZU9QRlRHNzNKZUpsZ1FZQ2FnN2toU0duRHNNbnZUT05Pc2ZLYnlBWlZWSmlUNnFWbk1sdGRpTExleTZ4MjhUUGVKdkJ2dG5MQWtvWUt1NmFEZjZwT290QUs0dGl4Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUM5TW9wTG1qdldnQVpBRDZqS3VuUDRTUjVKRURoRTB3NHlkQ0F2T01vWXZCTlpBRFc4cHMxeEhXWWJNbkhhQ3hSc2JUNURCWkJkcU9DcFZFVFpCTGhJQU1aQUFPUXJzaTgxUFVyZjRRdmxReEhCWkFaQjJPNkE0UlgxQmVYS2tobldHWXh3b2Q0YTBQdWN6aHByTmEwQ21pSHNtb0c1WWthR0FnQ05XbUNWIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE2MTY4MTU2OTh9',
}
response = requests.get('https://www.instagram.com/' + inputUserName + '/?__a=1',  headers=headers).text
res = json.loads(response)
userID = res['graphql']['user']['id']
print(userID)
userN = res['graphql']['user']['username']
print(userN)

for x in range(2):
    end_cursor = ''
    has_next = True
    queryhash = ''
    fileName = ''
    edgeFoll = ''
    if x == 0:
        queryhash = '5aefa9893005572d237da5068082d8d5'
        fileName = "followerList.csv"
        edgeFoll = 'edge_followed_by'
    if x == 1:
        queryhash = 'd04b0a864b4b54837c0d870b0e77e076'
        fileName = "followingList.csv"
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
        response = requests.get('https://www.instagram.com/graphql/query/', headers=headers, params=params).text

        res = json.loads(response)
        has_next = res['data']['user'][edgeFoll]['page_info']['has_next_page']
        # 获取的是json的hasnext的值
        print(has_next)
        end_cursor = res['data']['user'][edgeFoll]['page_info']['end_cursor']
        # 更新cursor的值，下一页就是这个
        edges = res['data']['user'][edgeFoll]['edges']

        out = open(fileName, "a+", newline="", encoding="utf-8-sig")
        csv_writer = csv.writer(out, dialect="excel")

        for i in edges:
            row = [i['node']['id'], i['node']['username'], i['node']['full_name']]
            csv_writer.writerow(row)

        out.close()
        
        sleep(5)
    if x == 0:
        print("=============爬取粉丝列表FINISH==============")

    if x == 1:
        print("=============爬取关注列表FINISH==============")

print("=============爬虫FINISH==============")