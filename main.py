img_cropped = "data/radical_cropped.png"
img_cropped_gauss = "data/radical_cropped.png"

imgfile = img_cropped_gauss

def ex1(path):
    import cv2.cv as cv
    import tesseract

    image=cv.LoadImage(path, cv.CV_LOAD_IMAGE_GRAYSCALE)

    api = tesseract.TessBaseAPI()
    api.Init(".","eng",tesseract.OEM_DEFAULT)
    #api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
    api.SetPageSegMode(tesseract.PSM_AUTO)
    tesseract.SetCvImage(image,api)
    text=api.GetUTF8Text()
    conf=api.MeanTextConf()
    print "Confidence of following: {}".format(conf)
    print text

print "Start"
ex1(img_cropped)
ex1(img_cropped_gauss)
print "End"
