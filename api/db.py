__author__ = 'feiyicheng'

import json
from pymongo import Connection
from bson.objectid import ObjectId
from dict2xml import dict2xml
from projects.models import Project
from func_box import *


def insert(db, coll_name, data):
    """ insert data into db.<coll_name>
    @param coll_name: string
    @param data: dict
    @return: ObjectId of the new record, otherwise a dict containing reason for the error
    """
    if validate(data):
        obj_id = None
        exec ("obj_id  = db.{0}.insert(data)".format(coll_name))
        if obj_id is None:
            return {'error': 'fail to insert in to database'}
        else:
            return obj_id
    else:
        return {'error': 'data invalid!'}


def add_node(db, data, pid, x=0, y=0):
    """ add_node from data into database

    @param data: dict
    @return: a tuple (<node_id>,<noderef_id>) <node_id>,<noderef_id> are all ObjectId
    """
    node_id = insert(db, 'node', data)
    if isinstance(node_id, dict):
        return node_id
    ref_data = {
        'pid': int(pid),
        'x': float(x),
        'y': float(y),
    }
    noderef_id = insert(db, 'node_ref', ref_data)
    if isinstance(noderef_id, dict):
        return noderef_id

    prj = db.project.find_one({'pid': int(pid)})
    if prj is None:
        # prj does not exist
        insert(db, 'project', {'pid': int(pid), 'node': [], 'link': []})
        prj = db.project.find_one({'pid': int(pid)})
    db.project.update({'_id': prj['_id']}, {'$push': {'node': noderef_id}}, True)

    db.node.update({'_id': node_id}, {'$push': {'refs': noderef_id}}, True)
    db.node_ref.update({'_id': noderef_id}, {'$set': {'node_id': node_id}})

    return node_id, noderef_id


def add_link(db, data, pid, id1, id2):
    """ add link from data into database

    @param data: dict
    @para id1,id2: string
    @return: a tuple (<link_id>,<linkref_id>) <link_id>,<linkref_id> are all ObjectId
    """
    link_id = insert(db, 'link', data)
    if isinstance(link_id, dict):
        return link_id
    ref_data = {
        'pid': int(pid)
    }
    linkref_id = insert(db, 'link_ref', ref_data)
    if isinstance(linkref_id, dict):
        return linkref_id

    prj = db.project.find_one({'pid': int(pid)})
    if prj is None:
        # prj does not exist
        insert(db, 'project', {'pid': int(pid), 'node': [], 'link': []})
        prj = db.project.find_one({'pid': int(pid)})
    db.project.update({'_id': prj['_id']}, {'$push': {'link': linkref_id}}, True)

    db.link.update({'_id': link_id}, {'$push': {'refs': linkref_id}}, True)
    db.link_ref.update({'_id': linkref_id}, {'$set': {'link_id': link_id,
                                                      'id1': ObjectId(id1),
                                                      'id2': ObjectId(id2), }})
    return link_id, linkref_id


def fork_node(db, node_id, pid, x=0, y=0):
    """ make a reference of the node

    @param node_id: string
    @param pid: a int object, a string that can be converted to int is alse OK
    @return: a tuple of ObjectId (<node_id>, <noderef_id>), otherwise a dict with error info
    """
    if not isinstance(node_id, str):
        return {'error': 'node_id must be a string'}
    node = db.node.find_one({'_id': ObjectId(node_id)})
    if node is None:
        return {'error': 'node matching the given id not found'}
    noderef_data = {
        'pid': int(pid),
        'x': float(x),
        'y': float(y),
        'node_id': node['_id']
    }
    noderef_id = insert(db, 'node_ref', noderef_data)
    if isinstance(noderef_id, dict):
        return noderef_id

    prj = db.project.find_one({'pid': int(pid)})
    if prj is None:
        # prj does not exist
        insert(db, 'project', {'pid': int(pid), 'node': [], 'link': []})
        prj = db.project.find_one({'pid': int(pid)})
    db.project.update({'_id': prj['_id']}, {'$push': {'node': noderef_id}}, True)

    db.node.update({'_id': node['_id']}, {'$push': {'refs': noderef_id}}, True)

    return node['_id'], noderef_id


def fork_link(db, node_id, pid, id1, id2):
    """ make a reference of the link

    @param node_id: string
    @param id1, id2: string or ObjectId
    @param pid: a int object, a string that can be converted to int is alse OK
    @return: a tuple of ObjectId (<node_id>, <noderef_id>), otherwise a dict with error info
    """
    #if id1, id2 are ObjectId object, convert to str
    if isinstance(id1, ObjectId):
        id1 = str(id2)
    if isinstance(id2, ObjectId):
        id2 = str(id2)

    # get the link object
    if not isinstance(node_id, str):
        return {'error': 'node_id must be a string'}
    link = db.link.find_one({'_id': ObjectId(node_id)})
    if link is None:
        return {'error': 'link matching the given id not found'}

    # add a ref record to the ref collection
    linkref_data = {
        'pid': int(pid),
        'id1': ObjectId(id1),
        'id2': ObjectId(id2),
        'node_id': link['_id']
    }
    linkref_id = insert(db, 'node_ref', linkref_data)
    if isinstance(linkref_data, dict):
        return linkref_data

    # update references in the project
    prj = db.project.find_one({'pid': int(pid)})
    if prj is None:
        # prj does not exist
        insert(db, 'project', {'pid': int(pid), 'node': [], 'link': []})
        prj = db.project.find_one({'pid': int(pid)})
    db.project.update({'_id': prj['_id']}, {'$push': {'link': linkref_id}}, True)

    # update references in the link record
    db.link.update({'_id': link['_id']}, {'$push': {'refs': linkref_id}}, True)

    return link['_id'], linkref_id









