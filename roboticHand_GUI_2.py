import PySimpleGUI as sg
# [ 2D Hand Animation ]
# Each finger width: `1/6` of image width
# Fingers y: `1/12` of image -> `11/12` of image
LENGTH = 640
HEIGHT = LENGTH; WIDTH = LENGTH
LINE_SIZE = LENGTH // 120
dashBoard_color = [64, 127, 64]

import numpy as np
import cv2 as cv

# from adafruit_servokit import ServoKit
# kit = ServoKit(channels=16)

servo_num = 10
angle_locations = [0] * servo_num

# kit.servo[0].angle = 0
# kit.servo[0].angle = 180

gray_mask = np.zeros((LENGTH, LENGTH*2), dtype=np.uint8)
bgr_mask = np.zeros((LENGTH, LENGTH*2, 3), dtype=np.uint8)

lengthes = [
    LENGTH,
    LENGTH/2,
    LENGTH/3,
    LENGTH/4,
    LENGTH/5,
    LENGTH/6,
    LENGTH/7,
    LENGTH/8,
    LENGTH/9,
    LENGTH/10,
    LENGTH/11,
    LENGTH/12,
    LENGTH/13,
    LENGTH/14,
    LENGTH/15,
    LENGTH/16,
]

# botton y position for all fingers' root position
y0 = int(HEIGHT / 12) # see on the top about a finger's length

# height and widht of one of finger's three box 
y_unit = int(HEIGHT/4)
x_unit = int(WIDTH/6) # see on the top about a finger's width

# fingers middle line's x coordinates
x_of_fingers = []
x0 = int(WIDTH / 6)
for i in range(10):
    x_of_fingers.append(x0+i*x_unit)

# Half of the Widths for a finger's different joints
w1 = int(WIDTH / 8 / 2)
w2 = int(WIDTH / 7 / 2)
w3 = int(WIDTH / 6 / 2)

# distance between image boundary and left or right side edge of hand
x_margin = int(WIDTH / 12)

    
def fingerBoxes(finger_index):
    # Each box contains 4 corner points.

    # a finger's average x coordinate
    x = x_of_fingers[finger_index]
    
    # box1
    box1_x1 = x-w1; box1_x2 = x+w1
    box1_y1 = y0; box1_y2 = box1_y1+y_unit

    # box2
    box2_x1 = x-w2; box2_x2 = x+w2
    box2_y1 = y0+y_unit; box2_y2 = box2_y1+y_unit

    # box3
    box3_x1 = x-w3 + LINE_SIZE//2; box3_x2 = x+w3 - LINE_SIZE//2
    box3_y1 = y0+2*y_unit; box3_y2 = LENGTH-y0 

    box1 = [box1_x1, box1_x2, box1_y1, box1_y2]
    box2 = [box2_x1, box2_x2, box2_y1, box2_y2]
    box3 = [box3_x1, box3_x2, box3_y1, box3_y2]
    return box1, box2, box3

def box_fill(image, box, color = [255, 255, 255]):
    color = np.array(color, dtype=np.uint8)
    image[box[2]:box[3], box[0]:box[1]] = color
    return image

