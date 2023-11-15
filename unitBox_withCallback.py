# [ 2D Hand Animation ]
# Each finger width: `1/6` of image width
# Fingers y: `1/8` of image -> `7/8` of image
LENGTH = 480
HEIGHT = LENGTH; WIDTH = LENGTH

import numpy as np
import cv2 as cv

# import color as u8
# colors = [u8.red, u8.green, u8.blue, u8.yellow, u8.purple]

gray_mask = np.zeros((LENGTH, LENGTH), dtype=np.uint8)
bgr_mask = np.zeros((LENGTH, LENGTH, 3), dtype=np.uint8)

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


def box_gray(image, box, color = 255):
    image[box[2]:box[3], box[0]:box[1]] = color
    return image
def box_bgr(image, box, color = [255, 255, 255]):
    color = np.array(color, dtype=np.uint8)
    image[box[2]:box[3], box[0]:box[1]] = color
    return image


def fingering(image, finger_index, color):
    dims = image.ndim
    box1_box2_box3 = fingerBoxes(finger_index)
    for box in box1_box2_box3:
        if dims == 2:
            image = box_gray(image, box, color)
        elif dims == 3:
            image = box_bgr(image, box, color)
    return image
        
def mask_gray():
    image = np.copy(gray_mask)
    print(image.shape())
    for finger_index in range(5):
        # for each finger
        image = fingering(image, finger_index, 255)
    return image
def mask_bgr():
    image = np.copy(bgr_mask)
    for finger_index in range(5):
        # for each finger
        image = fingering(image, finger_index, [255, 255, 255])
    return image     

# mouse callback function
def opencv_callback(event,x,y,flags,param):
 fingers = ['thumb', 'index finger', 'middle finger', 'ring finger', 'little finger']
 if x > x_margin and x < WIDTH-x_margin:
    # index of the finger that has been clicked
    index = int( (x-x_margin) / x_unit)

    global image_for_showing
    if event == cv.EVENT_LBUTTONDOWN:
        image_for_showing = redshift_finger[index]
        print('left button')
        print(fingers[index] + ' angle increased.')
    if event == cv.EVENT_RBUTTONDOWN:
        image_for_showing = blueshift_finger[index]
        print('right button')
        print(fingers[index] + ' angle decreased.')

redshift_finger = []
blueshift_finger = []
bgr_mask = mask_bgr()
for finger_index in range(5):
    # using opencv bgr colorspace
    red = [0, 0, 255]; blue = [255, 0, 0]
    redfinger = np.copy(bgr_mask)
    redfinger = fingering(redfinger, finger_index, red)
    redshift_finger.append(redfinger)
    
    bluefinger = np.copy(bgr_mask)
    bluefinger = fingering(bluefinger, finger_index, blue)
    blueshift_finger.append(bluefinger)

# global image_for_showing
image_for_showing = np.copy(bgr_mask)
cv.namedWindow('windows1', cv.WINDOW_NORMAL)
cv.setMouseCallback('windows1', opencv_callback)
while(1):
 cv.imshow('windows1',image_for_showing)
 if cv.waitKey(20) & 0xFF == 27:
    break
cv.destroyAllWindows()
