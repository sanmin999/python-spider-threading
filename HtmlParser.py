#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Jerry'
import re
from lxml import etree
from queue import Queue


class HtmlParser:

    def __init__(self):
        self.items_count = 0

    def get_brand_urls(self,res):
        """
        获取所有品牌的url
        :param res:
        :return:
        """
        tree = etree.HTML(res)
        urls = tree.xpath('//*[@id="treeList"]/ul//li/ul/li/a/@href')
        print(urls)
        print(len(urls))
        return urls

    def get_post_list_urls(self,res):
        """
        获取某个品牌下面具体车型帖子列表页的url
        :param res:
        :return:
        """
        tree = etree.HTML(res)
        roots = tree.xpath('//*[@id="div_result"]/div/div/div/a/@href')
        url_list = []
        for root in roots:
            url = 'http://baa.bitauto.com' + root
            url_list.append(url)
            print(url)
        return url_list

    def get_essential_posts_detail_url(self, res):
        """
        根据div的数量，判断有几个精华帖
        :param res:
        :return:
        """
        try :
            tree = etree.HTML(res)
            div = tree.xpath('//*[@id="divTopicList"]/div')
            flag = len(div)
            post_detail_urls = []
            if flag <= 2:
                return
            elif flag <= 12:
                for i in range(3,flag+1):
                    url = tree.xpath(f'//*[@id="divTopicList"]/div[{i}]/ul[1]/li[2]/a/@href')[0]
                    post_detail_urls.append(url)
                titles = tree.xpath('//div[@class="postslist_xh"]/ul/li[2]/a/@title')
            else:
                for i in range(3,13):
                    url = tree.xpath(f'//*[@id="divTopicList"]/div[{i}]/ul[1]/li[2]/a/@href')[0]
                    post_detail_urls.append(url)
                titles = tree.xpath('//div[@class="postslist_xh"]/ul/li[2]/a/@title')
            return post_detail_urls, titles
        except BaseException as f:
            print(f,'get_essential_posts_detail_url')

    def get_items(self,res, title):
        try:
            tree = etree.HTML(res)
            author = (tree.xpath('//*[@id="postleft1"]/div[1]/a/text()')[0]).strip()
            title = title
            # text = (tree.xpath('//div[@class="post_text post_text_sl"]/div[@class="post_width"]//*/text()')[0]).strip()
            text = (tree.xpath('string(//div[@class="post_text post_text_sl"]/div[@class="post_width"])')).strip()
            time = re.search('<span role="postTime">发表于(.*?)</span>', res).group(1)
            print("作者:",author)
            print("发表时间:",time)
            print("标题:",title)
            print("文本内容:",text)
            content = {
            "作者": author,
            "发表时间": time,
            "标题": title,
            "文本内容":text,
            }
            self.items_count +=1
            return content
        except BaseException as f:
            print(f, 'get_items')
