from pyamaze import maze, agent


def RCW():
    global directions
    k = list(directions.keys())
    v = list(directions.values())
    v_rotated=[v[-1]]+v[:-1]
    directions = dict(zip(k, v_rotated))


def RCCW():
    global directions
    k = list(directions.keys())
    v = list(directions.values())
    v_rotated=v[1:]+[v[0]]
    
    directions = dict(zip(k, v_rotated))


def MoveForward(pos, maze):
    if directions['forward'] == 'N':
        new_pos = (pos[0] - 1, pos[1])
        if 0 <= new_pos[0] < maze.rows and 0 <= new_pos[1] < maze.cols:
            print (new_pos)
            return new_pos, 'N'
        else:
            print (new_pos)
            return pos, directions['forward']  # Stay in place if at border
    if directions['forward'] == 'E':
        new_pos = (pos[0], pos[1] + 1)
        if 0 <= new_pos[0] < maze.rows and 0 <= new_pos[1] < maze.cols:
            print (new_pos)
            return new_pos, 'E'
        else:
            print (new_pos)
            return pos, directions['forward']  # Stay in place if at border
    if directions['forward'] == 'S':
        new_pos = (pos[0] + 1, pos[1])
        if 0 <= new_pos[0] < maze.rows and 0 <= new_pos[1] < maze.cols:
            print (new_pos)
            return new_pos, 'S'
        else:
            print (new_pos)
            return pos, directions['forward']  # Stay in place if at border
    if directions['forward'] == 'W':
        new_pos = (pos[0], pos[1] - 1)
        if 0 <= new_pos[0] < maze.rows and 0 <= new_pos[1] < maze.cols:
            print (new_pos)
            return new_pos, 'W'
        else:
            print (new_pos)
            return pos, directions['forward']  # Stay in place if at border


def Wall_Follower(F):
    global directions
    directions = {'forward': 'N', 'left': 'W', 'back': 'S', 'right': 'E'}
<<<<<<< HEAD
    currPos = (F.rows,F.cols)  # Start at (1, 1)  **assuming valid starting position**
    path = ''
    while True:
        if currPos == (1, 1):
            print("gg")
            break

        # Check if there's a wall on the left relative to current direction
        if F.maze_map[currPos][directions['left']] == 0:
            if F.maze_map[currPos][directions['forward']] == 0:
                # Dead end detected! Try turning around (replace with your strategy)
                
                RCW()  # Turn around (alternative action)
            else:
                currPos, D = MoveForward(currPos, F)
                path += D
        else:
            RCCW()
            currPos, D = MoveForward(currPos, F)
            path += D
=======
    currPos = (F.cols,F.rows)  # Start at (1, 1)  **assuming valid starting position**
    path = ''
    while True:
        if currPos == (2, 2):
            break

        # Check if there's a wall on the left relative to current direction
        if F.maze_map[currPos][directions['left']] == 0 and F.maze_map[currPos][directions['forward']] == 0 \
            and F.maze_map[currPos][directions['right']] == 1 and F.maze_map[currPos][directions['left']] == 1:
            # Dead end detected! Try turning around
            RCW()
            RCW()
            if F.maze_map[currPos][directions['left']] == 0:  # This section is redundant
                if F.maze_map[currPos][directions['forward']] == 0:
                    # Dead end detected! (already checked earlier)
                    RCW()
                    RCW()
                else:
                    currPos, D = MoveForward(currPos, F)
                    path += D

>>>>>>> f7f58cc9c2bd291842151e775b279aacc58e674a

    return path



if __name__ == '__main__':
    myMaze = maze(6, 6)
    myMaze.CreateMaze()
    a = agent(myMaze, shape='arrow')

    path = Wall_Follower(myMaze)

    myMaze.tracePath({a: path})

    myMaze.run()
