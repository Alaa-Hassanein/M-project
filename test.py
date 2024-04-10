from pyamaze import maze,agent
myMaze=maze(6,6)
myMaze.CreateMaze()
a=agent(myMaze,shape='arrow')


directions = {'forward': 'N', 'left': 'W', 'back': 'S', 'right': 'E'}
currPos=(myMaze.rows,myMaze.cols)
print(myMaze.maze_map[currPos][directions['left']])



myMaze.run()