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

import cv2 as cv
# OpenCV
d = WIDTH / (servo_num + 1)
def opencv_callback(event,x,y,flags,param):
    if x > d*0.5 and x < WIDTH-d*0.5:
        index = int( (x-d*0.5) / d)

import keyboard
cv.namedWindow('window_name')
# cv.setMouseCallback('window_name', opencv_callback)
def display():
    while True:
        cv.imshow('window_name', bgr_mask)
        cv.waitKey(1)
        if keyboard.is_pressed('q'):
            break
    cv.destroyAllWindows()
display()