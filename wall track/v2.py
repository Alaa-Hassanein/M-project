from pyamaze import maze,agent,COLOR
from math import sqrt, pow
import time
def r_size (FR,BR):
    XFR, YFR = FR
    XBR, YBR = BR
    SIZE = sqrt(pow(XFR - XBR,2) + pow(YFR - YBR, 2))
    return SIZE

def r_or(LF,RF,RB,LB):
    xRF,yRF=RF
    xLF,yLF=LF
    xRB,yRB=RB
    xLB,yLB=LB
    if xLF==xRF:
        if xLF>xLB:
            return "S"
        else:
            return "W"
    else:
        if yLF >yLB:
            return "D"
        else:
            return "S"


def print_map(m,LF,RF,RB,LB):
    xRF,yRF=RF
    xLF,yLF=LF
    xRB,yRB=RB
    xLB,yLB=LB
    m[xRF][yRF]=2
    m[xLF][yLF]=2
    m[xRB][yRB]=2
    m[xLB][yLB]=2
    print(m)

def RCW(LF,RF,RB,LB):
    global direction
    k=list(direction.keys())
    v=list(direction.values())
    v_rotated=[v[-1]]+v[:-1]
    direction=dict(zip(k,v_rotated))
    z=LF
    LF=RF
    RF=RB
    RB=LB
    LB=z
    return LF,RF,RB,LB

def RCCW(LF,RF,RB,LB):
    global direction
    k=list(direction.keys())
    v=list(direction.values())
    v_rotated=v[1:]+[v[0]]
    direction=dict(zip(k,v_rotated))
    c=LF
    LF=LB
    LB=RB
    RB=RF
    RF=c
    return LF,RF,RB,LB

def moveForward(LF,RF,RB,LB):
    if direction['forward']=='E':
        return (LF[0],LF[1]+1),(RF[0],RF[1]+1),(RB[0],RB[1]+1),(LB[0],LB[1]+1),'E'
    if direction['forward']=='W':
        return (LF[0],LF[1]-1),(RF[0],RF[1]-1),(RB[0],RB[1]-1),(LB[0],LB[1]-1),'W'
    if direction['forward']=='N':
        return (LF[0]-1,LF[1]),(RF[0]-1,RF[1]),(RB[0]-1,RB[1]),(LB[0]-1,LB[1]),'N'
    if direction['forward']=='S':
        return (LF[0]+1,LF[1]),(RF[0]+1,RF[1]),(RB[0]+1,RB[1]),(LB[0]+1,LB[1]),'S'

def wall_Detection(LF,RF,RB,LB,maze,D):
    front=1
    left=1
    goal=0
    R=0
    xLF, yLF = LF
    xRF, yRF = RF
    xRB, yRB = RB
    xLB, yLB = LB
    if (D=="W"):
        minx=min(xLF,xLB)
        maxx=max(xLF,xLB)
        maxy=max(yLF,yRF)
        miny=min(yLF,yRF)
        for x in range(minx,maxx+1):
            if maze[x][yLF-1]==1:
                left=1
                break
            else:
                left=0
        if left==0:
            for x in range(minx,maxx+1):
                if maze[x][yLF-1]==8:
                    R=1
                    goal=1
                else:
                    R=0
                    goal=0
                    break


        for y in range (miny,maxy+1):
            if maze[xLF-1][y]==1:
                front=1
                break
            else:
                front=0
        if front==0:
            for y in range (miny,maxy+1):
                if maze[xLF-1][y]==8:
                    goal=1
                elif maze[xLF-1][y]==0:
                    front=0
                    break        
            
                

    elif (D=="S"):
        minx=min(xLF,xLB)
        maxx=max(xLF,xLB)
        maxy=max(yLF,yRF)
        miny=min(yLF,yRF)
        for x in range(minx,maxx+1):
            if maze[x][yLF+1]==1:
                left=1
                break
            else:
                left=0
        if left==0:
            for x in range(minx,maxx+1):
                if maze[x][yLF+1]==8:
                    R=1
                    goal=1 
                else:
                    R=0
                    goal=0
                    break

        
        for y in range (miny,maxy+1):
            if maze[xLF+1][y]==1:
                front=1
                break
            else:
                front=0
        if front==0:
            for y in range (miny,maxy+1):
                if maze[xLF+1][y]==8:
                    goal=1
                elif maze[xLF+1][y]==0:
                    front=0
                    break

                
    elif D=="D":
        maxx=max(xLF,xRF)
        minx=min(xLF,xRF)
        maxy=max(yLF,yLB)
        miny=min(yLF,yLB)
        for y in range (miny,maxy+1):
            if maze[xLF-1][y]==1:
                left=1
                break
            else:
                left=0
        if left ==0:
            for y in range (miny,maxy+1):
                if maze[xLF-1][y]==8:
                    goal=1
                    R=1
                else:
                    goal=0
                    R=0
                    break
        for x in range (minx,maxx+1):
            if maze[x][maxy+1]==1:
                front=1
                break
            else:
                front=0
        if front==0:
            for x in range (minx,maxx+1):
                if maze[x][maxy+1]==8:
                    goal=1
                    front=0
                elif maze[x][maxy+1]==0:
                    front=0
                    break
    elif D=="A":
        maxx=max(xLF,xRF)
        minx=min(xLF,xRF)
        maxy=max(yLF,yLB)
        miny=min(yLF,yLB)
        for y in range (miny,maxy+1):
            if maze[xLF+1][y]==1:
                left=1
                break
            else:
                left=0
        if left ==0:
            for y in range (miny,maxy+1):
                if maze[xLF+1][y]==8:
                    goal=1
                    R=1
                else:
                    goal=0
                    R=0
                    break
        for x in range (minx,maxx+1):
            if maze[x][maxy-1]==1:
                front=1
                break
            else:
                front=0
        if front==0:
            for x in range (minx,maxx+1):
                if maze[x][maxy-1]==8:
                    goal=1
                    front=0
                elif maze[x][maxy-1]==0:
                    front=0
                    break
    return (left,front,goal,R)                

                
    

    
        
    
    

