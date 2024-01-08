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
    return fingers_list

color_white = np.array([255,255,255], dtype=np.uint8)
battery_green = np.array([64, 127, 64], dtype=np.uint8)
def init_draw(image):
    for fingerIndex in range(finger_num):
        i = 0
        for box in fingers_list[fingerIndex]:
            # draw grid
            image[box[2]:box[3], box[0]:box[1]] = color_white

            if i == int(19/2):
                image[box[2]:box[3], box[0]:box[1]] = battery_green
            i = i+1
            
        # draw border line for each finger
        draw_contourLine(image, fingerIndex)

# boxes stack of the finger
def fingerBoxes(index):
    # finger box
    box_x1 = x_of_fingers[index]-finger_distance*(0.4); box_x1 = int(box_x1)
    box_x2 = x_of_fingers[index]+finger_distance*(0.4); box_x2 = int(box_x2)
    
    box_y1 = y0
    box_y2 = window_height - y0
    box_y1 = box_y1 + line_size//2 + line_size
    box_y2 = box_y2 - line_size//2 - line_size

    # height of unit box
    height = ( abs(box_y2 - box_y1) + line_size ) / division_num

    stackBoxes = []
    for i in range(division_num):
        stack_box_x1 = (box_x1 + line_size) + line_size
        stack_box_x2 = (box_x2 - line_size) - line_size
        stack_box_y1 = int(box_y1 + height * i)
        stack_box_y2 = int(box_y1 + height * (i+1)) - line_size
        stackBoxes.append( [stack_box_x1, stack_box_x2, stack_box_y1, stack_box_y2] )
    return stackBoxes

def fill_box(image, box, color = [255, 255, 255]):
    color = np.array(color, dtype=np.uint8)
    image[box[2]:box[3], box[0]:box[1]] = color

def contourLineBox(index):
    # finger box
    box_x1 = x_of_fingers[index]-finger_distance*(0.4); box_x1 = int(box_x1)
    box_x2 = x_of_fingers[index]+finger_distance*(0.4); box_x2 = int(box_x2)
    box_y1 = y0
    box_y2 = window_height - y0

    lineBox_left = [box_x1, box_x1+line_size, box_y1, box_y2]
    lineBox_right = [box_x2-line_size, box_x2, box_y1, box_y2]

    lineBox_top = [box_x1, box_x2, box_y1, box_y1+line_size//2]
    lineBox_bottom = [box_x1, box_x2, box_y2-line_size//2, box_y2]

    return lineBox_left, lineBox_right, lineBox_top, lineBox_bottom

def draw_contourLine(image, index, color = [255, 255, 255]):
    lineBox_l, lineBox_r, lineBox_t, lineBox_b = contourLineBox(index)
    fill_box(image, lineBox_l, color)
    fill_box(image, lineBox_r, color)
    fill_box(image, lineBox_t, color)
    fill_box(image, lineBox_b, color)