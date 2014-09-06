__author__ = 'Beibeihome'

from pymongo import *
from django.shortcuts import HttpResponse
import bson
import json


db = MongoClient()['igemdata_new']


def look_around(request, **kwargs):
    if request.method == 'POST':
        ref_id = kwargs['ref_id']
        node_id = db.node_ref.find_one({'_id': bson.ObjectId(ref_id)})
        link_list1 = db.link_ref.find({'id1': bson.ObjectId(node_id)})
        link_list2 = db.link_ref.find({'id2': bson.ObjectId(node_id)})
        dict_list = []

        for link in link_list1:
            dict_one = {}
            dict_one['link_id'] = link['link_id']
            dict_one['node_id'] = link['id2']
            object_node = db.node.find_one({'_id': bson.ObjectId(link['id2'])})
            dict_one['NAME'] = object_node['NAME']
            dict_one['TYPE'] = object_node['TYPE']
            dict_list.append(dict_one)
            del dict_one

        for link in link_list2:
            dict_one = {}
            dict_one['link_id'] = link['link_id']
            dict_one['node_id'] = link['id1']
            object_node = db.node.find_one({'_id': bson.ObjectId(link['id1'])})
            dict_one['NAME'] = object_node['NAME']
            dict_one['TYPE'] = object_node['TYPE']
            dict_list.append(dict_one)
            del dict_one

        result_text = json.dumps(dict_list)
    return HttpResponse(result_text)