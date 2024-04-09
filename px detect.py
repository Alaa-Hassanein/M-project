import cv2

def check_white_square(image_path, center_x, center_y):

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    half_width = 2 
    half_height = 2 
    start_x = int(center_x - half_width)
    start_y = int(center_y - half_height)


    square_region = gray[start_y:start_y+4, start_x:start_x+4]

    if any(pixel != 255 for pixel in square_region.flatten()):
        print("obsticale")
    else:
        print("free")


image_path = "C:/Users/Aditya/OneDrive - YA/Desktop/Semster 6/Mechatronics Project/Resources/maze.jpg"
center_x = 20
center_y = 20  
check_white_square(image_path, center_x, center_y)
