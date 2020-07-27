import cv2
import numpy as np
import pyautogui as auto
import imutils

#####################################################
def move_mouse(cx,cy):
    if (cy - 92) > 0 and (cx - 48) > 0:
        auto.moveTo((cy - 92) * 3, (cx - 48) * 2)
    elif (cy - 92) <= 0:
        auto.moveTo(0, (cx - 48) * 2)
    elif (cx - 48) <= 0:
        auto.moveTo((cy - 92) * 3, 0)
    else:
        pass

#####################################################
def click_mouse(cx,cy):
    if (cy - 92) > 0 and (cx - 48) > 0:
        auto.mouseDown((cy - 92) * 3, (cx - 48) * 2)
    elif (cy - 92) <= 0:
        auto.mouseDown(0, (cx - 48) * 2)
    elif (cx - 48) <= 0:
        auto.mouseDown((cy - 92) * 3, 0)
    else:
        auto.mouseUp(cy, cx)
        pass

######################################################
low_red = np.array([1, 173, 141])
high_red = np.array([179, 255, 255])
low_green = np.array([68, 255, 72])
high_green = np.array([179, 255, 255])
flag = 0

#######################################################
def nothing(x):
    pass

#######################################################
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    frame_red = cv2.flip(frame, 1)
    frame_green = cv2.flip(frame, 1)
    hsv_red = cv2.cvtColor(frame_red, cv2.COLOR_BGR2HSV)
    hsv_green = cv2.cvtColor(frame_green, cv2.COLOR_BGR2HSV)
    #low_color = np.array([l_h, l_s, l_v])
    #high_color = np.array([h_h, h_s, h_v])


    mask_green = cv2.inRange(hsv_green, low_green, high_green)
    mask_red = cv2.inRange(hsv_red, low_red, high_red)
    median_red = cv2.medianBlur(mask_red, 7)
    median_green = cv2.medianBlur(mask_green, 7)
    cnts_red = cv2.findContours(median_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts_green = cv2.findContours(median_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts_red = imutils.grab_contours(cnts_red)
    cnts_green = imutils.grab_contours(cnts_green)



    for c in cnts_red:
        cy_red = 0
        cx_red = 0
        area = cv2.contourArea(c)
        cv2.drawContours(frame, [c], -1, (0,255,0), 2)
        print(len(cnts_red))

        M = cv2.moments(c)
        if M["m00"] != 0:
            cx_red = int(M["m10"]/M["m00"])
            cy_red = int(M["m01"]/ M["m00"])
            #print(cx)
            #print(cy)
            auto.FAILSAFE = False
            #move_mouse(cy,cx)
            for c in cnts_green:
                cy_green = 0
                cx_gren = 0
                area = cv2.contourArea(c)
                cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
                print(len(cnts_green))

                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx_green = int(M["m10"] / M["m00"])
                    cy_green = int(M["m01"] / M["m00"])
                    # print(cx)
                    # print(cy)
                    auto.FAILSAFE = False
                    # move_mouse(cy,cx)
                    cx = (cx_red + cx_green) / 2
                    cy = (cy_red + cy_green) / 2
                    print(str(cx)+","+str(cy))

    #cv2.imshow("mask", mask)
    frame = cv2.rectangle(frame, (93, 48), (548, 432), (255,0,0),  2)
    frame = cv2.putText(frame, "Move Pen In Rectangle", (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
    cv2.imshow("median_red", median_red)
    cv2.imshow("median_green", median_green)
    #cv2.imshow("frame", frame)



    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
