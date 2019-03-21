#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Jerry'
from queue import Queue

class UrlManager:

    def __init__(self):
        self.brand_url_queue = Queue()
        self.post_list_url_queue = Queue()
        self.post_detail_url_queue = Queue()


    def add_brand_url(self,url):
        if url is None or len(url) == 0:
            return
        if type(url) == str:
            self.brand_url_queue.put(url)
        if type(url) == list:
            for i in url:
                self.brand_url_queue.put(i)
        # self.brand_url_queue.task_done()

    def add_list_url(self, url):
        if url is None or len(url) == 0:
            return
        if type(url) == str:
            self.post_list_url_queue.put(url)
        if type(url) == list:
            for i in url:
                self.post_list_url_queue.put(i)

    def add_detail_url(self, url):
        if url is None or len(url) == 0:
            return
        if type(url) == str:
            self.post_detail_url_queue.put(url)
        if type(url) == list:
            for i in url:
                self.post_detail_url_queue.put(i)

    def get_brand_url(self):
        brand_url = self.brand_url_queue.get()
        return brand_url

    def get_list_url(self):
        list_url = self.post_list_url_queue.get()
        return list_url

    def get_detail_url(self):
        detail_url = self.post_detail_url_queue.get()
        return detail_url

