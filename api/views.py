import json

from django.shortcuts import HttpResponse
from pymongo import Connection
from django.contrib.auth.decorators import login_required
from bson.objectid import ObjectId
import bson
from dict2xml import dict2xml
from my_auth.decorators import user_verified
from func_box import *


# connect the database
conn = Connection()
db = conn.igemdata_new


# @login_required
# @group_authenticated
def add_node(request):
    if request.method == "POST":
        '''
            add a node id collection <node>
            request.POST is all information of the node
        '''
        if validate_node(request.POST['info']) and request.POST['group'] in [g.name for g in request.user.groups.all()]:
            # all the information is valid(including the group)
            node_id = db.node.insert(request.POST['info'])
            noderef_id = db.node_ref.insert(
                {'owner': request.POST['group'], 'x': request.POST['x'], 'y': request.POST['y']})

            # fail to insert into database
            if not node_id or not noderef_id:
                return HttpResponse("{'status':'error', 'reason':'insert failed'}")

            # add refs between two records
            db.node.update({'_id': node_id}, {'$push': {'refs': noderef_id}})
            db.node_ref.update({'_id': noderef_id}, {'$set': {'owner': request.POST['group'], 'node_id': node_id}})

            # return the _id of this user's own record of this node
            return HttpResponse({'ref_id': str(noderef_id)})

        elif request.POST['group'] not in request.user.groups:
            # the group info is not correct
            return HttpResponse("{'status':'error', 'reason':'group info incorrect'}")
        else:
            # node info is incorrect
            return HttpResponse("{'status':'error', 'reason':'node info invalid'}")

    else:
        # not using method POST
        return HttpResponse("{'status':'error', 'reason':'pls use method POST'}")


# @group_authenticated
@user_verified
def get_del_addref_node(request, **kwargs):
    if request.method == 'DELETE':
        '''
            DELETE A REF IN COLLECTION<node_ref>
        '''

        noderef = db.node_ref.find_one({'_id': ObjectId(kwargs['id'])})

        # not found
        if noderef == None:
            return HttpResponse("{'status':'error', 'reason':'no record match that id'}")

        # remove ref in specific node record
        db.node.update({'_id': noderef['node_id']}, {'$pull', {"node_refs", noderef['_id']}})

        # remove node_ref record
        db.node_ref.remove({'_id': noderef['_id']})

        return HttpResponse("{'status': 'success'}")

    elif request.method == 'PUT':
        '''
            add a ref record in collection <node_ref>
        '''
        try:
            node = db.node.find_one({'_id': ObjectId(kwargs['id'])})
        except KeyError:
            return HttpResponse("{'status':'error', 'reason':'key <_id> does not exist'}")

        # not found
        if node == None:
            return HttpResponse("{'status':'error', 'reason':'object not found'}")

        # node exists
        noderef_id = db.node_ref.insert({'owner': request.POST['group'], 'x': request.POST['x'],
                                         'y': request.POST['y'], 'node_id': node['_id']})

        return HttpResponse("{'status': 'success'}")

    elif request.method == 'GET':
        '''
        get the detail info of a record
        '''
        try:
            node = db.node.find_one({'_id': ObjectId(kwargs['id'])})
        except KeyError:
            return HttpResponse("{'status':'error', 'reason':'key <_id> does not exist'}")

        if node == None:
            # not found
            return HttpResponse("{'status':'error', 'reason':'object not found'}")

        else:
            # the node exists
            node_dic = node
            for key in node_dic.keys():
                if isinstance(node_dic[key], bson.objectid.ObjectId):
                    node_dic[key] = str(node_dic[key])
                if isinstance(node_dic[key], list) and isinstance(node_dic[key][0], ObjectId):
                    newrefs = []
                    for refid in node_dic[key]:
                        newrefs.append(str(refid))
                    node_dic[key] = newrefs

            return HttpResponse(json.dumps(node_dic))
    # TODO: add PATCH
    else:
        # method incorrect
        return HttpResponse("{'status': 'error','reason':'pls use method DELETE/PUT '}")


