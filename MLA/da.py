m=[[1,4],[5,6],[7,8]]


def print_back_to_front(lst):
    for item in reversed(lst):
        print(item)


def copy_2d_array(array_2d):
    return [row[:] for row in array_2d]
def delete_elements(array_2d, targets):
    return [[element for element in row if element not in targets] for row in array_2d]
def remove_free_indices_2d(array_2d, free_value=""):
    return [[element for element in row if element != free_value] for row in array_2d]
def remove_and_shrink_2d(array_2d, target):
    array_2d = [row for row in array_2d if row]
    return array_2d

def delete_elements(array_2d, targets):
    xf,yf=targets
    for i in range (0,len(array_2d)):
        x,y=array_2d[i]
        if x==xf and y==yf  :
            del  array_2d[i]
            print("row",i,"deleted",)
            break
    return array_2d




def corners(arr):
    x=[]
    for i in range (0,len(arr)-1):
        if arr [i]==[i+1]:
            x.append(i)

    return x

def delete_points_between(array_2d, point1):
    x1,y1=point1
    
    for i in range (0,len(array_2d)):
        x,y=array_2d[i]
        if x==x1 and y==y1  :
            array_2d[i]=[99999999999,99999999999]
            
            print("row",i,"deleted",)
            break
    
    return array_2d
m = [[1, 2], [3, 4], [5, 6], [7, 8]]  # Define m before trying to print it
print(m)
m = delete_points_between(m, (1,2))
print(m)
