import pymongo
import numpy as np
import matplotlib as plt

client = pymongo.MongoClient('localhost', 27017)
douban = client['douban']
movie_info = douban['movie_info']

for i in movie_info.find({}, {'movie_classify': 1, '_id': 0, 'movie_id': 1}).limit(10):
    print(i)


# visiable
def plot_show():
    data = movie_info.find({}, {'movie_classify': 1, '_id': 0, 'movie_id': 1})