# @login_required
def search_json_node(request, **kwargs):
    if request.method == 'POST':
        ''' POST: {
            'spec': <json query>,
            'fields': <filter in json format>,
            'skip': <INTEGER>,
            'limit': <the max amount to return(INTEGER)>
        }
        '''

        # try if query conform to JSON format
        try:
            queryinstance = json.loads(request.POST['spec'])
        except ValueError:
            return HttpResponse("{'status':'error', 'reason':'query not conform to JSON format'}")

        try:
            filterinstance = json.loads(request.POST['fields'])
        except KeyError:
            # set a default value
            filterinstance = {'_id': 1, 'NAME': 1, 'TYPE': 1}
        except ValueError:
            return HttpResponse("{'status':'error', 'reason':'filter not conform to JSON format'}")

        try:
            limit = int(request.POST['limit'])
            skip = int(request.POST['skip'])
        except KeyError:
            # set a default value
            limit = 20
            skip = 0
        except ValueError:
            return HttpResponse("{'status':'error', 'reason':'limit/skip must be a integer'}")

        # handle _id (string-->ObjectId)

        for key in queryinstance.keys():
            if '_id' == key:
                queryinstance[key] = ObjectId(queryinstance[key])
                continue
            if isinstance(queryinstance[key], list):
                new = []
                for item in queryinstance[key]:
                    if '_id' in item.keys():
                        item['_id'] = ObjectId(item['_id'])
                    new.append(item)
                queryinstance[key] = new

        # vague search
        # for key in queryinstance.keys():
        #     if key == 'NAME' or key == "TYPE":
        #         queryinstance[key] = {"$regex": queryinstance[key]}
        results = db.node.find(queryinstance, filterinstance).limit(limit)



        if 'format' in request.POST.keys():
            if request.POST['format'] == 'xml':
                # Pack data into xml format
                lists = []
                for item in results:
                    newitem = {}
                    for key in item.keys():
                        newitem[key] = item[key]
                    lists.append(newitem)
                inss = {}
                inss['result'] = lists
                final = {}
                final['results'] = inss
                data = dict2xml(final)
        else:
            results_data = []
            for result in results:
                for key in result.keys():
                    if isinstance(result[key], bson.objectid.ObjectId):
                        result[key] = str(result[key])
                    if isinstance(result[key], list) and isinstance(result[key][0], ObjectId):
                        newrefs = []
                        for refid in result[key]:
                            newrefs.append(str(refid))
                        result[key] = newrefs
                results_data.append(result)

            data = json.dumps({'result': results_data})

        return HttpResponse(data)

    else:
        # method is not POST
        return HttpResponse("{'status':'error', 'reason':'pls use POST method'}")


# @login_required
# @group_authenticated
def add_link(request):
    if request.method == "POST":
        # request.POST is all information of the link
        if validate_link(request.POST['info']) and request.POST['group'] in [g.name for g in request.user.groups.all()]:
            # all the information is valid(including the group)
            link_id = db.link.insert(request.POST['info'])
            linkref_id = db.link_ref.insert({'owner': request.POST['group']})

            # fail to insert into database
            if not link_id or not linkref_id:
                return HttpResponse("{'status':'error', 'reason':'insert failed'}")

            # add refs between two records
            db.link.update({'_id': link_id}, {'$push': {'refs': linkref_id}})
            db.link_ref.update({'_id': linkref_id}, {'$set': {'owner': request.POST['group'], 'link_id': link_id,
                                                              'id1': ObjectId(request.POST['id1']),
                                                              'id2': ObjectId(request.POST['id2'])}})

            # return the _id of this user's own record of this link
            return HttpResponse({'ref_id': str(linkref_id)})

        elif request.POST['group'] not in request.user.groups:
            # the group info is not correct
            return HttpResponse("{'status':'error', 'reason':'group info incorrect'}")
        else:
            # link info is incorrect
            return HttpResponse("{'status':'error', 'reason':'link info invalid'}")

    else:
        # method is not POST
        return HttpResponse("{'status':'error', 'reason':'pls use POST method'}")


