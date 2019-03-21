#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Jerry'
import time
import requests


def get_ip():
    while True:
        time.sleep(1)
        url = 'http://api3.xiguadaili.com/ip/?tid=557506829707479&num=1'
        response = requests.get(url)
        ip = response.text
        session = requests.session()
        fist_url = 'http://baa.bitauto.com/foruminterrelated/brandforumlist.html'
        session.proxies = {
            'http':'http://'+ip
        }
        headers = {
                    'Host':'baa.bitauto.com',
                    'Upgrade-Insecure-Requests':'1',
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'zh-CN,zh;q=0.9'
                }
        try:
            res = session .get(url=fist_url, headers = headers, timeout=3)
            if res.status_code == 200:
                return ip
        except:
            pass
