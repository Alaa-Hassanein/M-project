import random
import math
import pygame
class RRTMap:
    def __init__(self,start,goal,MapDimentions,obsdim,obsnum):
        self.start=start
        self.goal=goal
        self.MapDimentions=MapDimentions
        self.Maph,self.mapw=MapDimentions

        #windows settings
        self.mapwindowname='RRT path planing'
        pygame.display.set_caption(self.mapwindowname)
        self.map=pygame.display.set_mode((self.mapw,self.Maph))
        self.map.fill((255,255,255))
        self.nodeRad=0
        self.nodeThickness=0
        self.edgeThickness=1
        self.obstacles=[]
        self.obsnum=obsnum
        self.obsdim=obsdim

        #color
        self.grey=(70,70,70)
        self.blue=(0,0,255)
        self.gren=(0,255,0)
        self.red=(255,0,0)
        self.white=(255,255,255)
        

    def drawMap(self):
        pygame.draw.circle(self.map,self.green,self.start,self.nodeRad+5,0)
        pygame.draw.circle(self.map,self.green,self.goal,self.nodeRad+20,1)
        self.drawObs(obstacles)


    def  drawPath (self):
        pass
    def drawObs (self,obstacles):
        obstaclesList=obstacles.copy()
        while(len(obstaclesList)>0):
            obstacles=obstaclesList.pop(0)
            pygame.draw.rect(self.map,self.grey,obstacles)


class RRTGraph:
    def __init__(self,start,goal,MapDimentions,obsdim,obsnum):
        (x,y)=start
        self.start=start
        self.goal=goal
        self.goalFLage=False
        self.Maph,self.mapw=MapDimentions
        self.x=[]
        self.y=[]
        self.parent=[]

        #init the tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)

        #the obs
        self.obstacles=[]
        self.obsnum=obsnum
        self.obsdim=obsdim

        #path
        self.goalstate=None
        self.path=[]


    def makeRandomRect(self):
        uppercornerx=int(random.uniform(0,self.mapw-self.obsdim))
        uppercornerx=int(random.uniform(0,self.mapw-self.obsdim))
        return (uppercornerx,uppercornerx)


    def MakeObs(self):
        obs=[]

        for i in range(0,self.obsnum):
            rectang=None
            startgoalcol = True
            while startgoalcol:
                upper=self.makeRandomRect()
                rectang=pygame.Rect(upper,(self.obsdim,self.obsdim))
                if rectang.collidepoint(self.start) or rectang.collidepoint(self.goal):
                    startgoalcol=True
                else:
                    startgoalcol=False
            obs.append(rectang)
        self.obstacles=obs.copy()
        return obs

                


    def remove_node (self):
        pass
    def add_edge(self):
        pass
    def number_of_nodes(self):
        pass
    def distance (self):
        pass
    def nearst (self):
        pass
    def isFree (self):
        pass
    def crossObstacle (self):
        pass
    def connect (self):
        pass
    def step (self):
        pass
    def pass_to_goal(self):
        pass
    def getpathcoords(self):
        pass
    def bias (self):
        pass
    def expand (self):
        pass
    def cost (self):
        pass

        

