from pymongo import *
from django.shortcuts import HttpResponse
import bson
db = MongoClient()['igemdata_new']

def func(a,b):
    if a==b:
        return 1
    else:
		return -1


def NeedleWunch(s, t):
	n = len(s)
	m = len(t)
	f=[[0 for j in range(m+1)] for i in range(n+1)]
	g=[[0 for j in range(m+1)] for i in range(n+1)]
	h=[[0 for j in range(m+1)] for i in range(n+1)]

	for i in range(n):
		f[i+1][0] = -2 * (i+1)
		g[i+1][0] = i
		h[i+1][0] = 0
	for j in range(m):
		f[0][j+1] = -2 * (j+1)
		g[0][j+1] = 0
		h[0][j+1] = j

	for i in range(n):
		for j in range(m):
			f[i+1][j+1] = max(max(f[i+1][j],f[i][j+1])-2,f[i][j]+func(s[i],t[j]))
			if f[i+1][j+1]==f[i+1][j]-2:
				g[i+1][j+1]=i+1
				h[i+1][j+1]=j
			elif f[i+1][j+1]==f[i][j+1]-2:
				g[i+1][j+1]=i
				h[i+1][j+1]=j+1
			else:
				g[i+1][j+1]=i
				h[i+1][j+1]=j
	i = n
	j = m
	ss=""
	tt=""
	while (i!=0 or j!=0):
		if g[i][j]==i:
			ss='_'+ss
		else:
			ss=s[i-1]+ss
		if h[i][j]==j:
			tt='_'+tt
		else:
			tt=t[j-1]+tt
		i,j=g[i][j],h[i][j]
	#print ss
	#print tt
	return f[n][m]


def main(request):
    if request.method == 'POST':
        if 'sequence' not in request.POST.keys():
            key_list = str(request.POST.keys())
            return HttpResponse("{'status':'error', 'reason':'keyword sequence is not in request.', 'keys':" + key_list +"}")
        a = request.POST['sequence'].upper()
        id_list = []
        b = []
        # what down here is ugly code!
        for u_t_r in db.u_t_r.find():
            if u_t_r['TYPE'] == 'O_T_P':
                if u_t_r['SEQUENCE_5'] is not '':
                    id_list.append(str(u_t_r['node_id']))
                    b.append(u_t_r['SEQUENCE_5'].upper())
                if u_t_r['SEQUENCE_3'] is not '':
                    id_list.append(str(u_t_r['node_id']))
                    b.append(u_t_r['SEQUENCE_3'].upper())
            else:
                id_list.append(str(u_t_r['node_id']))
                b.append(u_t_r['SEQUENCE'].upper())
        ans = -9999999999
        ansx = []
        for i in b:
	        x=NeedleWunch(a, i)
	        if x==ans:
	        	ansx+=[b.index(i)]
	        if x>ans:
	        	ans=x
	        	ansx=[b.index(i)]

        result = []
        for each in ansx:
            dict = {}
            dict['_id'] = id_list[each]
            node = db.node.find_one({'_id': bson.ObjectId(id_list[each])})
            dict['NAME'] = node['NAME']
            dict['TYPE'] = node['TYPE']
            dict['SCORE'] = ans
            result.append(dict)

        return HttpResponse(result)
        #print ans   # mark
        #print ansx  # object list which have highest mark
    elif request.method == 'GET':
        return HttpResponse("{'status':'error', 'reason':'no GET method setting'}")
