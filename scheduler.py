#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Jerry'
import threading
import time
import asyncio
from HtmlParser import HtmlParser
from HtmlDloader import TitautoSpider
from UrlManager import UrlManager
from DataSave import DataSave


class scheduler:

    def __init__(self):
        self.spider = TitautoSpider()
        self.parser = HtmlParser()
        self.manager = UrlManager()

    def put_brand_url(self, url):
        """
        获取品牌url，添加到url管理器的队列里
        :param url:
        :return:
        """
        res = self.spider.visit_brandforumlist_html(url) #访问品牌列表页
        brand_urls = self.parser.get_brand_urls(res) #解析品牌列表页，获得品牌的url
        self.manager.add_brand_url(brand_urls) #把品牌的url加入队列

    def put_brand_list_response(self):
        size =  self.manager.brand_url_queue.qsize()
        print("brand_url数量", size)
        flag = True
        while flag:
            brand_url = self.manager.brand_url_queue.get()  # 向url管理器请求url
            self.spider.visit_brandforumlist_by_tree(brand_url)  # 访问某个品牌车型页面,并把response加入队列
            self.put_list_url()
            is_empty = self.manager.brand_url_queue.empty()
            if is_empty:
                flag = False

    def put_list_url(self):
        """
        获取车型列表页url，加入队列
        :return:
        """
        size = self.spider.brand_list_response_queue.qsize()
        print("车型数量：",size)
        flag = True
        while flag:
            res = self.spider.brand_list_response_queue.get()
            post_list_urls = self.parser.get_post_list_urls(res) #解析品牌车型页面，获得帖子列表url
            self.manager.add_list_url(post_list_urls) #把帖子列表url添加到队列
            self.put_detail_page_response()
            is_empty = self.spider.brand_list_response_queue.empty()
            if is_empty:
                flag = False

    def put_detail_page_response(self):
        """
        获取详情页的response，加入队列
        :return:
        """
        size = self.manager.post_list_url_queue.qsize()
        print("post_list_url数量", size)
        flag = True
        while flag:
            post_list_url = self.manager.post_list_url_queue.get() #向url管理器请求帖子列表页url
            res = self.spider.visit_essential_posts_list_page(post_list_url) #拼接精品帖子列表页url，发送请求
            try:
                if res is not None:
                    post_detail_url, titles = self.parser.get_essential_posts_detail_url(res) #获得前十个精品帖子的url,以及帖子的标题
                    if post_detail_url is None:
                        return
                    else:
                        for index,url in enumerate(post_detail_url):
                            self.spider.visit_essential_posts_detail_page(post_list_url, url, titles[index]) #访问精华帖详情页
                            self.parse_html()
            except BaseException as f:
                print(f, 'put_detail_page_response')
            is_empty = self.manager.post_list_url_queue.empty()
            if is_empty:
                flag = False

    def parse_html(self):
        """
        解析详情页
        :return:
        """
        size = self.spider.response_queue.qsize()
        # data_save = DataSave()
        flag = True
        while flag:
            response_title = self.spider.response_queue.get()
            title = list(response_title)[0]
            res = list(response_title.values())[0]
            data = self.parser.get_items(res, title)
            # if data is not None:
            #     data_save.insert_data(data)#写入数据库
            is_empty = self.spider.response_queue.empty()
            if is_empty:
                flag = False
        print("已爬取记录{}条".format(self.parser.items_count))

    # def main(self):
    #     self.put_brand_list_response()
    #     self.put_list_url()
    #     self.put_detail_page_response()
    #     self.parse_html()


if __name__ == '__main__':
    run = scheduler()
    start_time = time.time()
    fist_url = 'http://baa.bitauto.com/foruminterrelated/brandforumlist.html'
    run.put_brand_url(url=fist_url)
    tasks = []
    for i in range(25):
        task = threading.Thread(target=run.put_brand_list_response())
        tasks.append(task)
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()
    end_time = time.time()
    print("总耗时:",end_time-start_time)