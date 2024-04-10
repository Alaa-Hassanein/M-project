from pyamaze import maze
m=maze(6,6)
m.CreateMaze()
directions={'forward':'N','left':'W','back':'S','right':'E'}
d = {(1,5): 'val1', 'key2': 'val2', 'key3': 'val3'}
currPos=(m.rows,m.cols)
print(currPos)
if m.maze_map[currPos][directions['left']]== 0:
    print("yes")