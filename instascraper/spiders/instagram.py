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
            #yield scrapy.Request(url,cookies=cookies,meta={'proxy': 'http://127.0.0.1:7890'}, callback=self.parse,encoding='utf-8')
            yield SplashRequest(url=url,callback = self.parse_splash,endpoint='execute',args={"proxy": 'http://sovea.top:7890','wait': 7.0,'lua_source': log_lua})
    def parse(self, response):
        the_sharedData = re.search(r"(window._sharedData = {.+};)</script>",str(response.body))
        the_file = open(str(response.url).split(r"/")[3]+"_shared_data.json","w")
        the_file.write(the_sharedData.group(1))
        the_file.close()
        header_doc = pq(response.body,parser="html")

    # splash
    def parse_splash(self, response):
        #value = response.xpath('//a[@class="Jv7Aj"]//text()').extract()
        dict = pq(str(response.body))
        index_data["username"] = dict("div.nZSzR h2").text()
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
                index_data["tie_infos"].append([tie_link,tie_content,tie_imgurl])
        the_file = open(str(response.url).split(r"/")[3]+"_splash_data.json","w")
        the_file.write(index_data)
        the_file.close()
        #print(index_data)

