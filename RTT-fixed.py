import pygame
from RRTbasePy import RRTGraph
from RRTbasePy import RRTMap

def main():
    dimenstion =(600,1000)
    start =(50,50)
    goal=(510,510)
    obsdim=30
    obsnum=50
    pygame.init()
    map=RRTMap(start,goal,dimenstion,obsdim,obsnum)
    graph=RRTGraph(start,goal,dimenstion,obsdim,obsnum)

    obstacles=graph.MakeObs()
    map.drawMap(obstacles)

    pygame.display.update()
    pygame.event.clear()
    pygame.event.wait(0)

if __name__ == '__main__':
    main()