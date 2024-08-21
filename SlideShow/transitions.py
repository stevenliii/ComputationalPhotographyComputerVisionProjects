import cv2 # type: ignore
import numpy as np # type: ignore
import scipy as sp # type: ignore
import math

# CS4475 Project 1
# Summer 2024
# Stuthi Bhat, Victoria Choi, Steven Li, Raymond Liu

# ====== DO NOT MODIFY ABOVE THIS LINE ======


yourDirectory = "/Users/StevenLi/Desktop/CS4475/Project1/outputs/" # paste yourDirectory here
yourTransition = "splitoutputsequence/" # paste yourTransition here


# ====== DO NOT MODIFY BELOW THIS LINE ======


# transition that slides the start image off to the left while sliding in the end image from the right
def slideTransition(image1, image2, frameCount):

    step = math.floor(image1.shape[1] / (frameCount - 2))
    
    for i in range(1, frameCount - 1):

        out = np.zeros(image1.shape)

        out[0:image1.shape[0], 0:image1.shape[1] - (i * step)] = image1[0:image1.shape[0], (i * step):image1.shape[1]]
        out[0:image1.shape[0], image1.shape[1] - (i * step):out.shape[1]] = image2[0:image1.shape[0], 0:i * step]

        write(out, yourTransition, str(i))

    write(image1, yourTransition, str(0))
    write(image2, yourTransition, str(frameCount - 1))

# transition that fades the start image to black and fades the end image to full color
def fadeTransition(image1, image2, frameCount):

    for i in range(1, math.floor((frameCount + 1) / 2)):

        fraction = (math.floor((frameCount + 1) / 2) - i) / math.floor((frameCount + 1) / 2)

        out1 = image1 * fraction
        out2 = image2 * fraction

        write(out1, yourTransition, str(i))
        write(out2, yourTransition, str(frameCount - 1 - i))

    write(image1, yourTransition, str(0))
    write(image2, yourTransition, str(frameCount - 1))

# transition that reveals the end image through a growing circle in the center of the start image
def circleTransition(image1, image2, frameCount):

    maxRadius = math.ceil(math.sqrt(image1.shape[0]**2 + image1.shape[1]**2) / 1.8)
    step = math.floor(maxRadius / (frameCount - 2))

    for i in range(1, frameCount - 2):

        opmask = np.zeros((image1.shape[0], image1.shape[1]), dtype = np.uint8)
        opmask = cv2.circle(opmask, (int(image1.shape[1] / 2), int(image1.shape[0] / 2)), step * i, 255, -1)
        opmaskinv = cv2.bitwise_not(opmask)

        out1 = cv2.bitwise_and(image1, image1, mask = opmaskinv)
        out2 = cv2.bitwise_and(image2, image2, mask = opmask)
        out = cv2.add(out1, out2)

        write(out, yourTransition, str(i))

    write(image1, yourTransition, str(0))
    write(image2, yourTransition, str(frameCount - 1))

# transition that brightens the start image to white and darkens the end image to full color
def flashTransition(image1, image2, frameCount):

    for i in range(1, math.floor((frameCount + 1) / 2)):

        fraction = 1 - (math.floor((frameCount + 1) / 2) - i) / math.floor((frameCount + 1) / 2)
        inc1 = (-1 * image1 + 255) * fraction
        inc2 = (-1 * image2 + 255) * fraction
        out1 = np.add(image1, inc1)
        out2 = np.add(image2, inc2)

        write(out1, yourTransition, str(i))
        write(out2, yourTransition, str(frameCount - 1 - i))

    write(image1, yourTransition, str(0))
    write(image2, yourTransition, str(frameCount - 1))

# transition that slides the left half of the start image left and the right half right to reveal the end image in the center
def splitTransition(image1, image2, frameCount):

    middle = math.floor(image1.shape[1] / 2)
    step = math.floor(image1.shape[1] / (frameCount - 2))

    for i in range(1, (frameCount - 1)):

        out = np.zeros(image1.shape)

        out[0:image1.shape[0], 0:middle - int((i * step) / 2)] = image1[0:image1.shape[0], int((i * step) / 2):middle]
        out[0:image1.shape[0], middle + int((i * step) / 2):image1.shape[1]] = image1[0:image1.shape[0], middle:image1.shape[1] - int((i * step) / 2)]

        out[0:image2.shape[0], middle - int((i * step) / 2):middle + int((i * step) / 2)] = image2[0:image1.shape[0], middle - int((i * step) / 2):middle + int((i * step) / 2)]

        write(out, yourTransition, str(i))

    write(image1, yourTransition, str(0))
    write(image2, yourTransition, str(frameCount - 1))

# writes a numpy image array to a directory
def write(image, directory, name):
    cv2.imwrite(yourDirectory + directory + name + ".png", image)



# ====== DO NOT MODIFY ABOVE THIS LINE ======


start = "img5.png" #input the name of your start image file here
end = "img6.png" #input the name of your end image file here


# ====== DO NOT MODIFY BELOW THIS LINE ======

startArr = cv2.imread(start)
endArr = cv2.imread(end)

# ====== DO NOT MODIFY ABOVE THIS LINE ======

# Uncomment the transition you would like by calling the associated function. Edit the frameCount if you would like.

# slideTransition(startArr, endArr, 30)
# fadeTransition(startArr, endArr, 30)
# circleTransition(startArr, endArr, 30)
# flashTransition(startArr, endArr, 30)
# splitTransition(startArr, endArr, 30)