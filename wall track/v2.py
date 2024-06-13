from math import sqrt, pow
import numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv

def corners(arr):
    x=[]
    for i in range (0,len(arr)-1):
        if arr [i]!=arr[i+1]:
            x.append(i)

    return x

def cheak_points(arr):
    for i in arr:
        if i==1:
            return 1
    return 0

def check_diagonal_points(start, end, array_2d):
    
    x_start, y_start = start
    x_end, y_end = end
    x_diff = x_end - x_start
    y_diff = y_end - y_start
    diagonal_points = []
    xy=[]
    if x_diff == 0 or y_diff == 0:
        x=[[1,1],[1,1]]
        diagonal_points.append(x)
        xy.append(x)
        xy=[[1,1],[3,4]]
        return diagonal_points,xy
    else:
        if x_diff > 0 and y_diff > 0:
            while True:
                x_diff = x_end - x_start
                y_diff = y_end - y_start
                x_start = int(x_start)
                y_start = int(y_start)
                x=array_2d[x_start][y_start]
                po=(x_start,y_start)
                xy.append(po)
                diagonal_points.append(x) 
                if x_diff == 0 and y_diff == 0:
                    break
                elif x_diff != 0 and y_diff != 0:
                    x_start += 1
                    y_start += 1
                elif x_diff == 0:
                    y_start += 1
                elif y_diff == 0:
                    x_start += 1
                
        elif x_diff > 0 and y_diff < 0:
            while True:
                x_diff = x_end - x_start
                y_diff = y_start - y_end
                x_start = int(x_start)
                y_start = int(y_start)
                x=array_2d[x_start][y_start]
                po=(x_start,y_start)
                xy.append(po)
                diagonal_points.append(x) 
                if x_diff == 0 and y_diff == 0:
                    break
                elif x_diff != 0 and y_diff != 0:
                    x_start += 1
                    y_start =y_start - 1 
                elif x_diff == 0:
                    y_start =y_start - 1
                elif y_diff == 0:
                    x_start += 1
                   
        elif x_diff < 0 and y_diff > 0:
            while True:
                x_diff = x_start- x_end
                y_diff = y_end - y_start
                x_start = int(x_start)
                y_start = int(y_start)
                x=array_2d[x_start][y_start]
                po=(x_start,y_start)
                xy.append(po)
                diagonal_points.append(x) 
                if x_diff == 0 and y_diff == 0:
                    break
                elif x_diff != 0 and y_diff != 0:
                    x_start =x_start - 1
                    y_start += 1
                elif x_diff == 0:
                    y_start += 1
                elif y_diff == 0:
                    x_start =x_start - 1
        return diagonal_points,xy

def draw(binary_array):
    plt.imshow(binary_array, cmap='Greys', interpolation='nearest')
    plt.colorbar(label='Binary Value')
    plt.show()

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
            return "A"

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
    
    k=1
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
            if maze[x][yLF-k]==1:
                left=1
                break
            else:
                left=0
        if left==0:
            for x in range(minx,maxx+1):
                if maze[x][yLF-k]==3:
                    R=1
                    goal=1
                else:
                    R=0
                    goal=0
                    break


        for y in range (miny,maxy+1):
            if maze[xLF-k][y]==1:
                front=1
                break
            else:
                front=0
        if front==0:
            for y in range (miny,maxy+1):
                if maze[xLF-k][y]==3:
                    goal=1
                elif maze[xLF-k][y]==0:
                    front=0
                    break        
            
                

    elif (D=="S"):
        minx=min(xLF,xLB)
        maxx=max(xLF,xLB)
        maxy=max(yLF,yRF)
        miny=min(yLF,yRF)
        for x in range(minx,maxx+1):
            if maze[x][yLF+k]==1:
                left=1
                break
            else:
                left=0
        if left==0:
            for x in range(minx,maxx+1):
                if maze[x][yLF+k]==3:
                    R=1
                    goal=1 
                else:
                    R=0
                    goal=0
                    break

        
        for y in range (miny,maxy+1):
            if maze[xLF+k][y]==1:
                front=1
                break
            else:
                front=0
        if front==0:
            for y in range (miny,maxy+1):
                if maze[xLF+k][y]==3:
                    goal=1
                elif maze[xLF+k][y]==0:
                    front=0
                    break

                
    elif D=="D":
        maxx=max(xLF,xRF)
        minx=min(xLF,xRF)
        maxy=max(yLF,yLB)
        miny=min(yLF,yLB)
        for y in range (miny,maxy+1):
            if maze[xLF-k][y]==1:
                left=1
                break
            else:
                left=0
        if left ==0:
            for y in range (miny,maxy+1):
                if maze[xLF-k][y]==3:
                    goal=1
                    R=1
                else:
                    goal=0
                    R=0
                    break
        for x in range (minx,maxx+1):
            if maze[x][yLF+k]==1:
                front=1
                break
            else:
                front=0
        if front==0:
            for x in range (minx,maxx+1):
                if maze[x][yLF+k]==3:
                    goal=1
                    
                elif maze[x][yLF+k]==0:
                    
                    break
    elif D=="A":
        maxx=max(xLF,xRF)
        minx=min(xLF,xRF)
        maxy=max(yLF,yLB)
        miny=min(yLF,yLB)
        for y in range (miny,maxy+1):
            if maze[xLF+k][y]==1:
                left=1
                break
            else:
                left=0
        if left ==0:
            for y in range (miny,maxy+1):
                if maze[xLF+k][y]==3:
                    goal=1
                    R=1
                else:
                    goal=0
                    R=0
                    break
        for x in range (minx,maxx+1):
            if maze[x][yLF-k]==1:
                front=1
                break
            else:
                front=0
        if front==0:
            for x in range (minx,maxx+1):
                if maze[x][yLF-k]==3:
                    goal=1
                    
                elif maze[x][yLF-k]==0:
                    
                    break
    return (left,front,goal,R)                

