#coding=utf-8

import SimpleITK
from skimage import io
from skimage import data

#读取dicom文件
def read_dcm(path):
    #read dicom
    data = SimpleITK.ReadImage(path)

    #Rescale the vlaue into [0,255]
    filter = SimpleITK.RescaleIntensityImageFilter()
    dcm = filter.Execute(data,0,255)
    # tansform to numpy
    nda = SimpleITK.GetArrayFromImage(dcm)
    (w, h, d)=nda.shape
    image = nda.reshape((w, h, d)).transpose(1, 2, 0)
    return image

#显示图像
def show(image):
    io.imshow(image[:,:,0])
    io.show()

#统计图像属性
def statisctics(image):
    print image.min()
    print image.max()
    print image.shape
    print image.size


if __name__ == '__main__':
    path = '/home/dmp/code/imageProcess/data/1.dcm'
    image = read_dcm(path)
    show(image)
    #statisctics(image)