def contourLineBox(fingerBox):
    box_x1, box_x2, box_y1, box_y2 = fingerBox

    lineBox_left = [box_x1, box_x1+LINE_SIZE, box_y1, box_y2]
    lineBox_right = [box_x2-LINE_SIZE, box_x2, box_y1, box_y2]

    lineBox_top = [box_x1, box_x2, box_y1, box_y1+LINE_SIZE//2]
    lineBox_bottom = [box_x1, box_x2, box_y2-LINE_SIZE//2, box_y2]

    return lineBox_left, lineBox_right, lineBox_top, lineBox_bottom
    
def stackBoxes_in_box(box, num = 3):
    box_x1, box_x2, box_y1, box_y2 = box

    box_y1 = box_y1 + LINE_SIZE//2 + LINE_SIZE
    box_y2 = box_y2 - LINE_SIZE//2

    # height = int( abs(box_y2 - box_y1) / num )
    # not trim out decimal number
    height = abs(box_y2 - box_y1) / num

    stackBoxes = []
    for i in range(num):
        stack_box_x1 = (box_x1 + LINE_SIZE) + LINE_SIZE
        stack_box_x2 = (box_x2 - LINE_SIZE) - LINE_SIZE
        stack_box_y1 = int(box_y1 + height * i)
        stack_box_y2 = int(box_y1 + height * (i+1) - LINE_SIZE)
        stackBoxes.append( [stack_box_x1, stack_box_x2, stack_box_y1, stack_box_y2] )
    return stackBoxes

# draw a finger's contour line
def fingering(image, finger_index, color=[255, 255, 255]):
    box1_box2_box3 = fingerBoxes(finger_index)
    for box in box1_box2_box3:
        lineBoxes = contourLineBox(box)
        for lineBox in lineBoxes:
            image = box_fill(image, lineBox, color)
    return image
    

def update_angles(index, change_of_angle):
    old_angle = angle_locations[index]
    new_angle = old_angle + change_of_angle
    angle_locations[index] = new_angle

    # servokit[index] = new_angle

value_for_update = 10

######## Opencv mouse callback function
def opencv_callback(event,x,y,flags,param):
 fingers = ['thumb', 'index finger', 'middle finger', 'ring finger', 'little finger']
 if x > x_margin and x < WIDTH*2-x_margin:
    # index of the finger that has been clicked
    index = int( (x-x_margin) / x_unit)

    global image_for_showing
    if event == cv.EVENT_LBUTTONDOWN:
        # image_for_showing = redshift_finger[index]
        if angle_locations[index] <= 180 - value_for_update:
            update_angles(index, value_for_update)
            angle = angle_locations[index]

            for i in range(10):
                image_for_showing = box_fill(image_for_showing, fingers_boxes[index][i], (0,0,0))
            for i in range(int(angle/10)):
                image_for_showing = box_fill(image_for_showing, fingers_boxes[index][9-i], dashBoard_color)
        print('angles updated: ' + str(angle_locations))
    if event == cv.EVENT_RBUTTONDOWN:
        # image_for_showing = blueshift_finger[index]
        if angle_locations[index] >= value_for_update:
            update_angles(index, -value_for_update)
            angle = angle_locations[index]
            for i in range(10):
                image_for_showing = box_fill(image_for_showing, fingers_boxes[index][i], (0,0,0))
            for i in range(int(angle/10)):
                image_for_showing = box_fill(image_for_showing, fingers_boxes[index][9-i], dashBoard_color)

        print('angles updated: ' + str(angle_locations))

    # if event == cv.EVENT_MOUSEWHEEL:
        
fingers_boxes = []

# Create hand Dashboard
def dashboard(color = [255, 255, 255]):
    image = np.copy(bgr_mask)
    for finger_index in range(10):
        image = fingering(image, finger_index)

        box1_box2_box3 = fingerBoxes(finger_index)

        finger_boxes_10 = []

        # Distal and intermediate phalanges
        for box in box1_box2_box3[:2]:
            stack_boxes = stackBoxes_in_box(box)
            for stack_box in stack_boxes:
                finger_boxes_10.append(stack_box)
                image = box_fill(image, stack_box, color)

        # Proximal phalanges
        stack_boxes = stackBoxes_in_box(box1_box2_box3[-1], 4)
        for stack_box in stack_boxes:
            finger_boxes_10.append(stack_box)
            image = box_fill(image, stack_box, color)

        fingers_boxes.append(finger_boxes_10)

    return image     
bgr_mask = dashboard(dashBoard_color)


# Show which finger user have just clicked
redshift_finger = []
blueshift_finger = []

# using opencv bgr colorspace
red = [0, 0, 255]; blue = [255, 0, 0]
for finger_index in range(10):
    redfinger = np.copy(bgr_mask)
    redfinger = fingering(redfinger, finger_index, red)
    redshift_finger.append(redfinger)
    
    bluefinger = np.copy(bgr_mask)
    bluefinger = fingering(bluefinger, finger_index, blue)
    blueshift_finger.append(bluefinger)

# for i in range(len(angle_locations)):
#     update_angles(kit, i, 0)

image_for_showing = np.copy(bgr_mask)
# cv.namedWindow('windows1', cv.WINDOW_NORMAL)
cv.namedWindow('windows1')
cv.setMouseCallback('windows1', opencv_callback)
while(1):
 cv.imshow('windows1',image_for_showing)
 if cv.waitKey(20) & 0xFF == 27:
    break
cv.destroyAllWindows()