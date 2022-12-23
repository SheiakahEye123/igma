import numpy as np
import cv2
from PIL import Image, ImageDraw

# ok lets get started

image = Image.open("image.png")
quadtreeList = []
imgarray = np.asarray(image)
AVG_TOLERANCE = 50


def betteravgcolor(image):
    firstavg = np.average(image)
    finalavg = np.average(firstavg)
    return finalavg


def splitIgma(image, xMin, xMax, yMin, yMax):
    splitimg = []
    nw = []
    ne = []
    sw = []
    se = []

    for i in range(yMax / 2):
        for e in range(xMax / 2):
            nw.append(image[i][e])
    for i in range(yMax / 2):
        for e in range(xMax / 2):
            ne.append(image[i + yMax / 2][e + xMax / 2])
    for i in range(yMax / 2):
        for e in range(xMax / 2):
            sw.append(image[i][e + xMax / 2])
    for i in range(yMax / 2):
        for e in range(xMax / 2):
            se.append(image[i + yMax / 2][e])

    splitimg.append(nw)
    splitimg.append(ne)
    splitimg.append(sw)
    splitimg.append(se)

    return splitimg


# def imageTo2DArray(image):
#     initialArray = np.asarray(image)
#     finalArray = []
#     for i in range(initialArray.size):
#         for e in range(Y_DIMENSION):
#             minorArray.append(ini)

class Quadtree():
    def __init__(self, xMin_, xMax_, yMin_, yMax, imageArray_):
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
        self.xMin = xMin_
        self.xMax = xMax_
        self.yMin = yMin_
        self.yMax = yMax
        self.imageArray = imageArray_

    def split(self):
        splittedImg = splitIgma(self.imageArray, self.xMin, self.xMax, self.yMin, self.yMax)
        self.nw = Quadtree(self.xMin, self.xMax / 2, self.yMin, self.yMax / 2, splittedImg[0])
        self.ne = Quadtree(self.xMax / 2, self.xMax, self.yMin, self.yMax / 2, splittedImg[1])
        self.sw = Quadtree(self.xMin, self.xMax / 2, self.yMax / 2, self.yMax, splittedImg[2])
        self.se = Quadtree(self.xMax / 2, self.xMax, self.yMax / 2, self.yMax, splittedImg[3])

    def insert(self):
        avg = betteravgcolor(self.imageArray)
        for i in range(self.imageArray.size):
            for e in range(self.imageArray[0].size):
                for p in range(self.imageArray[0][0].size):
                    if avg - AVG_TOLERANCE < self.imageArray[i][e][p] < avg + AVG_TOLERANCE:
                        self.split()

