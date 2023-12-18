import numpy as np
import cv2


def colored_areas(i, area_in, color):
    # making masks for all colors to eventually count how many pixels of a particular color there are on the picture
    img = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)

    if color == "red":
        lower1 = np.array([0, 150, 100])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([160, 150, 100])
        upper2 = np.array([179, 255, 255])

        mask1 = cv2.inRange(img, lower1, upper1)
        mask2 = cv2.inRange(img, lower2, upper2)

        full_mask = mask1 + mask2

    elif color == "white":
        lower = np.array([0, 0, 210])
        upper = np.array([255, 45, 255])

        full_mask = cv2.inRange(img, lower, upper)

    elif color == "black":
        lower1 = np.array([0, 0, 0])
        upper1 = np.array([180, 255, 40])
        lower2 = np.array([0, 0, 0])
        upper2 = np.array([0, 250, 200])

        mask1 = cv2.inRange(img, lower1, upper1)
        mask2 = cv2.inRange(img, lower2, upper2)
        full_mask = mask1 + mask2

    elif color == "blue":
        lower = np.array([90, 60, 60])
        upper = np.array([130, 255, 255])

        full_mask = cv2.inRange(img, lower, upper)

    img_masked = cv2.bitwise_and(img, img, mask=full_mask)
    gray = cv2.cvtColor(img_masked, cv2.COLOR_BGR2GRAY)
    col_area = i.shape[0] * i.shape[1]
    for k in range(i.shape[0]):
        for j in range(i.shape[1]):
            if gray[k, j] == 0:
                col_area -= 1
    return col_area / area_in


def red_brick(i, area_in):
    # finding red area and looking for how much red color there are
    if 0.5 < colored_areas(i, area_in, 'red') < 0.8:
        return True


def speed_limit(i, area_in):
    # finding black area and looking for how much black color there are
    if 0.12 < colored_areas(i, area_in, 'black') < 0.35 and colored_areas(i, area_in, 'white') < 0.7:
        return True


def no_road(i, area_in):
    # finding white area and looking for how much white color there are
    if 0.75 < colored_areas(i, area_in, 'white'):
        return True


def no_stopping(i, area_in):
    # finding blue and red areas and looking for how much those colors there are
    if 0.35 < colored_areas(i, area_in, "blue") < 0.5 and 0.35 < colored_areas(i, area_in, "red") < 0.5:
        return True


def move(i, area_in):
    print(colored_areas(i, area_in, "blue"))
    if 0.8 < colored_areas(i, area_in, "blue") < 0.95:
        return 'straight'
    elif 0.55 < colored_areas(i, area_in, "blue") < 0.75:
        return 'circle'


picture_name = input()
image = cv2.imread("test_images/"+picture_name+".jpeg")
img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
sign = 'other sign'

# Find circles
circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.3, 100)
if circles is not None:
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
        sign = 'No entry sign'
    elif speed_limit(image, n):
        sign = 'Speed limit sign'
    elif no_road(image, n):
        sign = 'End of all restricted areas sign'
    elif no_stopping(image, n):
        sign = 'No stopping sign'
    elif move(image, n) == "straight":
        sign = 'Go straight sign'
    elif move(image, n) == "circle":
        sign = "Roundabout sign"

print(sign)
cv2.imshow(sign, cv2.imread("test_images/"+picture_name+".jpeg"))
cv2.waitKey(0)