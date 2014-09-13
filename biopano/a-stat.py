from Queue import PriorityQueue
from Queue import Queue

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


q = Queue()
pq = PriorityQueue()
inf = 100000000
n=int(raw_input())
m=int(raw_input())
#edge ww
edge = MakeArray(m)
edge2 = MakeArray(m)
next = MakeArray(m)
next2 = MakeArray(m)

ww = MakeArray(m)
point = MakeArray(n)
point2 = MakeArray(n)
pre = [[] for i in range(n+1)]
dis = [inf for i in range(n+1)]

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



for i in range(m):
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