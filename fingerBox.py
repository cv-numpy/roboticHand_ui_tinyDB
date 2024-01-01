import numpy as np


fingers_list = []
x_of_fingers = []

def init(window_width_, window_height_, finger_num_, division_num_, color_=[64, 127, 64]):
    global window_width
    window_width = window_width_
    global window_height
    window_height = window_height_
    global finger_num
    finger_num = finger_num_
    global division_num
    division_num = division_num_
    global color
    color = color_
    global line_size
    line_size = min(window_width, window_height) // 120

    global finger_distance
    finger_distance = int(window_width / (finger_num + 1) )

    global y0
    y0 = int(window_height / 12)
    for i in range(finger_num):
        x_of_fingers.append(finger_distance * (1+i))

    for i in range(finger_num):
        fingers_list.append(fingerBoxes(i))

# Each box contains 4 corner points.
def fingerBoxes(index):
    # box1
    box_x1 = x_of_fingers[index]-finger_distance*(0.4); box_x1 = int(box_x1)
    box_x2 = x_of_fingers[index]+finger_distance*(0.4); box_x2 = int(box_x2)
    box_y1 = y0
    box_y2 = window_height - y0

    height = ( abs(box_y2 - box_y1) + line_size ) / division_num

    stackBoxes = []
    for i in range(division_num):
        stack_box_x1 = (box_x1 + line_size) + line_size
        stack_box_x2 = (box_x2 - line_size) - line_size
        stack_box_y1 = int(box_y1 + height * i)
        stack_box_y2 = int(box_y1 + height * (i+1)) - line_size
        stackBoxes.append( [stack_box_x1, stack_box_x2, stack_box_y1, stack_box_y2] )
    return stackBoxes

def draw_finger_bg(image, index):
    color = np.array([255,255,255], dtype=np.uint8)
    for box in fingers_list[index]:
        # print(box)
        image[box[2]:box[3], box[0]:box[1]] = color