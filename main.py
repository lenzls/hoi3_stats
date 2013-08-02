path_screenshots_log = "data/unedited/log"
path_screenshots_pop = "data/unedited/pop"
path_screenshots_pop_a_log = "data/unedited/pop_a_log"

tmp_outbase_path = "./tmp_tesseract_file"

from PIL import Image, ImageOps, ImageFilter
import Levenshtein
from os import remove, listdir
from os.path import splitext, join
from random import random
from subprocess import check_call
from scipy.misc import imread, imsave
from scipy.ndimage.filters import gaussian_filter
from numpy import linspace


def load_images(basepath):
    image_sol_list = []  # imagepath, solutionpath
    for filename in listdir(basepath):
        if filename.endswith(".bmp"):
            image_path = join(basepath, filename)
            solution_path = join(basepath, splitext(image_path)[0] + ".txt")
            image_sol_list.append((image_path, solution_path))
    return image_sol_list


def prepare_image(imagepath, sigma, img_scale_factor):
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
    image = image.resize((int(w * img_scale_factor), int(h * img_scale_factor)), Image.ANTIALIAS)

    #########################
    image.save(prepared_path)
    #########################
    #gauss
    image = imread(prepared_path)
    image = gaussian_filter(image, sigma=sigma)
    #########################
    imsave(prepared_path, image)
    #########################
    image = Image.open(prepared_path)
    image = image.filter(ImageFilter.UnsharpMask)
    #########################
    image.save(prepared_path)
    #########################

    #image = Image.open(prepared_path)
    #image.show()
    return prepared_path


def evaluate_image(imagepath, solutionpath):
    tes_output_file = open(imagepath)
    ocr_output = tes_output_file.read()
    tes_output_file.close()

    solution_file = open(imagepath)
    solution = solution_file.read()
    solution_file.close()

    print "evaluating {} with solutions: {}".format(imagepath, solutionpath)
    return Levenshtein.ratio(ocr_output, solution)


def check_for_best_sigma(imagepath):
    best_args = [0, 0, 0, ""]  # goodness, solution, sigma, img_scale_factor
    for img_scale_factor in [1 + (random() * 4) for x in range(25)]:
        for sigma in linspace(0.8, 1.05, 25):
            print "sig: ", sigma
            print "img_scale_factor: ", img_scale_factor
            path_to_prepared_test_image = prepare_image(imagepath, sigma, img_scale_factor)
            check_call(["tesseract", path_to_prepared_test_image, tmp_outbase_path, "quiet"])
            goodness = evaluate_image(tmp_outbase_path + ".txt", test_image_solution)
            print "distance between guess and solution (more = better): ", goodness
            if goodness > best_args[0]:
                best_args = goodness, test_image_solution, sigma, img_scale_factor
    return best_args


def check_example_file():
    print "Start-test suite"
    path_to_test_image = "./data/unedited/log/HoI3_6.bmp"

    b_goodness, b_solution, b_sigma, b_img_scale_factor = check_for_best_sigma(path_to_test_image)

    tmp_path = prepare_image(path_to_test_image, b_sigma, b_img_scale_factor)
    check_call(["tesseract", tmp_path, tmp_outbase_path, "quiet"])
    goodness = evaluate_image(tmp_outbase_path + ".txt", test_image_solution)
    print "Best arguments ({}%): sigma = {} img_scale_factor = {}".format(b_goodness, b_sigma, b_img_scale_factor)
    print "Guess:\n{}".format(b_solution)
    image = Image.open(tmp_path)
    image.show()


def guess_all_log():
    # experimentally determined
    sigma = 0.8
    img_scale_factor = 2.779

    for image_path, solution_path in load_images(path_screenshots_log):
        tmp_path = prepare_image(image_path, sigma, img_scale_factor)
        check_call(["tesseract", tmp_path, tmp_outbase_path, "quiet"])
        goodness = evaluate_image(tmp_outbase_path + ".txt", solution_path)
        tes_output_file = open(tmp_outbase_path + ".txt")
        ocr_output = tes_output_file.read()
        tes_output_file.close()
        print "Guess:\n{}".format(ocr_output)
        print "Accurancy = {}% with arguments: sigma = {} img_scale_factor = {}".format(goodness, sigma, img_scale_factor)
        print "="*10


def cleanup():
    remove(tmp_outbase_path + ".txt")

guess_all_log()

cleanup()
