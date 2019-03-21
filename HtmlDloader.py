#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Jerry'
import requests
from queue import Queue
from GetProxy import get_ip

class TitautoSpider:

    def __init__(self):
        # self.session = requests.session()
        self.brand_list_response_queue = Queue()
        self.response_queue = Queue()

    def visit_brandforumlist_html(self, url):
        """
        访问汽车品牌列表页,就一个请求不需要代理IP
        :param url:
        :return:
        """
        headers = {
            'Host':'baa.bitauto.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text

    def visit_brandforumlist_by_tree(self, url):
        """
        访问某个品牌的车型列表页，请求失败则使用代理ip重新访问
        :param url:
        :return:
        """
        session = requests.session()
        headers = {
            'Host': 'baa.bitauto.com',
            'connection':'close',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9'
        }
        try:
            response = session.get(url,headers=headers, timeout=5)
            if response.status_code == 200:
                self.brand_list_response_queue.put(response.text)
                print("访问车型列表页成功",url)
            else:
                ip = get_ip()
                session.proxies = {
                    'http': 'http://' + ip
                }
                response = session.get(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    self.brand_list_response_queue.put(response.text)
                else:
                    print(response.status_code)
        except BaseException as f:
            print(f,'visit_brandforumlist_by_tree')

    def visit_essential_posts_list_page(self, url):
        """
        访问某个车型精华评论列表页，请求失败则使用代理ip重新访问
        :param url:
        :return:
        """
        session = requests.session()
        if url is not None:
            headers = {
                'Host':'baa.bitauto.com',
                'connection': 'close',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer':url,
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.9'
            }
            full_url = url + 'index-0-all-1-0.html'
            try:
                response = session.get(full_url, headers=headers, timeout=5)
                # print(response.status_code)
                if response.status_code == 200:
                    print("访问评论列表页成功")
                    return response.text
                else:
                    ip = get_ip()
                    session.proxies = {
                        'http': 'http://' + ip
                    }
                    response = session.get(full_url, headers=headers, timeout=5)
                    if response.status_code == 200:
                        return response.text
                    else:
                        print(response.status_code)
            except BaseException as f:
                print(f,'visit_essential_posts_list_page')

    def visit_essential_posts_detail_page(self, ref, url, title=None):
        """
        访问精华评论详情页,请求失败则使用代理ip重新访问
        :param ref:
        :param url:
        :return:
        """
        session = requests.session()
        headers = {
            'Host':'baa.bitauto.com',
            'connection': 'close',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Referer':ref,
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9'
        }
        try:
            response = session.get(url, headers=headers, timeout=5)
            response_title = {}
            if response.status_code == 200:
                print("访问精华评论详情页成功")
                response_title[title] = response.text
                self.response_queue.put(response_title)
            else:
                ip = get_ip()
                session.proxies = {
                    'http': 'http://' + ip
                }
                response = session.get(url, headers=headers, timeout=5)
                response_title[title] = response.text
                self.response_queue.put(response_title)
        except BaseException as f:
            print(f,'visit_essential_posts_detail_page')
            pass