def gg(LF,RF,RB,LB,maze,D):
    
    xRF,yRF=RF
    xLF,yLF=LF
    xRB,yRB=RB
    xLB,yLB=LB
    x=0
    b=yLF
    a=xLF
    
    while True:
        if(D=="W" ):
            if maze[xLF][b]==1:

                break
            else:
                b=b-1
                x=x+1
        elif(D=="A"):
            if maze[xLF][b]==1:

                break
            else:
                b=b+1
                x=x+1
        elif(D=="S"):
            if maze[xLF][b]==1:

                break
            else:
                b=b+1
                x=x+1
        elif(D=="D"):
            if maze[xLF][b]==1:

                break
            else:
                b=b+1
                x=x+1
    return x
        
def wallFollower(maze,goal,robot):
    path_list=[]
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
                cmax=max(xRF,xLF,xRB,xLB)
                cmix=min(xRF,xLF,xRB,xLB)
                cmay=max(yRF,yLF,yRB,yLB)
                cmiy=min(yRF,yLF,yRB,yLB)
                cx=(cmax+cmix+1)/2
                cy=(cmay+cmiy+1)/2
                cinter=[cx,cy]
                path_list.append(cinter)
                
                
                #time.sleep(0.05)
                print(O,h,"left=",left,"front=",front,"LF=",LF,"RF=",RF,"RB=",RB,"LB=",LB)
                break
            else:
                LF,RF,RB,LB,h=moveForward(LF,RF,RB,LB)
                xRF,yRF=RF
                xLF,yLF=LF
                xRB,yRB=RB
                xLB,yLB=LB
                path+=h
                cmax=max(xRF,xLF,xRB,xLB)
                cmix=min(xRF,xLF,xRB,xLB)
                cmay=max(yRF,yLF,yRB,yLB)
                cmiy=min(yRF,yLF,yRB,yLB)
                cx=(cmax+cmix+1)/2
                cy=(cmay+cmiy+1)/2
                cinter=[cx,cy]
                path_list.append(cinter)
                
                #time.sleep(0.05)
                print(O,h,"left=",left,"front=",front,"LF=",LF,"RF=",RF,"RB=",RB,"LB=",LB)
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
                cmax=max(xRF,xLF,xRB,xLB)
                cmix=min(xRF,xLF,xRB,xLB)
                cmay=max(yRF,yLF,yRB,yLB)
                cmiy=min(yRF,yLF,yRB,yLB)
                cx=(cmax+cmix+1)/2
                cy=(cmay+cmiy+1)/2
                cinter=[cx,cy]
                path_list.append(cinter)
                #time.sleep(0.05)
                print(O,h,"left=",left,"front=",front,"LF=",LF,"RF=",RF,"RB=",RB,"LB=",LB)
            else:
                (LF,RF,RB,LB)=RCCW(LF,RF,RB,LB)
                xRF,yRF=RF
                xLF,yLF=LF
                xRB,yRB=RB
                xLB,yLB=LB
                #for x in range(0,21):
                LF,RF,RB,LB,h=moveForward(LF,RF,RB,LB)
                xRF,yRF=RF
                xLF,yLF=LF
                xRB,yRB=RB
                xLB,yLB=LB
                path+=h
                
                cmax=max(xRF,xLF,xRB,xLB)
                cmix=min(xRF,xLF,xRB,xLB)
                cmay=max(yRF,yLF,yRB,yLB)
                cmiy=min(yRF,yLF,yRB,yLB)
                cx=(cmax+cmix+1)/2
                cy=(cmay+cmiy+1)/2
                cinter=[cx,cy]
                path_list.append(cinter)
                
                    
                #time.sleep(0.05)
                print(O,h,"left=",left,"front=",front,"LF=",LF,"RF=",RF,"RB=",RB,"LB=",LB) 


        
    path2=path
    while 'EW' in path2 or 'WE' in path2 or 'NS' in path2 or 'SN' in path2 or 'NEN' in path2 or'NWN' in path2 or'WNW' in path2 or 'ENE' in path2 or 'SES' in path2 or 'SWS' in path2 or 'WSW' in path2 or 'ESE' in path2:
        path2=path2.replace('EW','')
        path2=path2.replace('WE','')
        path2=path2.replace('NS','')
        path2=path2.replace('SN','')
        path2=path2.replace('NEN','N')
        path2=path2.replace('NWN','N')
        path2=path2.replace('WNW','W')
        path2=path2.replace('ENE','E')
        path2=path2.replace('SES','S')
        path2=path2.replace('SWS','S')
        path2=path2.replace('WSW','W')
        path2=path2.replace('ESE','E')
        
        
    return path2,path_list


    
