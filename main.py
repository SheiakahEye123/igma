import numpy as np
import cv2
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# ok lets get started

image = Image.open("image.png")
quadtreeList = []
imgarray = np.asarray(image)
AVG_TOLERANCE = 100


def betteravgcolor(image):
    r = np.average(image[:, :, 0])
    g = np.average(image[:, :, 1])
    b = np.average(image[:, :, 2])

    averagelist = np.array([r, g, b])

    return averagelist


def splitIgma(image, xMin, xMax, yMin, yMax):
    splitimg = []
    nw = image[int(xMin):int(xMax / 2), int(yMin):int(yMax / 2), :]
    ne = image[int(xMax / 2):int(xMax), int(yMin):int(yMax / 2), :]
    sw = image[int(xMin):int(xMax / 2), int(yMax / 2):int(yMax), :]
    se = image[int(xMax / 2):int(xMax), int(yMax / 2):int(yMax), :]

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

        self.nw.insert()
        self.ne.insert()
        self.sw.insert()
        self.se.insert()

    def insert(self):
        avg = betteravgcolor(self.imageArray)

        deviation1 = self.imageArray - avg
        deviation = np.average(deviation1, axis=2, weights=[1,1,1])

        for i in range(len(deviation)):
            for e in range(len(deviation[0])):
                if -1 * AVG_TOLERANCE >= deviation[i, e] <= AVG_TOLERANCE:
                    #print(deviation[i][e])
                    self.split()




baseQuad = Quadtree(0, image.width, 0, image.height, imgarray)
baseQuad.insert()
