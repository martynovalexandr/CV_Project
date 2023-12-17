import math as m
import numpy as np
import cv2


def red_brick(i, area_in):
    img = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)

    lower1 = np.array([0, 150, 100])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([160, 150, 100])
    upper2 = np.array([179, 255, 255])

    mask1 = cv2.inRange(img, lower1, upper1)
    mask2 = cv2.inRange(img, lower2, upper2)
    full_mask = mask1 + mask2
    img_masked = cv2.bitwise_and(img, img, mask=full_mask)

    gray = cv2.cvtColor(img_masked, cv2.COLOR_BGR2GRAY)
    red_area = i.shape[0] * i.shape[1]
    for k in range(i.shape[0]):
        for j in range(i.shape[1]):
            if gray[k, j] == 0:
                red_area -= 1
    print(red_area / area_in)
    if 0.5 < red_area / area_in < 0.8:
        return True
    cv2.imshow("Image", gray)
    cv2.waitKey(0)


picture_name = input()
image = cv2.imread("test_images/"+picture_name+".jpeg")
img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find circles
circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.3, 100)
# Get the (x, y, r) as integers
circles = np.round(circles[0, :]).astype("int")

# the number of pixels in the circle
n = image.shape[0] * image.shape[1]
# make the background green
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        if (j - circles[0][0]) ** 2 + (i - circles[0][1]) ** 2 > circles[0][2] ** 2:
            image[i, j] = (0, 255, 0)
            n -= 1

if red_brick(image, n):
    print('Red Brick')
