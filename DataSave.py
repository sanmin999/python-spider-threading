#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Jerry'
import pymongo

class DataSave:

    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client['test']
        self.collection = self.db['baa']

    def insert_data(self, data):
        content = data
        self.collection.insert(content)

    def close_databases(self):
        self.client.close()
