import pygame
import time
from RRTbasePy import RRTGraph
from RRTbasePy import RRTMap

def main():
    dimenstion =(600,1000)
    start =(50,50)
    goal=(510,510)
    obsdim=30
    obsnum=50
    iteration=0
    pygame.init()
    map=RRTMap(start,goal,dimenstion,obsdim,obsnum)
    graph=RRTGraph(start,goal,dimenstion,obsdim,obsnum)

    obstacles=graph.MakeObs()
    print(obstacles)
   
    
   

    
   
    
    
    

if __name__ == '__main__':
    main()