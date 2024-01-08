import numpy as np

servo_num = 8
servoAngles = [90] * servo_num

LENGTH = 480
HEIGHT = 720
# WIDTH = 960
WIDTH = servo_num * 120
bgr_mask = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

import canvas
fingers_list = canvas.init(WIDTH, HEIGHT, servo_num, 19)
canvas.init_draw(bgr_mask)

# OpenCV
import cv2 as cv
w = WIDTH / (servo_num + 1)
h = HEIGHT * (10/12); h = h / 19
h0 = ( int(HEIGHT / 12) + (HEIGHT / 120) )
def which_y(y): 
    y_index = int( (y - h0) / h )
    if y_index>=0 and y_index<=(19-1):
        return y_index
def which_x(x):
    if x > w*0.5 and x < WIDTH-w*0.5:
        x_index = int( (x-w*0.5) / w)
        if x > (x_index+1 - 0.4)*w and x < (x_index+1 + 0.4)*w:
            return x_index

def opencv_callback(event,x,y,flags,param):
    if x > w*0.5 and x < WIDTH-w*0.5:
        print('x index ' + str(which_x(x)) )
        print('y index ' + str(which_y(y)) )

import keyboard
cv.namedWindow('window_name')
cv.setMouseCallback('window_name', opencv_callback)
def display():
    while True:
        cv.imshow('window_name', bgr_mask)
        cv.waitKey(1)
        if keyboard.is_pressed('q'):
            break
    cv.destroyAllWindows()
display()