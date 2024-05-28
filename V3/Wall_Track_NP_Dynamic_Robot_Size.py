from time import sleep
import numpy as np

def RCW(direction, left_robot_back, left_robot_front, right_robot_back, right_robot_front):
    k=list(direction.keys())
    v=list(direction.values())
    v_rotated=[v[-1]]+v[:-1]
    direction=dict(zip(k,v_rotated)) 

    return direction

def RCCW(direction):
    k=list(direction.keys())
    v=list(direction.values())
    v_rotated=v[1:]+[v[0]]
    direction=dict(zip(k,v_rotated))
    return direction 

def robot_size(maze):
    width = -1
    x_c = 0
    left_robot_back = [0, 0]
    for x in maze:
        y_c = 0
        x_c += 1
        for y in x:
            y_c += 1
            if y == 2 and left_robot_back == [0, 0]:
                print("Robot found!")
                width += 1
                if maze[x_c-1][y_c] != 2:
                    if left_robot_back != []:
                        print(width)
                        left_robot_back = [x_c-1, y_c-1]
                        print(left_robot_back)
                        break

    right_robot_back = [left_robot_back[0], left_robot_back[1] - width]
    right_robot_front = [left_robot_back[0] + width, left_robot_back[1] - width]
    left_robot_front = [left_robot_back[0] + width, left_robot_back[1]]
    current_position = []
    x_c = 0
    for x in maze:
        y_c = 0
        for y in x:
            if y == 2:
                current_position.append([x_c, y_c])
            y_c += 1
        x_c += 1
    print(left_robot_back, left_robot_front, right_robot_back, right_robot_front, current_position)

    return left_robot_back, left_robot_front, right_robot_back, right_robot_front, current_position
                


def check_surr(current_position):
    if direction['forward'] == 'N':
        left_position = [current_position[0], current_position[1] - 1]
        front_position = [current_position[0] - 1, current_position[1]]
    elif direction['forward'] == 'S':
        left_position = [current_position[0], current_position[1] + 1]
        front_position = [current_position[0] + 1, current_position[1]]
    elif direction['forward'] == 'E':
        left_position = [current_position[0] - 1, current_position[1]]
        front_position = [current_position[0], current_position[1] + 1]
    elif direction['forward'] == 'W':
        left_position = [current_position[0] + 1, current_position[1]]
        front_position = [current_position[0], current_position[1] - 1]
    return left_position, front_position


def move_forward(current_position):
    if direction['forward'] == 'N':
        current_position = [current_position[0] - 1, current_position[1]]
    elif direction['forward'] == 'S':
        current_position = [current_position[0] + 1, current_position[1]]
    elif direction['forward'] == 'E':
        current_position = [current_position[0], current_position[1] + 1]
    elif direction['forward'] == 'W':
        current_position = [current_position[0], current_position[1] - 1]
    print(current_position)
    return current_position

    

def print_maze(maze):
    for x in maze:
        print(x)
    print("\n")

def wall_track(start, end, maze):
    global direction
    direction = {'forward':'S','left':'E','back':'N','right':'W'}
    current_position = list(start)
    previous_position = current_position
    path = []
    path.append([current_position, direction['forward']])
    while current_position != list(end):
        left_position, front_position = check_surr(current_position)
        # Check to the left of the current position
        if maze[left_position[0]][left_position[1]] == 0 or maze[left_position[0]][left_position[1]] == 3:
            direction = RCCW(direction)
            path.append([current_position, direction['forward']])
            print(direction['forward'])
            print(path)
            previous_position = current_position
            current_position = move_forward(current_position)
            path.append([current_position, direction['forward']])
            maze[current_position[0]][current_position[1]] = 2
            maze[previous_position[0]][previous_position[1]] = 0
            sleep(1)
            print_maze(maze)
        if maze[left_position[0]][left_position[1]] == 1 and maze[front_position[0]][front_position[1]] == 0:
            print(current_position)
            previous_position = current_position
            current_position = move_forward(current_position)
            path.append([current_position, direction['forward']])
            print(path)
            maze[current_position[0]][current_position[1]] = 2
            maze[previous_position[0]][previous_position[1]] = 0
            sleep(1)
            print_maze(maze)
        if maze[left_position[0]][left_position[1]] == 1 and maze[front_position[0]][front_position[1]] == 1:
            direction = RCW(direction)
            path.append([current_position, direction['forward']])
            print(direction['forward'])
            print(path)
            sleep(1)
            print_maze(maze)
    
    path.append([current_position, direction['forward']])
    print("Exit Found!")










def main():
    # Read the CSV file into a numpy array
    data_array = np.genfromtxt('site.csv', delimiter=',')
    maze = data_array
<<<<<<< HEAD
    # Display the result
    #print(data_array)

    """sex =[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 0, 0, 0, 0, 0, 0, 1],
            [1, 2, 2, 0, 0, 0, 0, 1, 1, 1],
            [1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 1, 1, 0, 0, 1, 0, 0, 3],
            [1, 0, 0, 1, 0, 0, 1, 1, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]"""

    start = [0, 0]
    end = [4, 9]
    #wall_track(start, end, maze)
=======
    wall_track(maze)
>>>>>>> d68423fcf84d321f49bd343541722607c0d33a82
    robot_size(maze)

if __name__ == '__main__':
    main()