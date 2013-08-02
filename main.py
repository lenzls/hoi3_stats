path_screenshots_log = "data/unedited/log"
path_screenshots_pop = "data/unedited/pop"
path_screenshots_pop_a_log = "data/unedited/pop_a_log"

from PIL import Image, ImageOps
from os import remove
from os.path import splitext
from subprocess import check_call
from scipy.misc import imread, imsave
from scipy.ndimage.filters import gaussian_filter


def prepare_image(imagepath):
    image = Image.open(imagepath)
    prepared_path = splitext(imagepath)[0] + ".png"

    # crop the gamelog out
    image = image.crop((866, 914, 866 + 439, 914 + 137))
    # invert colors
    image = ImageOps.invert(image)
    # to black and white
    image = image.convert("L")  # to black and white
    threshold = 40
    image = image.point(lambda p: p > threshold and 255)
    #########################
    image.save(prepared_path)
    #########################
    #gauss
    image = imread(prepared_path)
    image = gaussian_filter(image, sigma=0.55)
    imsave(prepared_path, image)

    image = Image.open(prepared_path)
    image.show()
    return prepared_path


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

print "Start-test suite"
path_to_test_image = "./data/unedited/log/HoI3_6.bmp"
path_to_prepared_test_image = prepare_image(path_to_test_image)
tmp_outbase_path = "./tmp_tesseract_file"
print "image to process: ", path_to_prepared_test_image
print "temporary path to result text: ", tmp_outbase_path
check_call(["tesseract", path_to_prepared_test_image, tmp_outbase_path])

tes_output_file = open(tmp_outbase_path + ".txt")
ocr_output = tes_output_file.read()
print ocr_output

remove(tmp_outbase_path + ".txt")
print "End"
