#coding:utf-8

import base
from skimage import filters
from skimage.morphology import disk
from skimage.filters.rank import median

def filter(image):
    edges = filters.sobel(image)
    return edges

def filter2(image):
    med = median(image, disk(5))
    return med


if __name__ == '__main__':
    path = '/home/dmp/code/imageProcess/data/1.dcm'
    image = base.read_dcm(path)
    print image.shape
    image = image[:,:,0]
    print image.shape
    edges = filter(image)
    #edges = filter2(image)
    print edges
    base.show(edges)
    base.show(image)
    #statisctics(image)