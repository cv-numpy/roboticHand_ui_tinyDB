# [ 2D Hand Animation ]
# Each finger width: `1/6` of image width
# Fingers y: `1/8` of image -> `7/8` of image
LENGTH = 480
HEIGHT = LENGTH; WIDTH = LENGTH

import numpy as np
import cv2 as cv

import color as u8
colors = [u8.red, u8.green, u8.blue, u8.yellow, u8.purple]

mask = np.zeros((LENGTH, LENGTH), dtype=np.uint8)

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
y0 = int(HEIGHT / 8) # see on the top about a finger's length

# height and widht of one of finger's three box 
y_unit = int(HEIGHT/4)
x_unit = int(WIDTH/6) # see on the top about a finger's width

# fingers middle line's x coordinates
x_of_fingers = []
x0 = int(WIDTH / 6)
for i in range(5):
    x_of_fingers.append(x0+i*x_unit)

# Half of the Widths for a finger's different joints
w1 = int(WIDTH / 8 / 2)
w2 = int(WIDTH / 7 / 2)
w3 = int(WIDTH / 6 / 2)

# distance between image boundary and left or right side edge of hand
x_margin = int(WIDTH / 12)

    
# one hand => 5 fingers
# one finger => 3 boxes
def fingerBoxes(finger_index):
    # Each box contains 4 corner points.

    # box1  box1  box1 ]
    # box2  box2  box2 ] finger_part
    # box3  box3  box3 ]
    # palm  palm  palm ]
    # palm  palm  palm ] hand

    # a finger's average x coordinate
    x = x_of_fingers[finger_index]
    
    # box1
    box1_x1 = x-w1; box1_x2 = x+w1
    box1_y1 = y0; box1_y2 = box1_y1+y_unit

    # box2
    box2_x1 = x-w2; box2_x2 = x+w2
    box2_y1 = y0+y_unit; box2_y2 = box2_y1+y_unit

    # box3
    box3_x1 = x-w3; box3_x2 = x+w3
    box3_y1 = y0+2*y_unit; box3_y2 = box3_y1+y_unit

    box1 = [box1_x1, box1_x2, box1_y1, box1_y2]
    box2 = [box2_x1, box2_x2, box2_y1, box2_y2]
    box3 = [box3_x1, box3_x2, box3_y1, box3_y2]
    return box1, box2, box3

def mask_Generator():pass

# Test
for i in range(5):
    box1, box2, box3 = fingerBoxes(i)

    mask[box1[2]:box1[3], box1[0]:box1[1]] = 255
    mask[box2[2]:box2[3], box2[0]:box2[1]] = 255
    mask[box3[2]:box3[3], box3[0]:box3[1]] = 255


# mouse callback function
def draw_circle(event,x,y,flags,param):
 fingers = ['thumb', 'index finger', 'middle finger', 'ring finger', 'little finger']
 if x > x_margin and x < WIDTH-x_margin:
    index = int( (x-x_margin) / x_unit)
    if event == cv.EVENT_LBUTTONDOWN:
        print('left button')
        print(fingers[index] + ' angle increased.')
    if event == cv.EVENT_RBUTTONDOWN:
        print('right button')
        print(fingers[index] + ' angle decreased.')

cv.namedWindow('image2')
cv.setMouseCallback('image2', draw_circle)
while(1):
 cv.imshow('image2',mask)
 if cv.waitKey(20) & 0xFF == 27:
    break
cv.destroyAllWindows()