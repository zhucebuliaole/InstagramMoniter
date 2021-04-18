# -*- coding: utf-8 -*-
import scrapy
# import scrapy.selector as Selector
from urllib.parse import urlencode
import json
from datetime import datetime
from pyquery import PyQuery as pq
from scrapy_splash import SplashRequest
import re
import time
import pandas as pd
import traceback
import random
import os
import sys
import requests
#import pymongo

API = 'beb596fbecce7ef15125ad7128bccb1b'
user_accounts = ["marvel"] 
cookies = {
    "ig_did":'C5058500-CA8A-4E2C-9AED-D2667089C593',
    "mid":'X9iyRQALAAEf8Xmlc6-ZyaUfgVyQ',
    "ig_nrcb":'1',
    "shbid":"10589",
    "csrftoken":"l1djYKTFITO3tcTO6wjDH4BMsOfgw2hQ",
    "ds_user_id":"12327440770",
    "sessionid":"12327440770%3AgN3J3EMaJm2vpw%3A8",
    "shbts":"1618217826.677595",
    "rur":"ATN"
}
log_lua = '''
function main(splash, args)
	splash:on_request(function(request)
		request:set_proxy{
			host = "sovea.top",
			port = 7890,
	}
    end)
    splash:set_custom_headers({
    ["Cookie"] = "ig_did=C5058500-CA8A-4E2C-9AED-D2667089C593; mid=X9iyRQALAAEf8Xmlc6-ZyaUfgVyQ; ig_nrcb=1; csrftoken=l1djYKTFITO3tcTO6wjDH4BMsOfgw2hQ; ds_user_id=12327440770; sessionid=12327440770%3AgN3J3EMaJm2vpw%3A8; shbid=10589; shbts=1618217826.677595; rur=ATN"
    })
	splash:go(args.url)
	splash:wait(7.0)
    local scroll_to = splash:jsfunc("window.scrollTo")
    scroll_to(0, 1800)
    return {
        html = splash:html()
      }
end
'''
index_data={}
uri = 'https://www.instagram.com/graphql/query/?query_hash=a5164aed103f24b03e7b7747a2d94e3c&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%22%7D'
def get_url(url):
    payload = {'api_key': API, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url
proxies = {
  'http': 'http://127.0.0.1:7890',
  'https': 'http://127.0.0.1:7890',
}

headers = {
    'authority': 'www.instagram.com',
    'method': 'GET',
    'path': '/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%221507979106%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A24%7D',
    'scheme': 'https',
    'cookie': 'ig_did=C5058500-CA8A-4E2C-9AED-D2667089C593; mid=X9iyRQALAAEf8Xmlc6-ZyaUfgVyQ; ig_nrcb=1; csrftoken=l1djYKTFITO3tcTO6wjDH4BMsOfgw2hQ; ds_user_id=12327440770; sessionid=12327440770%3AgN3J3EMaJm2vpw%3A8; shbid=10589; shbts=1618217826.677595; rur=ATN"',
    'referer': 'https://www.instagram.com/skuukzky/followers/?hl=zh-cn',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'x-csrftoken': 'l1djYKTFITO3tcTO6wjDH4BMsOfgw2hQ',
    'x-ig-app-id': '936619743392459',
    'x-ig-www-claim': 'hmac.AR294r-cfjuW7nL_AIiDHyw5f33yi_qxhhWbVEDtDKHlOrtI',
    'x-requested-with': 'XMLHttpRequest',
}


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['api.scraperapi.com',"www.instagram.com"]
    custom_settings = {'CONCURRENT_REQUESTS_PER_DOMAIN': 5}
    
    def get_json(url):
        try:
            response = requests.get(url, headers=headers, timeout=10, proxies=proxies)
            if response.status_code == 200:
                return response.json()
            else:
                print('请求网页json错误, 错误状态码：', response.status_code)
        except Exception as e:
            print(e)
            # time.sleep(60 + float(random.randint(1, 4000))/100)
            # return get_json(url)

    def start_requests(self):
        for username in user_accounts:
            url = f'https://www.instagram.com/{username}'
            
            yield scrapy.Request(url,cookies=cookies,meta={'proxy': 'http://sovea.top:7890'}, callback=self.parse,encoding='utf-8')
            yield SplashRequest(url=url,callback = self.parse_splash,endpoint='execute',args={"proxy": 'http://sovea.top:7890','wait': 7.0,'lua_source': log_lua})
    def parse(self, response):
        user_id = re.findall('"profilePage_([0-9]+)"', str(response.body), re.S)[0]
        the_sharedData = re.search(r"(window._sharedData = {.+};)</script>",str(response.body))
        doc = pq(str(response.body))
        items = doc('script[type="text/javascript"]').items()
        for item in items:
            if item.text().strip().startswith('window._sharedData'):
                print(111)
                js_data = json.loads(item.text()[21:-1], encoding='utf-8')
                user = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]
                id = user['id']
                username = user['username']
                fullname = user['full_name']
                intro = user['biography']
                following_count = user['edge_follow']['count']
                followed_count = user['edge_followed_by']['count']
                post_count = user['edge_owner_to_timeline_media']['count']

                # table_user.update_one({'id': id}, {'$set': {
                #     'id':id,
                #     'username':username,
                #     'fullname':fullname,
                #     'intro':intro,
                #     'following_count':following_count,
                #     'followed_count':followed_count,
                #     'post_count':post_count
                # }}, True)

                # print(js_data)
                # time.sleep(1000)
                edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
                page_info = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]['page_info']
                cursor = page_info['end_cursor']
                flag = page_info['has_next_page']
                for edge in edges:
                    post_id = edge['node']['id']
                    post_time = edge['node']['taken_at_timestamp']
                    post_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(post_time))
                    comment_count = edge['node']['edge_media_to_comment']['count']
                    like_count = edge['node']['edge_media_preview_like']['count']
                    urls = []
                    if edge['node']['display_url']:
                        display_url = edge['node']['display_url']
                        print(display_url)
                        urls.append(display_url)
                    urls = ';'.join(urls)
                    # table_post.update_one({'post_id': post_id}, {'$set': {
                    #     'user_id': id,
                    #     'user_name':username,
                    #     'post_id':post_id,
                    #     'time': post_time,
                    #     'comment_count': comment_count,
                    #     'like_count': like_count,
                    #     'img_urls': urls
                    # }}, True)
                    print({
                        'user_id': id,
                        'user_name': username,
                        'post_id': post_id,
                        'time': post_time,
                        'comment_count': comment_count,
                        'like_count': like_count,
                        'img_urls': urls
                    })
                # print(cursor, flag)
        while flag:
            url = uri.format(user_id=user_id, cursor=cursor)
            js_data = self.get_json(url)
            infos = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
            cursor = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            flag = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
            for edge in infos:
                # print('\n\n\n\n',edge)
                post_id = edge['node']['id']
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
                #     'img_urls': urls
                # }}, True)
                print({
                    'user_id': id,
                    'user_name': username,
                    'post_id': post_id,
                    'time': post_time,
                    'comment_count': comment_count,
                    'like_count': like_count,
                    'img_urls': urls
                })
            the_file = open("../data/"+str(response.url).split(r"/")[3]+"_shared_data.json","w")
            the_file.write(the_sharedData.group(1))
            the_file.close()
            header_doc = pq(response.body,parser="html")

    # splash
    def parse_splash(self, response):
        #value = response.xpath('//a[@class="Jv7Aj"]//text()').extract()
        dict = pq(str(response.body))
        index_data["username"] = dict("div.nZSzR h2").text()
        index_data["userheadimg"] = dict(".RR-M- img").attr("src")
        index_data["num_tiezi"] = dict("span span.g47SY").text()
        index_data["num_followers"] = dict("span.g47SY[title]").text()
        index_data["num_following"] = dict("li:nth-of-type(3) span").text()
        index_data["if_verity"] = 1 if dict("span.mTLOB") else 0
        index_data["profile_text"] = dict(".-vDIg > span").text()
        index_data["profile_link"] = dict("a.yLUwa").text()
        index_data["profile_flashing"] = dict("div.ekfSF")
        index_data["profile_full_tie"] = dict("div.Nnq7C")
        index_data["flashing_names"]=list()
        temp_flashing_names = index_data["profile_flashing"].find("div.eXle2").items()
        for item in temp_flashing_names:
            print(item)
            flashing_name = item.text()
            index_data["flashing_names"].append(flashing_name)
        index_data["tie_infos"]=[]
        for item in index_data["profile_full_tie"].items():
            tie_sec_divs = item.find("div.v1Nh3")
            for sec_item in tie_sec_divs.items():
                tie_link = sec_item.find("a").attr("href")
                tie_content = sec_item.find("img").attr("alt")
                tie_imgurl = sec_item.find("img").attr("src")
                #yield SplashRequest(url=url,callback = self.parse_splash,endpoint='execute',args={"proxy": 'http://sovea.top:7890','wait': 7.0,'lua_source': log_lua})
                index_data["tie_infos"].append([tie_link,tie_content,tie_imgurl])
        the_file = open("../data/"+str(response.url).split(r"/")[3]+"_splash_data.json","w")
        the_file.write(str(index_data))
        the_file.close()
        #print(index_data)

