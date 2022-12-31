import numpy as np
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# ok lets get started
AVG_TOLERANCE = 1


def betteravgcolor(image):
    r = np.nanmean(image[:, :, 0])
    g = np.nanmean(image[:, :, 1])
    b = np.nanmean(image[:, :, 2])

    averagelist = np.array([r, g, b])

    print('average list is', averagelist)

    return averagelist


def splitIgma(image, xMin, xMax, yMin, yMax):
    splitimg = []
    xCenter = int ((xMax + xMin) / 2)
    yCenter = int ((yMax + yMin) / 2)
    nw = image[int(xMin):xCenter, int(yMin):yCenter, :]
    ne = image[xCenter:int(xMax), int(yMin):yCenter, :]
    sw = image[int(xMin):xCenter, yCenter:int(yMax), :]
    se = image[xCenter:int(xMax), yCenter:int(yMax), :]

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
    def __init__(self, xMin_, xMax_, yMin_, yMax, image):
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
        self.xMin = xMin_
        self.xMax = xMax_
        self.yMin = yMin_
        self.yMax = yMax
        self.imgarray = image

    def split(self):
        xCenter = int((self.xMax + self.xMin) / 2)
        yCenter = int((self.yMax + self.yMin) / 2)
        self.nw = Quadtree(self.xMin, xCenter, self.yMin, yCenter)
        self.ne = Quadtree(xCenter, self.xMax, self.yMin, yCenter)
        self.sw = Quadtree(self.xMin, xCenter, yCenter, self.yMax)
        self.se = Quadtree(xCenter, self.xMax, yCenter, self.yMax)

        self.nw.insert()
        self.ne.insert()
        self.sw.insert()
        self.se.insert()

    def insert(self):
        slice = self.imgarray[self.yMin:self.yMax,self.xMin:self.xMax,:]
        if any(dim <= 20 for dim in slice.shape):
            return

        #print('inserting fr subimage of size', self.imageArray.shape)
        avg = betteravgcolor(slice)

        deviation1 = slice - avg

        deviation = np.average(deviation1, axis=2)

        if np.sum(np.abs(deviation)) >= AVG_TOLERANCE:
            #plt.imshow(deviation)
            #plt.pause(0.000000000000001)
            self.split()
            # sums deviation of the whole image
            # could try avg deviation?

        else:
            self.imgarray[self.yMin:self.yMax, self.xMin:self.xMax, :] = avg





image = Image.open("image.png")
npimg = np.asarray(image)
baseQuad = Quadtree(0, image.width, 0, image.height, npimg)
baseQuad.insert()
plt.imshow(npimg)
plt.show()
