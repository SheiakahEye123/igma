import numpy as np
import cv2
from PIL import Image, ImageDraw

#ok lets get started

image = Image.open("image.png")
quadtreeList = []
def avgcolor(image):
    finalavg = np.average(np.asarray(image), axis=0)
    return finalavg

avgcolor(image)

class Quadtree:
    def __init__(self):


