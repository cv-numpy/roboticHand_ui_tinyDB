servo_num = 5
LENGTH = 480; HEIGHT = LENGTH; WIDTH = LENGTH
LINE_SIZE = LENGTH // 120
# distance between window's edge and edge of hand on the left or right side
x_margin = int(WIDTH / 12)
# All fingers' root position
y0 = int(HEIGHT / 12)
# height and width of the finger box 
y_unit = int(HEIGHT/4)
x_unit = int(WIDTH/6)

# x coordinate of each finger's middle line
x_of_fingers = []
x0 = int(WIDTH / 6)
for i in range(servo_num):
    x_of_fingers.append(x0+i*x_unit)

# finger's width
w1 = int(WIDTH / 8 / 2)
w2 = int(WIDTH / 7 / 2)
w3 = int(WIDTH / 6 / 2)
# Each box contains 4 corner points.
def fingerBoxes(finger_index):
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



import numpy as np
def box_fill(image, box, color = [255, 255, 255]):
    color = np.array(color, dtype=np.uint8)
    image[box[2]:box[3], box[0]:box[1]] = color
    return image

def borderLine(fingerBox):
    box_x1, box_x2, box_y1, box_y2 = fingerBox

    lineBox_left = [box_x1, box_x1+LINE_SIZE, box_y1, box_y2]
    lineBox_right = [box_x2-LINE_SIZE, box_x2, box_y1, box_y2]
    lineBox_top = [box_x1, box_x2, box_y1, box_y1+LINE_SIZE//2]
    lineBox_bottom = [box_x1, box_x2, box_y2-LINE_SIZE//2, box_y2]
    return lineBox_left, lineBox_right, lineBox_top, lineBox_bottom


def stackBoxes_in_box(box, num = 3):
    box_x1, box_x2, box_y1, box_y2 = box
    box_y1 = int(box_y1 + LINE_SIZE* 1.5)
    box_y2 = int(box_y2 - LINE_SIZE* 1.5)

    height = ( abs(box_y2 - box_y1) + LINE_SIZE ) / num

    stackBoxes = []
    for i in range(num):
        stack_box_x1 = (box_x1 + LINE_SIZE) + LINE_SIZE
        stack_box_x2 = (box_x2 - LINE_SIZE) - LINE_SIZE
        stack_box_y1 = int(box_y1 + height * i)
        stack_box_y2 = int(box_y1 + height * (i+1)) - LINE_SIZE
        stackBoxes.append( [stack_box_x1, stack_box_x2, stack_box_y1, stack_box_y2] )
    return stackBoxes





bgr_mask = np.zeros((LENGTH, LENGTH, 3), dtype=np.uint8)
fingers_boxes = []
# Create hand Dashboard
def dashboard(color = [255, 255, 255]):
    image = np.copy(bgr_mask)
    for finger_index in range(servo_num):
        box1_box2_box3 = fingerBoxes(finger_index)
        for box in box1_box2_box3:
            lineBoxes = borderLine(box)
            for lineBox in lineBoxes:
                image = box_fill(image, lineBox, color)

        box1_box2_box3 = fingerBoxes(finger_index)

        finger_boxes_5 = []

        # Distal and intermediate phalanges
        for box in box1_box2_box3[:2]:
            stack_boxes = stackBoxes_in_box(box, 3*2)
            for stack_box in stack_boxes:
                finger_boxes_5.append(stack_box)
                image = box_fill(image, stack_box, color)

        # Proximal phalanges
        stack_boxes = stackBoxes_in_box(box1_box2_box3[-1], 4*2)
        for stack_box in stack_boxes:
            finger_boxes_5.append(stack_box)
            image = box_fill(image, stack_box, color)

        fingers_boxes.append(finger_boxes_5)

    return image     


dashBoard_color = [64, 127, 64]
bgr_mask = dashboard(dashBoard_color)


image_for_showing = np.copy(bgr_mask)
import cv2 as cv
cv.namedWindow('windows1')
while(1):
 cv.imshow('windows1',image_for_showing)
 if cv.waitKey(20) & 0xFF == 27:
    break
cv.destroyAllWindows()