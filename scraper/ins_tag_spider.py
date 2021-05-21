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
from pyquery import PyQuery as pq, text
from urllib.parse import urlencode

url_base = 'https://www.instagram.com/explore/tags/{}/'
default_url = 'https://www.instagram.com/explore/tags/{}/?__a=1'
query_url = 'https://i.instagram.com/api/v1/tags/{}/sections/'

proxies = {
    'http': 'https://127.0.0.1:7890',
    'https': 'https://127.0.0.1:7890',
}
raw_headers = {
    'authority': 'www.instagram.com',
    'scheme': 'https',
    'referer': 'https://www.instagram.com',
    'origin': 'https://www.instagram.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}
query_headers = {
    'authority': 'i.instagram.com',
    'method': 'POST',
    'scheme': 'https',
    'cookie': 'mid=YKShiwALAAH-bCUFDLxplWFX13xB; ig_did=11C8C4EF-4381-4E58-9D6B-EC267CE500FA; ig_nrcb=1; csrftoken=IeFa5klhRRFf498J4CarG4oB1Je0Vx4e; ds_user_id=48046266403; sessionid=48046266403%3AGPp9TtvX8aZic7%3A24; rur=NAO; ig_lang=zh-tw',
    'referer': 'https://www.instagram.com/',
    'origin': 'https://www.instagram.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'x-csrftoken': 'IeFa5klhRRFf498J4CarG4oB1Je0Vx4e',
    'x-ig-app-id': '936619743392459',
    'x-ig-www-claim': 'hmac.AR163B6Z0ZAkXIrcMEqOl0JN4AWpGzQLiY07owJSJYxzqZPE',
    'x-requested-with': 'XMLHttpRequest',
    'x-instagram-ajax': '52aa6db90924'
}
default_headers = {
    'authority': 'www.instagram.com',
    'scheme': 'https',
    'cookie': 'mid=YKShiwALAAH-bCUFDLxplWFX13xB; ig_did=11C8C4EF-4381-4E58-9D6B-EC267CE500FA; ig_nrcb=1; csrftoken=IeFa5klhRRFf498J4CarG4oB1Je0Vx4e; ds_user_id=48046266403; sessionid=48046266403%3AGPp9TtvX8aZic7%3A24; rur=NAO; ig_lang=zh-tw',
    'referer': 'https://www.instagram.com',
    'origin': 'https://www.instagram.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'x-csrftoken': 'IeFa5klhRRFf498J4CarG4oB1Je0Vx4e',
    'x-ig-app-id': '936619743392459',
    'x-ig-www-claim': 'hmac.AR163B6Z0ZAkXIrcMEqOl0JN4AWpGzQLiY07owJSJYxzqZPE',
    'x-requested-with': 'XMLHttpRequest',
}


def get_more_data(url, data):
    try:
        response = requests.post(
            url, data=data, headers=query_headers, timeout=10, proxies=proxies)
        # print(response.text)
        if response.status_code == 200:
            # print(type(response.json()))
            return response.json()
        else:
            print('请求网页源代码错误, 错误状态码：', response.status_code)
            print(response.text)
    except Exception as e:
        # print(e)
        traceback.print_exc()
        return None


def more_data_handler(data: dict, tag_name):
    if data == None:
        return
    else:
        try:
            next_media_ids = data.get("next_media_ids")
            recent_more_available = data.get("more_available")
            recent_next_max_id = data.get("next_max_id")
            recent_next_page = data.get("next_page")
            recent_data_sections = data.get("sections",[{}])
            #下次请求参数
            print({
                'recent_more_available': recent_more_available,
                'next_media_ids': next_media_ids,
                'recent_next_max_id': recent_next_max_id,
                'recent_next_page': recent_next_page,
            })
            #帖子数据
            for item in recent_data_sections:
                for sub_item in item.get("layout_content", {}).get("medias", [{}]):
                    temp_media = sub_item.get("media", {})
                    # print(type(temp_media))
                    comment_count = temp_media.get("comment_count")
                    like_count = temp_media.get("like_count")
                    timestamp = temp_media.get("taken_at")
                    post_code = temp_media.get("code")
                    caption_text = ""
                    temp_caption = temp_media.get("caption", {})
                    # print(type(temp_caption))
                    # print(temp_caption.keys())
                    caption_text = temp_caption.get("text")
                    user_id = temp_caption.get("user_id")
                    username = temp_caption.get("user", {}).get("username")
                    full_name = temp_caption.get("user", {}).get("full_name")
                    profile_pic_url = temp_caption.get(
                        "user", {}).get("profile_pic_url")
                    carousel_media_count = 1
                    accessibility_caption = []
                    carousel_media_links = []
                    if "carousel_media_count" in temp_media:
                        carousel_media_count = temp_media.get(
                            "carousel_media_count")
                        for carousel_media_item in temp_media.get("carousel_media", [{}]):
                            if carousel_media_item.get("media_type") == 1:
                                accessibility_caption.append(
                                    carousel_media_item.get("accessibility_caption"))
                                carousel_media_links.append(
                                    carousel_media_item.get("image_versions2", {}).get(
                                        "candidates", [{}])[0].get("url")
                                )
                            elif carousel_media_item.get("media_type") == 2:
                                carousel_media_links.append(
                                    carousel_media_item.get("video_versions", [{}])[
                                        0].get("url")
                                )
                    else:
                        if temp_media["media_type"] == 1:
                            accessibility_caption.append(
                                temp_media.get("accessibility_caption"))
                            carousel_media_links.append(
                                temp_media.get("image_versions2", {}).get(
                                    "candidates", [{}])[0].get("url")
                            )
                        elif temp_media["media_type"] == 2:
                            carousel_media_links.append(
                                temp_media.get("video_versions", [{}])[
                                    0].get("url")
                            )
                    print({
                        'post_code': post_code,
                        'comment_count': comment_count,
                        'like_count': like_count,
                        'timestamp': timestamp,
                        'caption_text': caption_text,
                        'user_id': user_id,
                        'username': username,
                        'full_name': full_name,
                        'profile_pic_url': profile_pic_url,
                        'carousel_media_count': carousel_media_count,
                        'accessibility_caption': accessibility_caption,
                        'carousel_media_links': carousel_media_links,
                    })
                    print("")
            if recent_more_available == True:
                new_query_data = {}
                new_query_data = {
                    'include_persistent': 0,
                    'max_id': recent_next_max_id,
                    'page': recent_next_page,
                    'next_media_ids[]': next_media_ids,
                    'surface': 'grid',
                    'tab': 'recent'
                }
                print(new_query_data)
                new_url = query_url.format(tag_name)
                time.sleep(5)
                more_data_handler(get_more_data(
                    new_url, new_query_data), tag_name)

        except Exception as e:
            # print(e)
            traceback.print_exc()


def preview_data_handler(raw_data: dict):
    if raw_data == None:
        return
    else:
        try:
            data = raw_data.get("data", {})
            # print(data)
            tag_name = data.get("name")
            media_count = data.get("media_count")
            recent_data = data.get("recent", {})
            top_data = data.get("top",{})
            recent_more_available = recent_data.get("more_available")
            recent_next_max_id = recent_data.get("next_max_id")
            recent_next_page = recent_data.get("next_page")
            recent_data_sections = recent_data.get("sections", [{}])
            top_more_available = top_data.get("more_available")
            top_next_max_id = top_data.get("next_max_id")
            top_next_page = top_data.get("next_page")
            top_data_sections = top_data.get("sections", [{}])
            top_next_media_ids = top_data.get("next_media_ids", [])
            #参数
            print({
                'tag_name': tag_name,
                'media_count': media_count,
                'recent_more_available': recent_more_available,
                'recent_next_max_id': recent_next_max_id,
                'recent_next_page': recent_next_page,
            })
            #本周热门帖子数据
            for item in top_data_sections:
                for sub_item in item.get("layout_content", {}).get("medias", [{}]):
                    temp_media = sub_item.get("media", {})
                    # print(type(temp_media))
                    comment_count = temp_media.get("comment_count")
                    like_count = temp_media.get("like_count")
                    timestamp = temp_media.get("taken_at")
                    post_code = temp_media.get("code")
                    caption_text = ""
                    temp_caption = temp_media.get("caption", {})
                    # print(type(temp_caption))
                    # print(temp_caption.keys())
                    caption_text = temp_caption.get("text")
                    user_id = temp_caption.get("user_id")
                    username = temp_caption.get("user", {}).get("username")
                    full_name = temp_caption.get("user", {}).get("full_name")
                    profile_pic_url = temp_caption.get(
                        "user", {}).get("profile_pic_url")
                    carousel_media_count = 1
                    accessibility_caption = []
                    carousel_media_links = []
                    if "carousel_media_count" in temp_media:
                        carousel_media_count = temp_media.get(
                            "carousel_media_count")
                        for carousel_media_item in temp_media.get("carousel_media", [{}]):
                            if carousel_media_item.get("media_type") == 1:
                                accessibility_caption.append(
                                    carousel_media_item.get("accessibility_caption"))
                                carousel_media_links.append(
                                    carousel_media_item.get("image_versions2", {}).get(
                                        "candidates", [{}])[0].get("url")
                                )
                            elif carousel_media_item.get("media_type") == 2:
                                carousel_media_links.append(
                                    carousel_media_item.get("video_versions", [{}])[
                                        0].get("url")
                                )
                    else:
                        if temp_media["media_type"] == 1:
                            accessibility_caption.append(
                                temp_media.get("accessibility_caption"))
                            carousel_media_links.append(
                                temp_media.get("image_versions2", {}).get(
                                    "candidates", [{}])[0].get("url")
                            )
                        elif temp_media["media_type"] == 2:
                            carousel_media_links.append(
                                temp_media.get("video_versions", [{}])[
                                    0].get("url")
                            )
                    print({
                        'post_code': post_code,
                        'comment_count': comment_count,
                        'like_count': like_count,
                        'timestamp': timestamp,
                        'caption_text': caption_text,
                        'user_id': user_id,
                        'username': username,
                        'full_name': full_name,
                        'profile_pic_url': profile_pic_url,
                        'carousel_media_count': carousel_media_count,
                        'accessibility_caption': accessibility_caption,
                        'carousel_media_links': carousel_media_links,
                    })
                    print("")
            #最新帖子数据
            for item in recent_data_sections:
                for sub_item in item.get("layout_content", {}).get("medias", [{}]):
                    temp_media = sub_item.get("media", {})
                    # print(type(temp_media))
                    comment_count = temp_media.get("comment_count")
                    like_count = temp_media.get("like_count")
                    timestamp = temp_media.get("taken_at")
                    post_code = temp_media.get("code")
                    caption_text = ""
                    temp_caption = temp_media.get("caption", {})
                    # print(type(temp_caption))
                    # print(temp_caption.keys())
                    caption_text = temp_caption.get("text")
                    user_id = temp_caption.get("user_id")
                    username = temp_caption.get("user", {}).get("username")
                    full_name = temp_caption.get("user", {}).get("full_name")
                    profile_pic_url = temp_caption.get(
                        "user", {}).get("profile_pic_url")
                    carousel_media_count = 1
                    accessibility_caption = []
                    carousel_media_links = []
                    if "carousel_media_count" in temp_media:
                        carousel_media_count = temp_media.get(
                            "carousel_media_count")
                        for carousel_media_item in temp_media.get("carousel_media", [{}]):
                            if carousel_media_item.get("media_type") == 1:
                                accessibility_caption.append(
                                    carousel_media_item.get("accessibility_caption"))
                                carousel_media_links.append(
                                    carousel_media_item.get("image_versions2", {}).get(
                                        "candidates", [{}])[0].get("url")
                                )
                            elif carousel_media_item.get("media_type") == 2:
                                carousel_media_links.append(
                                    carousel_media_item.get("video_versions", [{}])[
                                        0].get("url")
                                )
                    else:
                        if temp_media["media_type"] == 1:
                            accessibility_caption.append(
                                temp_media.get("accessibility_caption"))
                            carousel_media_links.append(
                                temp_media.get("image_versions2", {}).get(
                                    "candidates", [{}])[0].get("url")
                            )
                        elif temp_media["media_type"] == 2:
                            carousel_media_links.append(
                                temp_media.get("video_versions", [{}])[
                                    0].get("url")
                            )
                    print({
                        'post_code': post_code,
                        'comment_count': comment_count,
                        'like_count': like_count,
                        'timestamp': timestamp,
                        'caption_text': caption_text,
                        'user_id': user_id,
                        'username': username,
                        'full_name': full_name,
                        'profile_pic_url': profile_pic_url,
                        'carousel_media_count': carousel_media_count,
                        'accessibility_caption': accessibility_caption,
                        'carousel_media_links': carousel_media_links,
                    })
                    print("")
            if recent_more_available == True:
                new_query_data = {
                    'include_persistent': 0,
                    'max_id': recent_next_max_id,
                    'page': recent_next_page,
                    'surface': 'grid',
                    'tab': 'recent'
                }
                print(new_query_data)
                new_url = query_url.format(tag_name)
                time.sleep(5)
                more_data_handler(get_more_data(
                    new_url, new_query_data), tag_name)
        except Exception as e:
            # print(e)
            traceback.print_exc()


def get_preview_data(url):
    try:
        response = requests.get(
            url, headers=default_headers, timeout=10, proxies=proxies)
        # print(response.text)
        if response.status_code == 200:
            # print(type(response.json()))
            return response.json()
        else:
            print('请求网页源代码错误, 错误状态码：', response.status_code, response.text())
            return None
    except Exception as e:
        print(e)
        traceback.print_exc()
        return None


def main(tag):
    preview_data_handler(get_preview_data(default_url.format(tag)))


if __name__ == '__main__':
    main("香港")
