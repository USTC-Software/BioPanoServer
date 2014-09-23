from pymongo import *
from django.shortcuts import HttpResponse
import bson
from datetime import *

db = MongoClient()['igemdata_new']


def func(a, b):
    if a == b:
        return 1
    else:
        return -1


def NeedleWunch(s, t):
    n = len(s)
    m = len(t)
    f = [[0 for j in range(m + 1)] for i in range(n + 1)]

    for i in range(n):
        f[i + 1][0] = -2 * (i + 1)
    for j in range(m):
        f[0][j + 1] = -2 * (j + 1)

    for i in range(n):
        for j in range(m):
            f[i + 1][j + 1] = max(max(f[i + 1][j], f[i][j + 1]) - 2, f[i][j] + func(s[i], t[j]))
    return f[n][m]


def main(request):
    if request.method == 'POST':
        if 'sequence' not in request.POST.keys():
            key_list = str(request.POST.keys())
            return HttpResponse(
                "{'status':'error', 'reason':'keyword sequence is not in request.', 'keys':" + key_list + "}")
        a = request.POST['sequence'].upper()
        id_list = []
        b = []
        # what down here is ugly code!
        time_point = {}
        start_time = datetime.now()
        for u_t_r in db.u_t_r.find():
            if u_t_r['TYPE'] == 'O_T_P':
                if u_t_r['SEQUENCE_5'] is not '':
                    # id_list.append(str(u_t_r['node_id']))
                    b.append(u_t_r['SEQUENCE_5'].upper())
                if u_t_r['SEQUENCE_3'] is not '':
                    # id_list.append(str(u_t_r['node_id']))
                    b.append(u_t_r['SEQUENCE_3'].upper())
            else:
                # id_list.append(str(u_t_r['node_id']))
                b.append(u_t_r['SEQUENCE'].upper())
        time_point['datebase_reading'] = datetime.now() - start_time
        ans = -9999999999
        ansx = []
        for i in b:
            x = NeedleWunch(a, i)
            if x == ans:
                ansx += [i]
            if x > ans:
                ans = x
                ansx = [i]
        time_point['core_computing'] = datetime.now() - start_time
        result = []
        for sequence in ansx:
            for node in db.u_t_r.find({'$or': [{'SEQUENCE': sequence}, {'SEQUENCE_3': sequence}, {'SEQUENCE_5': sequence}]}):
                if str(node['node_id']) not in id_list:
                    id_list.append(str(node['node_id']))
        time_point['search_result_in_datebase'] = datetime.now() - start_time
        for each_id in id_list:
            dicts = {'_id': each_id}
            node = db.node.find_one({'_id': bson.ObjectId(each_id)})
            dicts['NAME'] = node['NAME']
            dicts['TYPE'] = node['TYPE']
            dicts['SCORE'] = ans
            result.append(dicts)
        result = str(result)
        time_point['serialize'] = datetime.now() - start_time

        time_report = '\n'.join(step + str(time_point[step]) for step in time_point.keys())
        return HttpResponse(result)
        # print ans   # mark
        #print ansx  # object list which have highest mark
    elif request.method == 'GET':
        #return HttpResponse('This is new!!!!')
        return HttpResponse("{'status':'error', 'reason':'no GET method setting'}")
