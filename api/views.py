from django.shortcuts import HttpResponse
from pymongo import Connection
from django.contrib.auth.decorators import login_required
from decorators import group_authenticated
from func_box import *
from bson.objectid import ObjectId
from dict2xml import dict2xml
import json

# connect the database
conn = Connection()
db = conn.igemdata_new


@login_required
@group_authenticated
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


@login_required
@group_authenticated
def del_or_addref_node(request, **kwargs):
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

    else:
        # method incorrect
        return HttpResponse("{'status': 'error','reason':'pls use method DELETE/PUT '}")


@login_required
def search_json_node(request):
    if request.method == 'POST':
        ''' POST: {
            'query': <json query>,
            'filter': <filter in json format>,
            'limit': <the max amount to return(INTEGER)>
        }
        '''

        # try if query conform to JSON format
        try:
            queryinstance = json.loads(request.POST['query'])
        except ValueError:
            return HttpResponse("{'status':'error', 'reason':'query not conform to JSON format'}")

        try:
            filterinstance = json.loads(request.POST['filter'])
        except KeyError:
            # set a default value
            filterinstance = {'_id': 1, 'NAME': 1, 'TYPE': 1}
        except ValueError:
            return HttpResponse("{'status':'error', 'reason':'filter not conform to JSON format'}")

        try:
            limit = int(request.POST['limit'])
        except KeyError:
            # set a default value
            limit = 20
        except ValueError:
            return HttpResponse("{'status':'error', 'reason':'limit must be a integer'}")

        # vague search
        for key in queryinstance.keys():
            if key == 'NAME' or key == "TYPE":
                queryinstance[key] = {"$regex": queryinstance[key]}
        results = db.node.find(queryinstance, filterinstance).limit(limit)

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

        return HttpResponse(data)

    else:
        # method is not POST
        return HttpResponse("{'status':'error', 'reason':'pls use POST method'}")


@login_required
@group_authenticated
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


@login_required
@group_authenticated
def del_or_addref_link(request, **kwargs):
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

    else:
        # method incorrect
        return HttpResponse("{'status': 'error','reason':'pls use method DELETE/PUT '}")


@login_required
def search_json_link(request):
    if request.method == 'POST':
        ''' POST: {
            'query': <json query>,
            'filter': <filter in json format>,
            'limit': <the max amount to return(INTEGER)>
        }
        '''

        # try if query conform to JSON format
        try:
            queryinstance = json.loads(request.POST['query'])
        except ValueError:
            return HttpResponse("{'status':'error', 'reason':'query not conform to JSON format'}")

        try:
            filterinstance = json.loads(request.POST['query'])
        except KeyError:
            # set a default value
            filterinstance = {'_id': 1, 'NAME': 1, 'TYPE': 1}
        except ValueError:
            return HttpResponse("{'status':'error', 'reason':'filter not conform to JSON format'}")

        try:
            limit = int(request.POST['limit'])
        except KeyError:
            # set a default value
            limit = 20
        except ValueError:
            return HttpResponse("{'status':'error', 'reason':'limit must be a integer'}")


        # vague search
        for key in queryinstance.keys():
            if key in ['NAME', 'TYPE']:
                queryinstance[key] = {"$regex": queryinstance[key]}
        results = db.link.find(queryinstance, filterinstance).limit(limit)

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

        return HttpResponse(data)

    else:
        # method is not POST
        return HttpResponse("{'status':'error', 'reason':'pls use POST method'}")


