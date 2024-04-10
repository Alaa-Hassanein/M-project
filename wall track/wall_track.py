from pyamaze import maze,agent


def RCW():
    global directions
    k=list(directions.keys())
    v=list(directions.values())
    x=v[0]
    for i in range(len(v)-1):
        
        v[i]=v[i+1]
    v[len(v)-1]=x

    zip(k,v)
    directions=dict(zip(k,v))


def RCCW():
    global directions
    k=list(directions.keys())
    v=list(directions.values())
    x=v[len(v)-1]
    i=len(v)-1
    print(x)
    while (i>0):
        v[i]=v[i-1]
        i=i-1
    v[0]=x

    zip(k,v)
    directions=dict(zip(k,v))


def MoveForward(pos):
    if directions['forward'] == 'N':
        return (pos[0] - 1, pos[1]),'N'
    if directions['forward'] == 'E':
        return (pos[0], pos[1] + 1),'E'
    if directions['forward'] == 'S':
        return (pos[0] + 1, pos[1]),'S'
    if directions['forward'] == 'W':
        return (pos[0], pos[1] - 1),'W'



def Wall_Follower(F):
    global directions
    directions={'forward':'N','left':'W','back':'S','right':'E'}
    currPos=(F.rows,F.cols)
    path=''
    while True:
        if currPos == (1, 1):
            break
        if F.maze_map[currPos][directions['left']] == 0:
            if F.maze_map[currPos][directions['forward']] == 0:
                RCW()
            else:
                currPos, D = MoveForward(currPos)
                path += D
        else:
            RCCW()
            currPos, D = MoveForward(currPos)
            path += D


    
if __name__=='__main__':
    myMaze=maze(6,6)
    myMaze.CreateMaze()
    a=agent(myMaze,shape='arrow')

    
    path=Wall_Follower(myMaze)


    myMaze.tracePath({a:path})


    myMaze.run()