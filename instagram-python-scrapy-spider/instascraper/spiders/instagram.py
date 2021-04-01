# -*- coding: utf-8 -*-
import scrapy
# import scrapy.selector as Selector
from urllib.parse import urlencode
import json
from datetime import datetime
from pyquery import PyQuery as pq
from scrapy_splash import SplashRequest
import re
API = 'beb596fbecce7ef15125ad7128bccb1b'
user_accounts = ["marvel","nba","dancingastro"] 
cookies = {
    "ig_did":'',
    "mid":'',
    "ig_nrcb":'1',
    "shbid":"",
    "csrftoken":"",
    "ds_user_id":"",
    "sessionid":"",
    "shbts":"",
    "rur":"ATN"
}
log_lua = '''
function main(splash, args)
    -- 自定义请求头
    splash:set_custom_headers({
        ["Cookie"] = ""
    })
    assert(splash:go(args.url))
    assert(splash:wait(3))
    return {
        html = splash:html(),
    }
end
'''
def get_url(url):
    payload = {'api_key': API, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['api.scraperapi.com',"www.instagram.com"]
    custom_settings = {'CONCURRENT_REQUESTS_PER_DOMAIN': 5}

    def start_requests(self):
        for username in user_accounts:
            url = f'https://www.instagram.com/{username}'
            yield scrapy.Request(url,cookies=cookies,meta={'proxy': 'http://127.0.0.1:7890'}, callback=self.parse,encoding='utf-8')
            #yield SplashRequest(url=url,cookies=cookies,callback = self.parse,endpoint='execute',args={'wait': 3.0,'lua_source': log_lua})
    def parse(self, response):
        the_sharedData = re.search(r"(window._sharedData = {.+};)</script>",str(response.body))
        the_file = open(str(response.url).split(r"/")[3]+"_shared_data.json","w")
        the_file.write(the_sharedData.group(1))
        the_file.close()
        
        header_doc = pq(response.body,parser="html")
        data_feature = dict()
        # splash
#    def parse_pages(self, response):

