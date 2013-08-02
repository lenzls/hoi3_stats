path_screenshots_log = "data/unedited/log"
path_screenshots_pop = "data/unedited/pop"
path_screenshots_pop_a_log = "data/unedited/pop_a_log"

path_to_test_image = "data/unedited/log/HoI3_6.bmp"

from PIL import Image
from os.path import splitext


def prepare_image(imagepath):
    image = Image.open(imagepath)
    cropped_path = splitext(imagepath)[0] + ".png"

    image.crop((866, 914, 866 + 439, 914 + 137)).save(cropped_path)


def ex1(path):
    import cv2.cv as cv
    import tesseract

    image = cv.LoadImage(path, cv.CV_LOAD_IMAGE_GRAYSCALE)

    api = tesseract.TessBaseAPI()
    api.Init(".", "eng", tesseract.OEM_DEFAULT)
    #api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
    api.SetPageSegMode(tesseract.PSM_AUTO)
    tesseract.SetCvImage(image, api)
    text = api.GetUTF8Text()
    conf = api.MeanTextConf()
    print "Confidence of following: {}".format(conf)
    print text

print "Start"
prepare_image(path_to_test_image)
print "End"
