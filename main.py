path_screenshots_log = "data/unedited/log"
path_screenshots_pop = "data/unedited/pop"
path_screenshots_pop_a_log = "data/unedited/pop_a_log"

tmp_outbase_path = "./tmp_tesseract_file"

from PIL import Image, ImageOps
import Levenshtein
from os import remove
from os.path import splitext
from subprocess import check_call
from scipy.misc import imread, imsave
from scipy.ndimage.filters import gaussian_filter
from numpy import linspace


def prepare_image(imagepath, sigma):
    image = Image.open(imagepath)
    prepared_path = splitext(imagepath)[0] + ".png"

    # crop the gamelog out
    image = image.crop((866, 914, 866 + 439, 914 + 137))
    # invert colors
    image = ImageOps.invert(image)
    # to black and white
    image = image.convert("L")  # to black and white
    threshold = 41
    image = image.point(lambda p: p > threshold and 255)
    #resize
    w, h = image.size
    image = image.resize((w * 2, h * 2), Image.NEAREST)
    #########################
    image.save(prepared_path)
    #########################
    #gauss
    image = imread(prepared_path)
    image = gaussian_filter(image, sigma=sigma)
    imsave(prepared_path, image)

    image = Image.open(prepared_path)
    #image.show()
    return prepared_path


def evaluate_image(imagepath, solution):
    tes_output_file = open(imagepath)
    ocr_output = tes_output_file.read()
    tes_output_file.close()
    #print ocr_output
    return Levenshtein.ratio(ocr_output, solution)


def check_for_best_sigma(imagepath):
    best_args = [0, 0, ""]  # sigma, goodness, solution
    for sigma in linspace(-1., 1., 10):
        print "sig: ", sigma
        path_to_prepared_test_image = prepare_image(imagepath, sigma)
        check_call(["tesseract", path_to_prepared_test_image, tmp_outbase_path])
        goodness = evaluate_image(tmp_outbase_path + ".txt", test_image_solution)
        print "distance between guess and solution (more = better): ", goodness
        if goodness > best_args[1]:
            best_args = sigma, goodness, test_image_solution
    return best_args

print "Start-test suite"
path_to_test_image = "./data/unedited/log/HoI3_6.bmp"
test_image_solution = """14:00, 19 October, 1941 133a Divisione 'Littorio' arrived in Balashov
16:00, 19 October1 1941 Hostile planes are performing a Ground Attack in
Tandaho.
316:00, 19 October1 1941 We won the Batle of Korenovsk. We lost 1084 of
46967, Soviet Union lost 380 of 8998

17:00, 19 October1 1941 1a Divisione Alpina 'Taurinese' arrived in

Korenovsk
"""

b_sigma, b_goodness, b_solution = check_for_best_sigma(path_to_test_image)

tmp_path = prepare_image(path_to_test_image, b_sigma)
check_call(["tesseract", tmp_path, tmp_outbase_path])
goodness = evaluate_image(tmp_outbase_path + ".txt", test_image_solution)
print "Best arguments ({}%): sigma = {} ".format(b_goodness, b_sigma)
print "Guess:\n{}".format(b_solution)
image = Image.open(tmp_path)
image.show()


remove(tmp_outbase_path + ".txt")
print "End"
