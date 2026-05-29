
import tkinter as tk
scr = tk.Tk("ds project")
canv = tk.Canvas(scr,width=2000,height=1000,bg="#FFFFFF")
def scale(x,y):
    return x*50,y*50
def dot(x,y):
    canv.create_oval(x,y,x+50,y+50,fill="#000000")
import math
with open("inputs.txt", "r") as f:
    content = f.read()

print(type(content))
print(content)

start = None
goal = None
obstacles = []
lines = content.splitlines()
i = 0
while i < len(lines):
    line = lines[i].strip()
    if line == "START":
        i += 1
        x, y = map(int, lines[i].split())
        start = (x, y)
    elif line == "GOAL":
        i += 1
        x, y = map(int, lines[i].split())
        goal = (x, y)
    elif line == "POINTS":
        i += 1
        n = int(lines[i])
        points = []
        for _ in range(n):
            i += 1
            x, y = map(int, lines[i].split())
            points.append((x, y))
        obstacles.append(points)
    i += 1

def polar_angle(p):
    return math.atan2(p[1] - start[1], p[0] - start[0])
    
def mergesort(A):
    if len(A)<2:
        return A
    B,C = mergesort(A[:len(A)//2]),mergesort(A[len(A)//2:])
    i,j=0,0
    A.clear()
    while i<len(B) and j<len(C):
        if polar_angle(B[i])>polar_angle(C[j]):
            A.append(C[j])
            j+=1
        else:
            A.append(B[i])
            i+=1
    return A + B + C


def graham_scan(points):
    start = min(points, key=lambda p: (p[1], p[0]))

    sorted_points = mergesort(points)

    hull = []
    for p in sorted_points:
        while len(hull) >= 2:
            x1, y1 = hull[-2]
            x2, y2 = hull[-1]
            x3, y3 = p
            cross = (x2 - x1)*(y3 - y1) - (y2 - y1)*(x3 - x1)
            if cross > 0:  # اگر خلاف جهت چرخش داشتیم
                break
            hull.pop()
        hull.append(p)
    return hull

convex_obstacles = [graham_scan(ob) for ob in obstacles]
class WeightedGraph:
    '''
    using list of neighbors
    format is like that:
    [node,(connected1,cost1),(connected2,cost2)...]
    '''
    def __init__(self):
        self.graph = []
    def addNode(self,val):
        self.graph.append([val]) #O(V)
    def addEdge(self,node1,node2,w):#O(V+E)
        
        for i in self.graph:
            if i[0] == node1:
                if not i.count(node2)>0:
                    i.append((node2,w))
            if i[0] == node2:
                if not i.count(node1)>0:
                    i.append((node1,w))
    def print(self):
        for i in self.graph:
            print(i[0],':',*i[1:])



graph = WeightedGraph()
nodes = [start, goal] + [pt for hull in convex_obstacles for pt in hull]
for n in nodes:
    graph.addNode(n)




def get_edges(hull):
    edges = []
    n = len(hull)
    for i in range(n):
        edges.append((hull[i], hull[(i+1)%n]))
    return edges

obstacle_edges = [get_edges(hull) for hull in convex_obstacles]

def ccw(A, B, C):
    return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

def do_intersect(A, B, C, D):
    return (ccw(A, C, D) != ccw(B, C, D)) and (ccw(A, B, C) != ccw(A, B, D))

def is_visible(p1, p2, all_edges):
    for edge_list in all_edges:
        for edge in edge_list:
            A, B = edge
            if p1 in edge or p2 in edge:
                continue
            if do_intersect(p1, p2, A, B):
                return False
    return True
for i, p1 in enumerate(nodes):
    for j, p2 in enumerate(nodes):
        if i >= j:
            continue
        if is_visible(p1, p2, obstacle_edges):
            dist = math.hypot(p1[0]-p2[0], p1[1]-p2[1])
            graph.addEdge(p1,p2,dist)


class Node:
    def __init__(self,val):
        self.val = val
        self.childs = []
        self.parent = None

class Tree:
    def __init__(self):
        self.root = None
    def insert(self,val,node:Node = None):
        if self.root == None:
            self.root = Node(val)
            return self.root
        n = Node(val)
        node.childs.append(n)
        n.parent = node
        return n
    def delete(self,node:Node):
        node.parent.childs.remove(node)
        node.parent.childs.extend(node.childs)
        for i in node.childs:
            i.parent = node.parent
    def findUTIL(self,val,rt):
        if rt == None:
            return None
        if rt.val == val:
            return rt
        for i in rt.childs:
            n = self.findUTIL(val,i)
            if n != None:
                return n
    def find(self,val):
        return self.findUTIL(val,self.root)
    def printTreeUTIL(self,rt):
        print(str(rt.val) + "->",end="")
        for c in rt.childs:
            print(str(c.val),end="")
        print()
        for c in rt.childs:
            self.printTreeUTIL(c)
    def printTree(self):
        self.printTreeUTIL(self.root)
class PriorityQueue:#using min heap (as array, child indexes are 2i + 1 and 2i + 2)
    #the least priority(or cost) is popped first
    def __init__(self,ml):
        self.queue = [(None,None) for _ in range(ml)]  #heap , elements are touples
        self.maxlen = ml
        self.lentgh = 0
    '''def heapify(self):#O(n)
        for i in range(len(self.queue)):
            p = self.queue[i][1]
            b = False
            while 2*i + 2 < len(self.queue):
                if self.queue[2*i+1][1]<self.queue[2*i+2][1]:
                    if self.queue[2*i+1][1]<p:
                        t = self.queue[2*i+1]
                        self.queue[2*i+1] = self.queue[i]
                        self.queue[i] = t
                        i = 2*i+1
                    else:
                        b = True
                else:
                    if self.queue[2*i+2][1]<p:
                        t = self.queue[2*i+2]
                        self.queue[2*i+2] = self.queue[i]
                        self.queue[i] = t
                        i = 2*i+2
                    else:
                        b = True
                if b:
                    break
        if self.queue[2*i+1][1]<p:
            t = self.queue[2*i+1]
            self.queue[2*i+1] = self.queue[i]
            self.queue[i] = t
            i = 2*i+1'''
    def insert(self,x,p):
        if self.lentgh == self.maxlen:
            raise Exception("queue overflow")
        t = (x,p)
        self.queue[self.lentgh] = t
        self.lentgh += 1
        i = self.lentgh - 1
        while i != 0 and self.queue[int((i-2)/2)][1]>p:
            t = self.queue[int((i-2)/2)]
            self.queue[int((i-2)/2)] = self.queue[i]
            self.queue[i] = t
            i = int((i-2)/2)
    def pop(self):
        if self.lentgh == 0:
            raise Exception("queue empty")
        self.lentgh -= 1
        res = self.queue[0]
        self.queue[0] = self.queue[self.lentgh]
        i = 0
        b = False
        while 2*i + 2 <= self.lentgh:
            if self.queue[2*i+1][1]<self.queue[2*i+2][1]:
                if self.queue[2*i+1][1]<res[1]:
                    t = self.queue[2*i+1]
                    self.queue[2*i+1] = self.queue[i]
                    self.queue[i] = t
                    i = 2*i+1
                else:
                    b = True
            else:
                if self.queue[2*i+2][1]<res[1]:
                    t = self.queue[2*i+2]
                    self.queue[2*i+2] = self.queue[i]
                    self.queue[i] = t
                    i = 2*i+2
                else:
                    b = True
            if b:
                break
        if self.queue[2*i+1][1]!=None and self.queue[2*i+1][1]<res[1]:
            t = self.queue[2*i+1]
            self.queue[2*i+1] = self.queue[i]
            self.queue[i] = t
            i = 2*i+1
        return res
    

def distance(a,b):
    return math.sqrt((a[0] - b[0]) ** 2  + (a[1]-b[1]) ** 2)
def heuristic(a,b):
    return distance(a,b)
def A_star(graph:WeightedGraph,start,goal):
    tree=Tree()
    root=tree.insert(start)
    frontier=PriorityQueue(100)
    frontier.insert(root,heuristic(start,goal))
    visited=[]
    g_cost={start:0}
    while frontier.lentgh !=0:
        current_node,f=frontier.pop()
        current_val=current_node.val
        if current_val in visited:
            continue
        visited.append(current_val)
        if current_val==goal:
            return tree,current_node,g_cost[current_val]
        neighbors=[]
        for item in graph.graph:
            if item[0]==current_val:
                neighbors=item[1:]
                break
        for nb,_ in neighbors:
            if nb in visited:
                continue
            child=tree.insert(nb,current_node)
            new_g=g_cost[current_val]+distance(current_val,nb)
            if nb not in g_cost or new_g<g_cost[nb]:
                g_cost[nb]=new_g

                f_cost=new_g + heuristic(nb,goal)
                frontier.insert(child,f_cost)
                p1 = scale(current_val[0],current_val[1])
                p2 = scale(nb[0],nb[1])
                canv.create_line(p1[0]+25,p1[1]+25,p2[0]+25,p2[1]+25,fill="#26FF26")

    print("None")
    return None

tree,curr,cost = A_star(graph,start,goal)


class Stack:
    def __init__(self,mxln):
        self.mxln = mxln
        self.len = 0
        self.arr = [0] * mxln
    def push(self,x):
        if self.len==self.mxln:
            raise Exception("stack overflow")
        self.arr[self.len] = x
        self.len += 1
    def pop(self):
        if self.len == 0 :
            raise Exception("stack empty")
        self.len -= 1
        return self.arr[self.len]

st = Stack(10000)
while curr != None:
    st.push(curr)
    curr = curr.parent
way = []
while True:
    try:
        way.append(st.pop().val)
    except Exception:
        break

print("Start:", start)
print("Goal:", goal)
print("Obstacles:", obstacles)
graph.print()
tree.printTree()
print(*way)






#grid:
for i in range(30):
    for j in range(15):
        x,y = scale(i,j)
        canv.create_line(x,0,x,1500,fill="#262626")
        canv.create_line(0,y,1500,y,fill="#262626")
#start and end
x,y = scale(start[0],start[1])
dot(x,y)
x,y = scale(goal[0],goal[1])
dot(x,y)
#obstacles
#for ob in convex_obstacles:
    #print(ob)
#    for i,j in ob:
#        x,y = scale(i,j)
#        dot(x,y)
for ob in convex_obstacles:
    lst = []
    for i in ob:
        lst.append(i[0]*50+25)
        lst.append(i[1]*50+25)
    canv.create_polygon(*lst,fill="#2626FF",outline="#000026",width=3)
#way

for i in range(len(way)-1):
    p1,p2 = scale(way[i][0],way[i][1]),scale(way[i+1][0],way[i+1][1])
    canv.create_line(p1[0]+25,p1[1]+25,p2[0]+25,p2[1]+25,fill="#FF2626",width="3")




canv.place(x=0,y=0)

scr.mainloop()