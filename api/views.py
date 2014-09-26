import json

from django.shortcuts import HttpResponse
from pymongo import Connection
from bson.objectid import ObjectId
import bson
from dict2xml import dict2xml
from func_box import *
from decorators import project_verified, logged_in, project_verified_exclude_get, logged_in_exclude_get
from projects.models import Project

# connect the database
conn = Connection()
db = conn.igemdata_new


@logged_in
@project_verified
def add_node(request):
    if request.method == "POST":
        '''
            add a node id collection <node>
            request.POST is all information of the node
        '''
        if validate_node(request.POST['info']):
            # all the information is valid(including the group)
            node_id = db.node.insert(request.POST['info'])
            noderef_id = db.node_ref.insert(
                {'pid': int(request.POST['pid']) if 'pid' in request.POST.keys() else 0,
                 'x': request.POST['x'] if 'x' in request.POST.keys() else '0',
                 'y': request.POST['y'] if 'y' in request.POST.keys() else '0',
                }
            )

            # fail to insert into database
            if not node_id or not noderef_id:
                return HttpResponse("{'status':'error', 'reason':'insert failed'}")

            # add refs between two records
            db.node.update({'_id': node_id}, {'$push': {'refs': noderef_id}})
            db.node_ref.update({'_id': noderef_id}, {'$set': {'node_id': node_id}})

            # return the _id of this user's own record of this node
            return HttpResponse({'ref_id': str(noderef_id)})

        else:
            # node info is incorrect
            return HttpResponse("{'status':'error', 'reason':'node info invalid'}")

    else:
        # not using method POST
        return HttpResponse("{'status':'error', 'reason':'pls use method POST'}")


@logged_in_exclude_get
@project_verified_exclude_get
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
        noderef_id = db.node_ref.insert({'pid': int(request.POST['pid']) if 'pid' in request.POST.keys() else 0,
                                         'x': request.POST['x'] if 'x' in request.POST.keys() else '0',
                                         'y': request.POST['y'] if 'y' in request.POST.keys() else '0',
                                         'node_id': node['_id']}
                                        )


        return HttpResponse("{'status': 'success'}")

    elif request.method == 'GET':
        '''
        get the detail info of a record
        :param kwargs: kwargs['_id'] is the object id in collection node
        '''
        BANNED_ATTRI = {'_id': 0, 'REF': 0, 'REF_COUNT': 0, 'ID': 0, 'FATHER': 0, 'CHILD': 0}
        try:
            node = db.node.find_one({'_id': ObjectId(kwargs['id'])}, BANNED_ATTRI)
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
                if isinstance(node_dic[key], list) and len(node_dic[key]) > 0 and isinstance(node_dic[key][0], ObjectId):
                    newrefs = []
                    for refid in node_dic[key]:
                        newrefs.append(str(refid))
                    node_dic[key] = newrefs

            return HttpResponse(json.dumps(node_dic))

    elif request.method == 'PATCH':
        '''
        update merely the position(x,y) of the node
        :param request.PATCH: a dict with keys(token, username, info), info is also a dict with keys(x, y, ref_id)
        :return data: {'status': 'success'} if everything goes right
        '''
        try:
            info = request.PATCH['info']
        except KeyError:
            return HttpResponse("{'status': 'error','reason':'your paras should include the key named info'}")
        try:
            x = info['x']
            y = info['y']
            old_ref_id = info['ref_id']
        except KeyError:
            return HttpResponse("{'status': 'error','reason':'your info should include keys: x, y, ref_id'}")

        # x,y should be able to convert to a float number
        try:
            fx = float(x)
            fy = float(y)
        except ValueError:
            return HttpResponse("{'status': 'error','reason':'the x, y value should be float'}")

        node = db.node_ref.find_one({'_id': ObjectId(old_ref_id)})
        if not node:
            return HttpResponse("{'status': 'error','reason':'unable to find the record matching red_id given'}")
        else:
            db.node_ref.update({'_id': ObjectId(old_ref_id)}, {'$set', {'x': x, 'y': y}})
            return HttpResponse("{'status': 'success}")

    else:
        # method incorrect
        return HttpResponse("{'status': 'error','reason':'pls use method DELETE/PUT/GET/PATCH '}")


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
                    if isinstance(result[key], list) and len(result[key]) > 0 and isinstance(result[key][0], ObjectId):
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


@logged_in
@project_verified
def add_link(request):
    if request.method == "POST":
        # request.POST is all information of the link
        if validate_link(request.POST['info']):
            # all the information is valid(including the group)
            link_id = db.link.insert(request.POST['info'])
            linkref_id = db.link_ref.insert({
                'pid': int(request.POST['pid']) if 'pid' in request.POST.keys() else 0,
                }
            )

            # fail to insert into database
            if not link_id or not linkref_id:
                return HttpResponse("{'status':'error', 'reason':'insert failed'}")

            # add refs between two records
            db.link.update({'_id': link_id}, {'$push': {'refs': linkref_id}})
            db.link_ref.update({'_id': linkref_id}, {'$set': {'link_id': link_id,
                                                              'id1': ObjectId(request.POST['id1']),
                                                              'id2': ObjectId(request.POST['id2'])}})

            # return the _id of this user's own record of this link
            return HttpResponse({'ref_id': str(linkref_id)})

        else:
            # link info is incorrect
            return HttpResponse("{'status':'error', 'reason':'link info invalid'}")

    else:
        # method is not POST
        return HttpResponse("{'status':'error', 'reason':'pls use POST method'}")


@logged_in_exclude_get
@project_verified_exclude_get
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
        db.link_ref.insert({'pid': int(request.POST['pid']) if 'pid' in request.POST.keys() else 0,
                            'link_id': request.POST['_id'],
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
                if isinstance(link_dic[key], list) and len(link_dic[key]) > 0 and isinstance(link_dic[key][0], ObjectId):
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
                    if isinstance(result[key], list) and len(result[key]) > 0 and isinstance(result[key][0], ObjectId):
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


@logged_in
@project_verified
def test_prj(request):
    prj = Project.objects.get(pk=request.POST['pid'])
    return HttpResponse(prj.name + ' ' + prj.author.username)


