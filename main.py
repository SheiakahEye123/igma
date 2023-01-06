import numpy as np
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# ok lets get started
AVG_TOLERANCE = 20000


def betteravgcolor(thatimage):
    r = np.nanmean(thatimage[:, :, 0])
    g = np.nanmean(thatimage[:, :, 1])
    b = np.nanmean(thatimage[:, :, 2])

    averagelist = np.array([r, g, b])

    return averagelist.astype(np.uint8)


def splitIgma(thisimage, xMin, xMax, yMin, yMax):
    splitimg = []
    xCenter = int((xMax + xMin) / 2)
    yCenter = int((yMax + yMin) / 2)
    nw = thisimage[int(xMin):xCenter, int(yMin):yCenter, :]
    ne = thisimage[xCenter:int(xMax), int(yMin):yCenter, :]
    sw = thisimage[int(xMin):xCenter, yCenter:int(yMax), :]
    se = thisimage[xCenter:int(xMax), yCenter:int(yMax), :]

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
    def __init__(self, xMin_, xMax_, yMin_, yMax, image, final):
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
        self.xMin = xMin_
        self.xMax = xMax_
        self.yMin = yMin_
        self.yMax = yMax
        self.imgarray = image
        self.finalimgarray = final

    def split(self):
        xCenter = int((self.xMax + self.xMin) / 2)
        yCenter = int((self.yMax + self.yMin) / 2)
        self.nw = Quadtree(self.xMin, xCenter, self.yMin, yCenter, self.imgarray, self.finalimgarray)
        self.ne = Quadtree(xCenter, self.xMax, self.yMin, yCenter, self.imgarray, self.finalimgarray)
        self.sw = Quadtree(self.xMin, xCenter, yCenter, self.yMax, self.imgarray, self.finalimgarray)
        self.se = Quadtree(xCenter, self.xMax, yCenter, self.yMax, self.imgarray, self.finalimgarray)

        self.nw.insert()
        self.ne.insert()
        self.sw.insert()
        self.se.insert()

    def insert(self):
        slice = self.imgarray[self.yMin:self.yMax, self.xMin:self.xMax, :]
        avg = betteravgcolor(slice)
        if any(dim <= 1 for dim in slice.shape[0:2]):
            self.finalimgarray[self.yMin:self.yMax, self.xMin:self.xMax, :] = avg
            return
        # print('inserting fr subimage of size', self.imageArray.shape)

        deviation1 = slice - avg

        deviation = np.average(deviation1, axis=2)
        # print(np.sum(np.abs(deviation)))

        print(np.sum(np.abs(deviation)))
        if np.sum(np.abs(deviation)) >= AVG_TOLERANCE:
            self.split()
            # sums deviation of the whole image
            # could try avg deviation?

        else:
            self.finalimgarray[self.yMin:self.yMax, self.xMin:self.xMax, :] = avg
            return

    def finalimg(self):
        return self.finalimgarray


image = Image.open("image.png")
image = image.convert('RGB')
npimg = np.asarray(image)
baseQuad = Quadtree(0, image.width, 0, image.height, npimg, np.zeros_like(npimg, dtype=np.uint8))
baseQuad.insert()
plt.imshow(baseQuad.finalimgarray)
plt.show()