def wallFollower(maze,goal,robot):
    global direction
    goal_found=0
    front=0
    left=0
    R=0
    direction={'forward':'N','left':'W','back':'S','right':'E'}
    k=0
    path=''
    xmax,ymax = max(goal)
    xmin,ymin = min(goal)
    RF=robot[0]
    LF=robot[1]
    RB=robot[2]
    LB=robot[3]
    xRF,yRF=RF
    xLF,yLF=LF
    xRB,yRB=RB
    xLB,yLB=LB
    
    while True:
        O=r_or(LF,RF,RB,LB)
        (left,front,goal_found,R)=wall_Detection(LF,RF,RB,LB,maze,O)
        if goal_found==1:
            if R==1:
                (LF,RF,RB,LB)=RCCW(LF,RF,RB,LB)
                xRF,yRF=RF
                xLF,yLF=LF
                xRB,yRB=RB
                xLB,yLB=LB
                LF,RF,RB,LB,h=moveForward(LF,RF,RB,LB)
                xRF,yRF=RF
                xLF,yLF=LF
                xRB,yRB=RB
                xLB,yLB=LB
                path+=h
                time.sleep(0.5)
                print(O,h,LF,RF,RB,LB)
                break
            else:
                LF,RF,RB,LB,h=moveForward(LF,RF,RB,LB)
                xRF,yRF=RF
                xLF,yLF=LF
                xRB,yRB=RB
                xLB,yLB=LB
                path+=h
                time.sleep(0.5)
                print(O,h,LF,RF,RB,LB)
                break        
        else:
            if left==1:
                if front==1:
                    (LF,RF,RB,LB)=RCW(LF,RF,RB,LB)
                    xRF,yRF=RF
                    xLF,yLF=LF
                    xRB,yRB=RB
                    xLB,yLB=LB
                else:
                    LF,RF,RB,LB,h=moveForward(LF,RF,RB,LB)
                    xRF,yRF=RF
                    xLF,yLF=LF
                    xRB,yRB=RB
                    xLB,yLB=LB
                    path+=h
                    time.sleep(0.5)
                    print(O,h,LF,RF,RB,LB)
            else:
                (LF,RF,RB,LB)=RCCW(LF,RF,RB,LB)
                xRF,yRF=RF
                xLF,yLF=LF
                xRB,yRB=RB
                xLB,yLB=LB

                LF,RF,RB,LB,h=moveForward(LF,RF,RB,LB)
                xRF,yRF=RF
                xLF,yLF=LF
                xRB,yRB=RB
                xLB,yLB=LB
                path+=h
                time.sleep(0.5)
                print(O,h,LF,RF,RB,LB) 


    print(path)    
    path2=path
    while 'EW' in path2 or 'WE' in path2 or 'NS' in path2 or 'SN' in path2:
        path2=path2.replace('EW','')
        path2=path2.replace('WE','')
        path2=path2.replace('NS','')
        path2=path2.replace('SN','')
    return path,path2
        


if __name__=='__main__':
    m=[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  #0
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],   #1
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],   #2
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],   #3
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],#4
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],#5
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],#6
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#7
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#8
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#9
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#10
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#11
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#12
      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#13
      [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#14
      [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#15
      [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#16
      [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#17
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#18
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#19
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#20
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#21
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#22
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#23
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#24
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#25
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#26
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#27
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#28
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#29
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#30
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#31
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#32
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#33
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#34
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#35
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#36
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#37
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#38
      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]#39
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    goal=  [[39,12],
            [39,13],
            [39,14],
            [39,15],
            [39,16],
            [39,17]]
    robot= [[35,4],#RF
            [35,1],#LF
            [38,4],#RB
            [38,1]]#LB
    path1,path2=wallFollower(m,goal,robot)

    print(path2)
    

