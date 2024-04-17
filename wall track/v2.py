import pygame 


class Map:
    def __init__(self,start,goal,MapDimentions):
        self.start=start
        self.goal=goal
        self.MapDimentions=MapDimentions
        self.Maph,self.mapw=MapDimentions
        self.obsdim=obsdim

        #windows settings
       
        self.map=pygame.display.set_mode((self.mapw,self.Maph))
        pygame.display.set_caption('wall track path planing')
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