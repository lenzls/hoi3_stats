path_screenshots_log = "data/unedited/log"
path_screenshots_pop = "data/unedited/pop"
path_screenshots_pop_a_log = "data/unedited/pop_a_log"

from PIL import Image, ImageOps
import Levenshtein
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

print "Start-test suite"
path_to_test_image = "./data/unedited/log/HoI3_6.bmp"
test_image_solution = """14:00, 19 October, 1941 133a Divisione 'Littorio' arrived in Balashov
16:00, 19 October1 1941 Hostile planes are performing a Ground Attack in
Tandaho.
16:00, 19 October1 1941 We won the Batle of Korenovsk. We lost 1084 of
46967, Soviet Union lost 380 of 8998
17:00, 19 October1 1941 1a Divisione Alpina 'Taurinese' arrived in
Korenovsk
"""

path_to_prepared_test_image = prepare_image(path_to_test_image)
tmp_outbase_path = "./tmp_tesseract_file"
print "image to process: ", path_to_prepared_test_image
print "temporary path to result text: ", tmp_outbase_path
check_call(["tesseract", path_to_prepared_test_image, tmp_outbase_path])

tes_output_file = open(tmp_outbase_path + ".txt")
ocr_output = tes_output_file.read()
print ocr_output

print Levenshtein.ratio(ocr_output, test_image_solution)

remove(tmp_outbase_path + ".txt")
print "End"
