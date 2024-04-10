import random
import math
import pygame
import cv2 
import numpy as np



class RRTMap:
    def __init__(self,start,goal,MapDimentions,obsdim):
        self.start=start
        self.goal=goal
        self.MapDimentions=MapDimentions
        self.Maph,self.mapw=MapDimentions
        self.obsdim=obsdim

        #windows settings
       
        self.map=pygame.display.set_mode((self.mapw,self.Maph))
        pygame.display.set_caption('RRT path planing')
        maze=pygame.image.load('maze.jpg')
        self.map.fill((255, 255, 255))
        self.map.blit(maze,(0,0))
        self.nodeRad=2
        self.nodeThickness=0
        self.edgeThickness=1
        

        #color
        self.black=(0,0,0)
        self.grey=(70,70,70)
        self.blue=(0,0,255)
        self.green=(0,255,0)
        self.red=(255,0,0)
        self.white=(255,255,255)
       
        

    def drawMap(self):
        pygame.draw.circle(self.map,self.green,self.start,self.nodeRad+5,0)
        pygame.draw.circle(self.map,self.green,self.goal,self.nodeRad+20,1)
        


    def  drawPath (self, path):
       for node in path:
            pygame.draw.circle(self.map,self.red,node,self.nodeRad+3,0)
        
        

    def drawObs (self,obstacles):
        obstaclesList=obstacles.copy()
        while(len(obstaclesList)>0):
            obstacles=obstaclesList.pop(0)
            pygame.draw.rect(self.map,self.black,obstacles)


class RRTGraph:
    def __init__(self,start,goal,MapDimentions,obsdim):
        self.obsdim=obsdim
        self.maze=pygame.image.load('maze.jpg')
        self.nodeRad=30
        self.nodeThickness=0
        self.edgeThickness=1
        (x,y)=start
        self.start=start
        self.goal=goal
        self.goalFLag=False
        self.Maph,self.mapw=MapDimentions
        self.x=[]
        self.y=[]
        self.parent=[]
        self.black=(0,0,0)
        self.im = cv2.imread('maze.jpg')
        self.gray = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)
        self.Yb, self.Xb = np.where(np.all(self.im==self.black,axis=2))

        #init the tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)

        #path
        self.goalstate=None
        self.path=[]


        


    def MakeObs(self):
        
        obs=[]
        for i in range(0,len(self.Xb)):
            rectang=None
            startgoalcol = True
            while startgoalcol:
                upper=(self.Xb[i],self.Yb[i])
                rectang=pygame.Rect(upper,(self.obsdim,self.obsdim))
                if rectang.collidepoint(self.start) or rectang.collidepoint(self.goal):
                    startgoalcol=True
                else:
                    startgoalcol=False
            obs.append(rectang)
        self.obstacles=obs.copy()
        return obs
         

    def add_node (self,n,x,y):
        self.x.insert(n,x)
        self.y.append(y)


    def remove_node (self,n):
        self.x.pop(n)
        self.y.pop(n)


    def add_edge(self,parent,child):
        self.parent.insert(child,parent)

    def remove_edge(self,parent,n):
        self.parent.popn(n)


    def number_of_nodes(self):
        return len(self.x)


    def distance (self,n1,n2):
        (x1,y1)=(self.x[n1],self.y[n1])
        (x2,y2)=(self.x[n2],self.y[n2])
        px=(float(x1)-float(x2))**2
        py=(float(y1)-float(y2))**2
        return (px+py)**0.5


    def sample_evir(self):
        x=int(random.randint(0,self.mapw))   
        y=int(random.randint(0,self.Maph)) 
        return x,y


    def nearest (self,n):
        dmin=self.distance(0,n)
        nnear=0
        for i in range(0,n):
            if self.distance(i,n)<dmin:
                dmin=self.distance(i,n)
                nnear=i
        return nnear


    def isFree (self):
        n=self.number_of_nodes()-1
        (x,y)=(self.x[n],self.y[n])
        half_width = 55 
        half_height = 55 
        start_x = int(x - half_width)
        start_y = int(y - half_height)
        square_region = self.gray[start_y:start_y+110, start_x:start_x+110]

        
        if any(pixel != 255 for pixel in square_region.flatten()) :
            self.remove_node(n)
            return False
        return True
        
        


    def crossObstacle (self,x1,x2,y1,y2):
           
        for i in range(0,101):
            u=i/100
            x=x1*u+x2*(1-u)
            y=y1*u+y2*(1-u)
            half_width = 20 
            half_height = 20 
            start_x = int(x - half_width)
            start_y = int(y - half_height)
            square_region = self.gray[start_y:start_y+40, start_x:start_x+40]
            if any(pixel != 255 for pixel in square_region.flatten()):
                return True
        return False


    def connect (self,n1,n2):
        (x1,y1)=(self.x[n1],self.y[n1])
        (x2,y2)=(self.x[n2],self.y[n2])
        if self.crossObstacle(x1,x2,y1,y2):
            self.remove_node(n2)
            return False
        else:
            self.add_edge(n1,n2)
            return True
            

    def step (self,nnear,nrand,dmax=35):
        d=self.distance(nnear,nrand)
        if d>dmax:
            u=dmax/d
            (xnear,ynear)=(self.x[nnear],self.y[nnear])
            (xrand,yrand)=(self.x[nrand],self.y[nrand])
            (px,py)=((xrand-xnear),(yrand-ynear))
            theta=math.atan2(py,px)
            (x,y)=(int(xnear+dmax *math.cos(theta)),int(ynear+dmax * math.sin(theta)))
            self.remove_node(nrand)
            if abs(x-self.goal[0])<dmax and abs (y-self.goal[1])<dmax:
                self.add_node(nrand,self.goal[0],self.goal[1])
                self.goalstate=nrand
                self.goalFLag=True
            else:
                self.add_node(nrand,x,y)


    def path_to_goal(self):
        if self.goalFLag:
            self.path=[]
            self.path.append(self.goalstate)
            newpos=self.parent[self.goalstate]
            while(newpos !=0):
                self.path.append(newpos)
                newpos=self.parent[newpos]
            self.path.append(0)
        return self.goalFLag

    def getpathcoords(self):
        pathCoords=[]
        for node in self.path:
            x,y=(self.x[node],self.y[node])
            pathCoords.append((x,y))
        return pathCoords


    def bias (self,ngoal):
        n=self.number_of_nodes()
        self.add_node(n,ngoal[0],ngoal[1])
        nnear=self.nearest(n)
        self.step(nnear,n)
        self.connect(nnear,n)
        return self.x,self.y,self.parent


    def expand (self):
        n=self.number_of_nodes()
        x,y=self.sample_evir()
        self.add_node(n,x,y)
        if self.isFree():
            xnearest=self.nearest(n)
            self.step(xnearest,n)
            self.connect(xnearest,n)
        return self.x,self.y,self.parent


    def cost (self):
        pass

        

