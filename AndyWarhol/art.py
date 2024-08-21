import cv2 # type: ignore
import numpy as np # type: ignore
import scipy as sp # type: ignore
import random

# CS4475 Project 3
# Summer 2024
# Stuthi Bhat, Victoria Choi, Steven Li, Raymond Liu



# ====== DO NOT MODIFY BELOW THIS LINE ======

face_cascade = cv2.CascadeClassifier()

def cropFace(image):
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 

    faceRect = haar_cascade.detectMultiScale(grayImage, scaleFactor=1.1, minNeighbors=9)
    largestFace = ()
    largestSize = 0
    for (x, y, w, h) in faceRect: 
        if (w * h > largestSize):
            largestSize = w * h
            largestFace = (x, y, w, h)
    return image[largestFace[1] : largestFace[1] + largestFace[2], largestFace[0] : largestFace[0] + largestFace[2]]

def mapToBlockColors(image):
    out = np.array(image)
    cv2.edgePreservingFilter(image, out, 3, 128)

    out = np.round(image / 72)
    out *= 72

    kernel = np.ones((5,5),np.uint8)
    out = cv2.erode(out, kernel, iterations=2)
    out = cv2.dilate(out, kernel, iterations=1)
    return out.astype(np.uint8)

def mapColors(image, brightColor):
    colors = dict()
    out = np.zeros(image.shape)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if str(image[i, j]) not in colors.keys():
                if (image[i, j, 0] == image[i, j, 1] == image[i, j, 2] >= int(random.uniform(150, 200))):
                    newColor = brightColor
                else:
                    change = 50
                    newColor = [image[i, j, 0], image[i, j, 1], image[i, j, 2]]
                    newColor[0] = trim(newColor[0] + int(random.uniform(-change, change)))
                    newColor[1] = trim(newColor[1] + int(random.uniform(-change, change)))
                    newColor[2] = trim(newColor[2] + int(random.uniform(-change, change)))
                colors[str(image[i, j])] = newColor
            out[i, j] = colors[str(image[i, j])]
    out = out.astype(np.uint8)
    hsv = cv2.cvtColor(out, cv2.COLOR_BGR2HSV)
    for i in range(hsv.shape[0]):
        for j in range(hsv.shape[1]):
            hsv[i, j, 1] = trim(hsv[i, j, 1] * 1.5)
    out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return out
    
def collage(images):
    out = np.zeros((3 * images[0].shape[0], 3 * images[0].shape[1], 3))
    # print(out.shape)
    counter = 0
    for i in range(0, 3):
        for j in range(0, 3):
            out[i * images[counter].shape[0] : (i + 1) * images[counter].shape[0], 
                j * images[counter].shape[1]: (j + 1) * images[counter].shape[1]] = images[counter]
            counter += 1
    return out

def trim(num):
    if (num < 0):
        return 0
    elif (num >= 255):
        return 255
    else:
        return num


# ====== DO NOT MODIFY ABOVE THIS LINE ======


input = "person.png" #input the name of your start image file here

colorList = [
    [255, 0, 255], #magenta
    [0, 110, 255], #bright orange
    [240, 200, 140], #baby blue
    [180, 105, 255], #hot pink
    [0, 0, 255], #red
    [8, 200, 12], #bright green
    [191, 64, 191], #bright purple
    [88, 219, 255], #mustard yellow
    [128, 128, 0], #dull teal
]

# ====== DO NOT MODIFY BELOW THIS LINE ======

image = cv2.imread(input)
imageList = []

for i in range(9):
    curr = np.array(image)
    curr = cropFace(image)
    curr = mapToBlockColors(curr)
    curr = mapColors(curr, colorList[i])
    imageList.append(curr)

cv2.imwrite('personOutput.png', collage(imageList))

# ====== DO NOT MODIFY ABOVE THIS LINE ======