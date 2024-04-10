from pyamaze import maze,agent
myMaze=maze(6,6)
myMaze.CreateMaze()
a=agent(myMaze,shape='arrow')


print(myMaze.maze_map)



myMaze.run()