from pyamaze import maze,COLOR,agent
m=maze(10,10)
m.CreateMaze(theme=COLOR.light)
a=agent(m)
m.run()