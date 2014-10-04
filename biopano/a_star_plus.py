from Queue import PriorityQueue
from Queue import Queue
from django.shortcuts import HttpResponse
from pymongo import *
from datetime import *
import bson


def MakeArray(n):
	return [0 for i in range(n+1)]

#class state is aimed at A*-state
class state:
	def __init__(self, f, g, now, pre):
		self.f = f
		self.g = g
		self.now = now
		self.pre = pre
	def __lt__(self, x):
		if (x.f == self.f):
			return x.g>self.g
		return x.f>self.f

db = MongoClient()['igemdata_new']

q = Queue()
pq = PriorityQueue()
inf = 100000000
#edge ww

#edge = MakeArray(m)
#edge2 = MakeArray(m)
#next = MakeArray(m)
#next2 = MakeArray(m)
edge = []
edge2 = []
next = []
next2 = []

#ww = MakeArray(m)
#point = MakeArray(n)
#point2 = MakeArray(n)
#pre = [[] for i in range(n+1)]
#dis = [inf for i in range(n+1)]
ww = []
point = []
point2 = []
pre = []
dis = []

def AddEdge(u,v,w,ee):
	global edge, edge2, ww, next, next2, point, point2
	edge[ee]=v
	edge2[ee]=u
	ww[ee]=w
	next[ee]=point[u]
	point[u]=ee
	next2[ee]=point2[v]
	point2[v]=ee

def Relax(u,v,c):
	global dis
	if dis[v]>dis[u]+c:
		dis[v]=dis[u]+c
		return True
	return False

def SPFA(src, n):
	global dis, point2, next2, ww, inf
	global q

	vis=[False for i in range(n+1)]
	dis[src] = 0
	q.put(src)
	while (not q.empty()):
		u = q.get()
		vis[u] = False
		i = point2[u]
		while i!=0:
			v = edge2[i]
			if Relax(u,v,ww[i]) and not vis[v]:
				q.put(v)
				vis[v] = True
			i = next2[i]

def Astar(src, to, k):
	global dis
	global pq

	cnt=0
	if src == to:
		k+=1
	if dis[src]==inf:
		yield -1
		return
	pq.put(state(dis[src], 0, src, [src]))
	time_monitor = datetime.now()
	while (not pq.empty()):
		b = pq.qsize()
		a = pq.get()
		if (a.now == to):
			yield a.pre
			cnt+=1
			if (cnt == k):
				break
		i=point[a.now]
		while i!=0:

			if not edge[i] in a.pre:
				pq.put(state(a.g+ww[i]+dis[edge[i]], a.g+ww[i], edge[i], a.pre+[edge[i]]))
			i=next[i]

			if (datetime.now() - time_monitor).seconds > 5:
				yield 0
				return



def a_star(request):
	global edge,edge2,next,next2,ww,point,point2,pre,dis
	if request.method == 'POST':
		link_count = 0
		node_count = 0
		link_pool = {}
		node_pool = {}
		search_dict = {}
		time_point = {}
		start_time = datetime.now()

		# count distinct node
		for node in db.node.find():
			if node_pool.get(node['_id']) is None:
				node_count += 1
				node_pool[node['_id']] = node_count
				search_dict[node_count] = node['_id']
		# count distinct link
		for link_ref in db.link_ref.find():
			if link_pool.get((link_ref['id1'], link_ref['id2'])) is None:
				link_count += 1
				link_pool[(link_ref['id1'], link_ref['id2'])] = True
		count_time = datetime.now()
		time_point['counting'] = count_time - start_time
		# initial vars
		edge = MakeArray(link_count)
		edge2 = MakeArray(link_count)
		next = MakeArray(link_count)
		next2 = MakeArray(link_count)
		ww = MakeArray(link_count)
		point = MakeArray(node_count)
		point2 = MakeArray(node_count)
		dis = [inf for i in xrange(node_count + 1)]

		initial_time = datetime.now()
		time_point['initial'] = initial_time - count_time

		# add in edge
		link_count = 0
		for distinct_link in link_pool:
			link_count += 1
			id1 = distinct_link[0]
			id2 = distinct_link[1]
			# ObjectId to int
			AddEdge(node_pool[id1], node_pool[id2], 1, link_count)

		s = node_pool[bson.ObjectId(request.POST['id1'])]
		t = node_pool[bson.ObjectId(request.POST['id2'])]
		k = int(request.POST['order'])

		convert_time = datetime.now()
		time_point['convert'] = convert_time - initial_time

		SPFA(t, node_count)

		SPFA_time = datetime.now()
		time_point['SPFA'] = SPFA_time - convert_time

		path_list = []
		for j in Astar(s, t, k):
			# not founded
			if j == -1:
				break

			# overtime
			if j == 0:
				break

			path = []
			for node in j:
				# path.append(str(search_dict[node]))
				path.append(db.node.find_one({'_id': search_dict[node]})['NAME'])
			path_list.append(path)

		Astar_time = datetime.now()
		time_point['Astar'] = Astar_time - SPFA_time

		return HttpResponse(str(path_list) + '\n' + str(time_point))

	elif request.method == 'GET':
		return HttpResponse("{'status':'error', 'reason':'no GET method setting'}")


'''for i in range(m):

	u=int(raw_input())
	v=int(raw_input())
	w=int(raw_input())
	AddEdge(u,v,w,i+1)
	s=int(raw_input())
t=int(raw_input())
k=int(raw_input())
SPFA(t)
for j in Astar(s,t,k):
	print j
'''
'''
dic={}
n=db.node.find().count()
m=db.link_ref.find().count()
edge = MakeArray(m)
edge2 = MakeArray(m)
next = MakeArray(m)
next2 = MakeArray(m)
ww = MakeArray(m)
point = MakeArray(n)
point2 = MakeArray(n)

time_point = {}
start_time = datetime.now()

n=0
m=0
for node in db.node.find():
	n+=1
	dic[str(node['_id'])]=n

for link in db.link_ref.find():
	u=dic[str(link['id1'])]
	v=dic[str(link['id2'])]
	m+=1
	AddEdge(u,v,1,m)

time_point['datebase_reading'] = datetime.now() - start_time

pre = [[] for i in range(n+1)]
dis = [inf for i in range(n+1)]

s=dic['541fb5a7fc368954b31db39a']
print s
t=dic['541fb83cfc368954b31e6b1c']
print t

k=1000
SPFA(t)
print dis[t]
for j in Astar(s,t,k):
	print j

time_point['search end'] = datetime.now() - start_time
time_report = '\n'.join(step + str(time_point[step]) for step in time_point.keys())

print time_report
'''