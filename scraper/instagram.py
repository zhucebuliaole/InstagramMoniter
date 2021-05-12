import pandas as pd
import traceback
import random
import os
import re
import sys
import json
import time
import random
import requests
import pymongo
from pyquery import PyQuery as pq

# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client['instagram']
# table_user = db['user']
# table_post = db['post']

url_base = 'https://www.instagram.com/{}/'
uri = 'https://www.instagram.com/graphql/query/?query_hash=a5164aed103f24b03e7b7747a2d94e3c&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%22%7D'

proxies = {
  'http': 'https://sovea.top:7890',
  'https': 'https://sovea.top:7890',
}

headers = {
    'authority': 'www.instagram.com',
    'method': 'GET',
    'path': '/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%221507979106%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A24%7D',
    'scheme': 'https',
    'cookie': 'ig_did=D0BBE613-E4FB-43FF-BE61-BD2773F28215; mid=X8J0rAALAAHzbjA4odl8yodBLon7; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; csrftoken=C4YxPdgI63qPIJ8hDWt9DIqcrFleomtk; ds_user_id=40009934193; sessionid=40009934193:jSydV4x95fjpQ2:6; shbid=8899; shbts=1618748446.3717258; rur=PRN; fbsr_124024574287414=Kuw9sxnllT7VEy65ZTOBrlbm2fRmFqLnWRDpAiNjV0o.eyJ1c2VyX2lkIjoiMTAwMDUyMzE1MjkwODE1IiwiY29kZSI6IkFRQm5HcFYtcUhXdWxOSTRzNWh6OXQ3Q2c3WldPczZXZUg2RWkwUTNIVUtZRUZmSllaaUNiNm9iU19KODk5VlFNTDk3VXJqVUEtcVMyOC1CUTUtQWJIMnNFZWdsd1k2LVZjRlozRHRTbWxDLUktbGJYSmd3ZnVfQjFReFZYaWxEYUJka1FnVTVRSl9majFQVXZmNlp2VVpYaFRlYnJ3ZWR4SnJhdERYX3luSlhBTTJmdGNWSEg0UktUa293VEpDelVnOVlTUEt4cVhRSHlRalNqQ294MWd5aU8xZFVRWDIwYzBOOE1SMUxqbkxyajdXRmkySzV1TkJ0WmlrZGc4V25jLXlwaDdzMUh3VXVYaWlUTnpzQ3pZal9wbWYxcU54ZzVDVG5rby12ZWZqNEVTZzllMjZSUW9UU2psRlVWR0FwNnBNb1h5R3pUMXd5Z05JSllENzdIQnVzIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQU1zM1FoRjFaQkcwbEZ1bzk4cEplMkVaQWZGMTFEZjBNdEdxOXVWeTZrRGJJYnpFdWEzSGVPQTYyaDZQRmVaQmVBbVNCTDlKaEhSZHVaQUxYVkZ4ZHc0b2JRSkZWaFBUcXV5TzZGclNaQUV4dlhubEhjV3BxYm90cmdlbk5SaUZUaTJYTzQ4dlBPM0dBWkNFdlNnTm5aQ1pDdHdsbXl4NFhUYXpKWFZQcnVuUiIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNjE4NzQ5ODc1fQ',
    'referer': 'https://www.instagram.com/skuukzky/followers/?hl=zh-cn',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'x-csrftoken': 'C4YxPdgI63qPIJ8hDWt9DIqcrFleomtk',
    'x-ig-app-id':'936619743392459',
    'x-ig-www-claim': 'hmac.AR3dCaDVELkM5_jUcWy6BgoYx5qdPkk_FpQ-5YBrNqQoswNP',
    'x-requested-with': 'XMLHttpRequest',
}
def get_html(url):
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        # print(response.text)
        if response.status_code == 200:
            return response.text
        else:
            print('请求网页源代码错误, 错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        return None
def get_json(url):
    try:
        response = requests.get(url, headers=headers, timeout=10, proxies=proxies)
        if response.status_code == 200:
            return response.json()
        else:
            print('请求网页json错误, 错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        time.sleep(60 + float(random.randint(1, 4000))/100)
        return get_json(url)
def get_content(url):
    try:
        response = requests.get(url, headers=headers, timeout=10, proxies=proxies)
        if response.status_code == 200:
            return response.content
        else:
            print('请求照片二进制流错误, 错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        return None
def get_urls(html):
    id, username = '', ''
    user_id = re.findall('"profilePage_([0-9]+)"', html, re.S)[0]
    print('user_id：' + user_id)
    doc = pq(html)
    items = doc('script[type="text/javascript"]').items()
    for item in items:
        if item.text().strip().startswith('window._sharedData'):
            js_data = json.loads(item.text()[21:-1], encoding='utf-8')
            user = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]
            id = user['id']
            country_code = js_data['country_code']
            username = user['username']
            fullname = user['full_name']
            is_joined_recently = user['is_joined_recently']
            is_private = user['is_private']
            is_verified = user['is_verified']
            is_business_account = user['is_business_account']
            highlight_reel_count = user['highlight_reel_count']
            intro = user['biography']
            external_url = user['external_url']
            following_count = user['edge_follow']['count']
            followed_count = user['edge_followed_by']['count']
            post_count = user['edge_owner_to_timeline_media']['count']
            new_info_data = {
                    'user_id': id,
                    'country_code': country_code,
                    'user_name': username,
                    'fullname': fullname,
                    'intro': intro,
                    'external_url': external_url,
                    'is_joined_recently':is_joined_recently,
                    'is_private':is_private,
                    'is_verified':is_verified,
                    'is_business_account':is_business_account,
                    'highlight_reel_count':highlight_reel_count,
                    'following_count': following_count,
                    'followed_count': followed_count,
                    'post_count': post_count
                }
            print(new_info_data)
            list_values = [i for i in new_info_data.values()]
            df = pd.DataFrame(columns=['user_id','country_code','user_name','fullname','intro','external_url','is_joined_recently','is_private','is_verified','is_business_account','highlight_reel_count','following_count','followed_count','post_count'])
            df = df.append(new_info_data,ignore_index=True)
            df.to_csv('data/user_csv.csv', mode='a',header=True, index=None,encoding="utf-8")
            # table_user.update_one({'id': id}, {'$set': {
            #     'user_id': id,
            #     'country_code': country_code,
            #     'user_name': username,
            #     'fullname': fullname,
            #     'intro': intro,
            #     'external_url': external_url,
            #     'is_joined_recently':is_joined_recently,
            #     'is_private':is_private,
            #     'is_verified':is_verified,
            #     'is_business_account':is_business_account,
            #     'highlight_reel_count':highlight_reel_count,
            #     'following_count': following_count,
            #     'followed_count': followed_count,
            #     'post_count': post_count
            # }}, True)

            # print(js_data)
            # time.sleep(1000)
            edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
            page_info = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]['page_info']
            cursor = page_info['end_cursor']
            flag = page_info['has_next_page']
            for edge in edges:
                post_id = edge['node']['id']
                if len(edge['node']['edge_media_to_caption']['edges'])>=1:
                    post_text = edge['node']['edge_media_to_caption']['edges'][0]['node']['text']
                post_time = edge['node']['taken_at_timestamp']
                post_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(post_time))
                comment_count = edge['node']['edge_media_to_comment']['count']
                like_count = edge['node']['edge_media_preview_like']['count']
                urls = []
                if edge['node']['display_url']:
                    display_url = edge['node']['display_url']
                    # print(display_url)
                    urls.append(display_url)
                urls = ';'.join(urls)
                # table_post.update_one({'post_id': post_id}, {'$set': {
                #     'user_id': id,
                #     'user_name': username,
                #     'post_id': post_id,
                #     'time': post_time,
                #     'comment_count': comment_count,
                #     'like_count': like_count,
                #     'img_urls': urls,
                #     'post_text': post_text,
                #     '#_count': post_text.count('#'),
                #     '@_count': post_text.count('@'),
                # }}, True)
                new_post_data = {
                    'user_id': id,
                    'user_name': username,
                    'post_id': post_id,
                    'time': post_time,
                    'comment_count': comment_count,
                    'like_count': like_count,
                    'img_urls': urls,
                    'post_text': post_text,
                    '#_count': post_text.count('#'),
                    '@_count': post_text.count('@'),
                }
                print(new_post_data)
                list_values = [i for i in new_post_data.values()]
                df = pd.DataFrame(columns=['user_id','user_name','post_id','time',
            'comment_count','like_count','img_urls','post_text','#_count','@_count'])
                df = df.append(new_post_data,ignore_index=True)
                df.to_csv('data/post_csv.csv', mode='a',header=True, index=None,encoding="utf-8")

            # print(cursor, flag)
    while flag:
        url = uri.format(user_id=user_id, cursor=cursor)
        js_data = get_json(url)
        infos = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
        cursor = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        flag = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        for edge in infos:
            # print('\n\n\n\n',edge)
            post_id = edge['node']['id']
            if len(edge['node']['edge_media_to_caption']['edges'])>=1:
                post_text = edge['node']['edge_media_to_caption']['edges'][0]['node']['text']
            post_time = edge['node']['taken_at_timestamp']
            post_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(post_time))
            comment_count = edge['node']['edge_media_to_comment']['count']
            like_count = edge['node']['edge_media_preview_like']['count']
            urls = []
            if edge['node']['is_video']:
                video_url = edge['node']['video_url']
                if video_url:
                    print(video_url)
                    # urls.append(video_url)
            else:
                if edge['node']['display_url']:
                    display_url = edge['node']['display_url']
                    print(display_url)
                    urls.append(display_url)
            urls = ';'.join(urls)
            # table_post.update_one({'post_id': post_id}, {'$set': {
            #     'user_id': id,
            #     'user_name': username,
            #     'post_id': post_id,
            #     'time': post_time,
            #     'comment_count': comment_count,
            #     'like_count': like_count,
            #     'img_urls': urls,
            #     'post_text': post_text,
            #     '#_count': post_text.count('#'),
            #     '@_count': post_text.count('@'),
            # }}, True)
            new_post_data = {
                    'user_id': id,
                    'user_name': username,
                    'post_id': post_id,
                    'time': post_time,
                    'comment_count': comment_count,
                    'like_count': like_count,
                    'img_urls': urls,
                    'post_text': post_text,
                    '#_count': post_text.count('#'),
                    '@_count': post_text.count('@'),
            }
            print(new_post_data)
            list_values = [i for i in new_post_data.values()]
            df = pd.DataFrame(columns=['user_id','user_name','post_id','time',
            'comment_count','like_count','img_urls','post_text','#_count','@_count'])
            df = df.append(new_post_data,ignore_index=True)
            df.to_csv('../data/post_csv.csv', mode='a',index=None,encoding="utf-8")
def main(user):
    get_urls(get_html(url_base.format(user)))


if __name__ == '__main__':
    main(input())
    # df = pd.read_csv('source.csv')
    # for index, row in df.iterrows():
    #     print('{}/{}'.format(index, df.shape[0]), row['username'])

    #     if row['isFinished']>0:
    #         continue
    #     user_name = row['username']
    #     try:
    #         start = time.time()
    #         main(user_name)
    #         end = time.time()
    #         spent = end - start
    #         print('spent {} s'.format(spent))
    #         df.loc[index, 'isFinished'] = 1
    #         df.to_csv('source.csv', index=False, encoding='utf-8-sig')
    #         time.sleep(random.randint(2,3))
    #     except Exception as e:
    #         # if isinstance(e, IndexError) or isinstance(e, TypeError):
    #         if isinstance(e, IndexError):
    #             print('{} 改名了'.format(user_name))
    #             df.loc[index, 'isFinished'] = 2
    #             df.to_csv('source.csv', index=False, encoding='utf-8-sig')
    #             continue
    #         print(traceback.format_exc())
    #         break
