from Queue import PriorityQueue
from Queue import Queue
from django.shortcuts import HttpResponse
from pymongo import *

def MakeArray(n):
	return [0 for i in range(n+1)]

#class state is aimed at A*-state
class state:
	def __init__(self, f, g, now):
		self.f = f
		self.g = g
		self.now = now
	def __lt__(self, x):
		if (x.f == self.f):
			return x.g<self.g
		return x.f<self.f

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

def SPFA(src):
	global dis, point2, next2, ww, inf
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
	global dis, pre
	pre[src]=[src]
	cnt=0
	if src == to:
		k+=1
	if dis[src]==inf:
		yield -1
		return
	pq.put(state(dis[src], 0, src))
	while (not pq.empty()):
		a = pq.get()
		if (a.now == to):
			yield pre[to]
			cnt+=1
			if (cnt == k):
				break
		i=point[a.now]
		while i!=0:
			pq.put(state(a.g+ww[i]+dis[edge[i]], a.g+ww[i], edge[i]))
			pre[edge[i]]=pre[a.now]+[edge[i]]
			i=next[i]

def a_star(request):
    global edge,edge2,next,next2,ww,point,point2,pre,dis
    if request.method == 'POST':
        link_count = 0
        node_count = 0
        range = 2000000
        link_hash_pool = [False for i in xrange(range)]
        node_hash_pool = [False for i in xrange(range)]
        for link_ref in db.link_ref.find():
            link_hash_value = hash((link_ref['id1'],link_ref['id2'])) % range
            if link_hash_pool[link_hash_value] is False:
                link_count += 1
                link_hash_pool[link_hash_value] = True
                AddEdge(link_ref['id1'], link_ref['id2'],1,link_count)
            node1_hash = hash(link_ref['id1']) % range
            node2_hash = hash(link_ref['id2']) % range
            if node_hash_pool[node1_hash] is False:
                node_hash_pool[node1_hash] = True
                node_count += 1
            if node_hash_pool[node2_hash] is False:
                node_hash_pool[node2_hash] = True
                node_count += 1

        edge = MakeArray(link_count)
        edge2 = MakeArray(link_count)
        next = MakeArray(link_count)
        next2 = MakeArray(link_count)
        ww = MakeArray(link_count)
        point = MakeArray(node_count)
        point2 = MakeArray(node_count)
        pre = [[] for i in xrange(node_count)]
        dis = [inf for i in xrange(node_count)]

        s = request.POST['id1']
        t = request.POST['id2']
        k = request.POST['order']
        SPFA(t)

        path = []
        for j in Astar(s,t,k):
            path.append(j)
        return HttpResponse(str(path))

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