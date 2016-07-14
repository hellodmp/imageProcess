#coding=utf-8

from skimage.segmentation import slic
import base

def segment(image):
    segments = slic(image, n_segments=100, compactness=10)
    return segments


if __name__ == '__main__':
    path = '/home/dmp/code/imageProcess/data/1.dcm'
    image = base.read_dcm(path)
    image = image[:,:,0]
    segments = segment(image)
    print segments
    base.show(segments)
