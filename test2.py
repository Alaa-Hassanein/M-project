

import random
import math
import pygame

def makeRandomRect():
        uppercornerx=int(random.randint(0,1000))
        uppercornery=int(random.randint(0,1000))
        return (uppercornerx,uppercornery)
def make():
        obs=[]
        for i in range(0,20):
            rectang=None
            startgoalcol = True
            while startgoalcol:
                upper=makeRandomRect()
                rectang=pygame.Rect(upper,(12,12))
                if rectang.collidepoint(15,11) or rectang.collidepoint(80,73):
                    startgoalcol=True
                else:
                    startgoalcol=False
            obs.append(rectang)
        obstacles=obs.copy()
        return obs
def main():
    o=make()
    print(type(o)

if __name__ == '__main__':
    main()