import os
import numpy
import SimpleITK
import matplotlib.pyplot as plt

def sitk_show(img, title=None, margin=0.05, dpi=40 ):
    nda = SimpleITK.GetArrayFromImage(img)
    spacing = img.GetSpacing()
    figsize = (1 + margin) * nda.shape[0] / dpi, (1 + margin) * nda.shape[1] / dpi
    extent = (0, nda.shape[1]*spacing[1], nda.shape[0]*spacing[0], 0)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes([margin, margin, 1 - 2*margin, 1 - 2*margin])
    plt.set_cmap("gray")
    ax.imshow(nda,extent=extent,interpolation=None)

    if title:
        plt.title(title)
    plt.show()


def read_images(pathDicom):
    reader = SimpleITK.ImageSeriesReader()
    filenamesDICOM = reader.GetGDCMSeriesFileNames(pathDicom)
    reader.SetFileNames(filenamesDICOM)
    imgOriginal = reader.Execute()
    return imgOriginal

def read_image(path):
    image = SimpleITK.ReadImage(path)
    return image

def smooth(image):
    imgSmooth = SimpleITK.CurvatureFlow(image1=image,
                                        timeStep=0.125,
                                        numberOfIterations=5)
    #blurFilter = SimpleITK.CurvatureFlowImageFilter()
    #blurFilter.SetNumberOfIterations(5)
    #blurFilter.SetTimeStep(0.125)
    #imgSmooth = blurFilter.Execute(image)
    return imgSmooth

def segment1(imgSmooth):
    labelWhiteMatter = 1
    labelGrayMatter = 2
    lstSeeds = [(100, 150)]
    imgWhiteMatter = SimpleITK.ConnectedThreshold(image1=imgSmooth,
                                                  seedList=lstSeeds,
                                                  lower=-1024,
                                                  upper=1024,
                                                  replaceValue=labelWhiteMatter)

    # Rescale 'imgSmooth' and cast it to an integer type to match that of 'imgWhiteMatter'
    temp =  imgWhiteMatter.GetPixelID()
    b = SimpleITK.RescaleIntensity(imgSmooth)
    imgSmoothInt = SimpleITK.Cast(SimpleITK.RescaleIntensity(imgSmooth), imgWhiteMatter.GetPixelID())

    # Use 'LabelOverlay' to overlay 'imgSmooth' and 'imgWhiteMatter'
    sitk_show(SimpleITK.LabelOverlay(imgSmoothInt, imgWhiteMatter))


def segment(imgSmooth):
    labelWhiteMatter = 1
    labelGrayMatter = 2
    lstSeeds = [(119, 83), (198, 80), (185, 102), (164, 43)]

    imgGrayMatter = SimpleITK.ConnectedThreshold(image1=imgSmooth,
                                                 seedList=lstSeeds,
                                                 lower=150,
                                                 upper=270,
                                                 replaceValue=labelGrayMatter)

    # Rescale 'imgSmooth' and cast it to an integer type to match that of 'imgWhiteMatter'
    imgSmoothInt = SimpleITK.Cast(SimpleITK.RescaleIntensity(imgSmooth), imgGrayMatter.GetPixelID())

    imgGrayMatterNoHoles = SimpleITK.VotingBinaryHoleFilling(image1=imgGrayMatter,
                                                             radius=[2] * 3,
                                                             majorityThreshold=1,
                                                             backgroundValue=0,
                                                             foregroundValue=labelGrayMatter)

    sitk_show(SimpleITK.LabelOverlay(imgSmoothInt, imgGrayMatterNoHoles))





if __name__ == '__main__':
    headPath = "./data/MR000050.dcm"
    pathDicom = "./data/2.dcm"
    print pathDicom

    image = read_image(pathDicom)

    image = image[:, :, 0]
    #imgSmooth = smooth(image)
    # sitk_show(imgSmooth)
    imgSmooth = image
    segment1(imgSmooth)