# @login_required
# @group_authenticated
def get_del_addref_link(request, **kwargs):
    if request.method == 'DELETE':
        '''
            DELETE A REF IN COLLECTION<link_ref>
        '''

        linkref = db.link_ref.find_one({'_id': ObjectId(kwargs['id'])})

        # not found
        if linkref == None:
            return HttpResponse("{'status':'error', 'reason':'no record match that id'}")

        # remove ref in specific node record
        db.link.update({'_id': linkref['link_id']}, {'$pull', {"link_refs", linkref['_id']}})

        # remove node_ref record
        db.link_ref.remove({'_id': linkref['_id']})

        return HttpResponse("{'status': 'success'}")

    elif request.method == 'PUT':
        '''
            add a ref record in collection <node_ref>
        '''
        try:
            link = db.link.find_one({'_id': ObjectId(kwargs['id'])})
        except KeyError:
            return HttpResponse("{'status':'error', 'reason':'key <_id> does not exist'}")

        # not found
        if link == None:
            return HttpResponse("{'status':'error', 'reason':'object not found'}")

        # link exists
        db.link_ref.insert({'owner': request.POST['group'], 'link_id': request.POST['_id'],
                            'id1': ObjectId(request.POST['id1']),
                            'id2': ObjectId(request.POST['id2'])}
        )

        return HttpResponse("{'status': 'success'}")

    elif request.method == 'GET':
        '''
        get the detail info of a record
        '''
        try:
            link = db.link.find_one({'_id': ObjectId(kwargs['id'])})
        except KeyError:
            return HttpResponse("{'status':'error', 'reason':'key <_id> does not exist'}")

        if link == None:
            # not found
            return HttpResponse("{'status':'error', 'reason':'object not found'}")

        else:
            # the node exists
            link_dic = link
            for key in link_dic.keys():
                if isinstance(link_dic[key], bson.objectid.ObjectId):
                    link_dic[key] = str(link_dic[key])
                if isinstance(link_dic[key], list) and isinstance(link_dic[key][0], ObjectId):
                    newrefs = []
                    for refid in link_dic[key]:
                        newrefs.append(str(refid))
                    link_dic[key] = newrefs

            return HttpResponse(json.dumps(link_dic))

    else:
        # method incorrect
        return HttpResponse("{'status': 'error','reason':'pls use method DELETE/PUT '}")


# @login_required
def search_json_link(request, **kwargs):
    if request.method == 'POST':
        ''' POST: {
            'spec': <json query>,
            'fields': <filter in json format>,
            'skip': <INTEGER>,
            'limit': <the max amount to return(INTEGER)>
        }
        '''

        # try if query conform to JSON format
        try:
            queryinstance = json.loads(request.POST['spec'])
        except ValueError:
            return HttpResponse("{'status':'error', 'reason':'query not conform to JSON format'}")

        try:
            filterinstance = json.loads(request.POST['fields'])
        except KeyError:
            # set a default value
            filterinstance = {'TYPE1': 1, 'TYPE2': 1, '_id': 1}
        except ValueError:
            return HttpResponse("{'status':'error', 'reason':'filter not conform to JSON format'}")

        try:
            limit = int(request.POST['limit'])
            skip = int(request.POST['skip'])
        except KeyError:
            # set a default value
            limit = 20
            skip = 0
        except ValueError:
            return HttpResponse("{'status':'error', 'reason':'limit must be a integer'}")

        # handle _id (string-->ObjectId)

        for key in queryinstance.keys():
            if '_id' == key:
                queryinstance[key] = ObjectId(queryinstance[key])
                continue
            if isinstance(queryinstance[key], list):
                new = []
                for item in queryinstance[key]:
                    if '_id' in item.keys():
                        item['_id'] = ObjectId(item['_id'])
                    new.append(item)
                queryinstance[key] = new

        # vague search
        # for key in queryinstance.keys():
        #     if key in ['NAME', 'TYPE']:
        #         queryinstance[key] = {"$regex": queryinstance[key]}
        results = db.link.find(queryinstance, filterinstance).limit(limit)


        if 'format' in request.POST.keys():
            if request.POST['format'] == 'xml':
                # Pack data into xml format
                lists = []
                for item in results:
                    newitem = {}
                    for key in item.keys():
                        newitem[key] = item[key]
                    lists.append(newitem)
                inss = {}
                inss['result'] = lists
                final = {}
                final['results'] = inss
                data = dict2xml(final)
        else:
            results_data = []
            for result in results:
                for key in result.keys():
                    if isinstance(result[key], bson.objectid.ObjectId):
                        result[key] = str(result[key])
                    if isinstance(result[key], list) and isinstance(result[key][0], ObjectId):
                        newrefs = []
                        for refid in result[key]:
                            newrefs.append(str(refid))
                        result[key] = newrefs
                results_data.append(result)
            data = json.dumps({'result': results_data})

        return HttpResponse(data)

    else:
        # method is not POST
        return HttpResponse("{'status':'error', 'reason':'pls use POST method'}")