def plot_2d_array(array_2d):
    # Unpack the 2D array into x and y coordinates for plotting
    x_coords = [point[0] for point in array_2d]
    y_coords = [point[1] for point in array_2d]

    # Create a scatter plot
    plt.scatter(x_coords, y_coords)

    # Show the plot
    plt.show()

def plot_3d_array(array_3d):
    # Create a new figure and add a 3D subplot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Unpack the 3D array into x, y, and z coordinates for plotting
    x_coords = array_3d[:, 0]
    y_coords = array_3d[:, 1]
    z_coords = array_3d[:, 2]

    # Create a scatter plot
    ax.scatter(x_coords, y_coords, z_coords)

    # Show the plot
    plt.show()
        
def save_array_to_txt(array, filename):
    np.savetxt(filename, array, fmt='%d')

def save_array_to_csv(array_2d, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(array_2d)

def remove_and_shrink_2d(array_2d, target):

    array_2d = [row for row in array_2d if row]
    return array_2d

def copy_2d_array(array_2d):
    return [row[:] for row in array_2d]

def delete_elements(array_2d, targets):
    x1,y1=targets

    for i in range (0,len(array_2d)):
        x,y=array_2d[i]
        if x==x1 and y==y1  :
            array_2d[i]=[6000,6000]
            print("row",i,"deleted",)
            break
    return array_2d

def filter_path(path,maze): 
    F=1
    de=0
    delete_list=[]
    new_path=copy_2d_array(path)
    
    le=len(path)
    for i in range(0,len(path)):
        new_path[i]=path[i]

    for i in range (0,le):
        le=len(path)
        xmain,ymain=path[i]
        print('loding',(i/len(path))*100)
        for j in range(len(path)-1,0,-1):
            
            x,y=path[j]
            
            xc,yc=check_diagonal_points((xmain,ymain),(x,y),maze)
            tt=cheak_points(xc)
            if tt==1:
                F=1
                break
            elif tt==0:
                if len(yc)>=3:
                    del yc[0]
                    del yc[len(yc)-1]
                    for k in range(len(yc)):

                        print("deleting for point",i,"|",(k/len (yc)*100 ),"%")
                        
                        xd,yd=yc.pop(0)
                        
                        
                        
                        new_path=(delete_elements(new_path,(xd,yd)))
                        new_path=remove_and_shrink_2d(new_path,"")
 
    return new_path 

def delt(corners,path):
    new_path=[]
    for i in range(0,len(corners)):
        x=corners[i]
        t=path[x]
        new_path.append(t)
    return new_path

            

if __name__=='__main__':
    '''m=  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],#0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#1
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#2
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#3
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#4
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#5
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#6
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],#7
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],#8
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],#9
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],#10
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],#11
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],#12
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#13
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#14
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#15
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#16
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#17
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
            # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]'''
    m = np.genfromtxt('V4\Map_Gen\map.csv', delimiter=',', skip_header=0)
    ''' robot= [[35,4], #RF
        [35,1],#LF
        [38,4],#RB
        [38,1]]#LB'''
            
           
      
    
    robot=[[1723,123 ],
           [1723, 33],
           [1891,123],
           [1891, 33]]
    
    goal=[
        [11,29],
        [12,29],
        [13,29],
        [14,29],
        [15,29],
        [16,29]
    ]
    
            
    path,path_l=wallFollower(m,goal,robot)

    #path2=filter_path(path_l,m)
    print (path)
    
    g=corners(path)
    print (len(g))
  
    plot_2d_array(path_l)
    
   
 
    
    

    
    

