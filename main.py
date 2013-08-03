path_screenshots_log = "data/log"
path_screenshots_pop = "data/pop"
path_screenshots_pop_a_log = "data/pop_a_log"

tmp_guess_path_base = "./tmp_tesseract_file"
tmp_guess_path = tmp_guess_path_base + ".txt"

from PIL import Image, ImageOps, ImageFilter
import Levenshtein
from os import remove, listdir
from os.path import splitext, join
from random import random
from subprocess import check_call
from scipy.misc import imread, imsave
from scipy.ndimage.filters import gaussian_filter
from numpy import linspace


def load_images(base_path):
    image_sol_list = []  # image_path, solution_path
    for filename in listdir(base_path):
        if filename.endswith(".bmp"):
            image_path = join(base_path, filename)
            solution_path = join(base_path, splitext(filename)[0] + ".txt")
            image_sol_list.append((image_path, solution_path))
    return image_sol_list


def prepare_image(image_path, sigma, img_scale_factor, scale_mode):
    image = Image.open(image_path)
    prepared_path = splitext(image_path)[0] + "-edited.png"

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
    image = image.resize((int(w * img_scale_factor), int(h * img_scale_factor)), scale_mode)

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


def read_text_file(filepath):
    opened = open(filepath)
    content = opened.read()
    opened.close()
    return content


def evaluate_image(guess, solution):
    return Levenshtein.ratio(guess, solution)


def determine_best_parameters(image_path, solution_path, sigma_list=[.8, ], img_scale_factor_list=[2.77, ], scale_mode_list=[Image.ANTIALIAS, ]):
    best_args = [0, 0, 0, ""]  # goodness, guess, sigma, img_scale_factor, scale_mode
    for img_scale_factor in img_scale_factor_list:
        for sigma in sigma_list:
            for scale_mode in scale_mode_list:
                path_to_prepared_test_image = prepare_image(image_path, sigma, img_scale_factor, scale_mode)
                check_call(["tesseract", path_to_prepared_test_image, tmp_guess_path_base, "quiet"])
                guess = read_text_file(tmp_guess_path)
                solution = read_text_file(solution_path)
                goodness = evaluate_image(guess, solution)
                if goodness > best_args[0]:
                    best_args = goodness, read_text_file(tmp_guess_path_base + ".txt"), sigma, img_scale_factor, scale_mode
    return best_args


def guess_all_log():
    # experimentally determined

    sigma_list = linspace(0.8, 1.05, 25),
    img_scale_factor_list = [1 + (random() * 4) for x in range(25)],
    scale_mode_list = [Image.ANTIALIAS, Image.BILINEAR, Image.BICUBIC, Image.NEAREST]

    goodnesses = []

    for image_path, solution_path in load_images(path_screenshots_log):
        goodness, guess, sigma, img_scale_factor, scale_mode = determine_best_parameters(image_path, solution_path,
                                                                                         #sigma_list=sigma_list,
                                                                                         #img_scale_factor_list=img_scale_factor_list,
                                                                                         #scale_mode_list=scale_mode_list
                                                                                         )

        path_to_prepared_test_image = prepare_image(image_path, sigma, img_scale_factor, scale_mode)
        check_call(["tesseract", path_to_prepared_test_image, tmp_guess_path_base, "tesseract_config", "quiet"])
        guess = read_text_file(tmp_guess_path)
        solution = read_text_file(solution_path)
        goodness = evaluate_image(guess, solution)

        goodnesses.append(goodness)

        print "File: {}".format(image_path)
        print "Guess:\n{}".format(guess)
        print "Accurancy = {}% with arguments: sigma = {} img_scale_factor = {}".format(goodness, sigma, img_scale_factor)
        print "="*10

    print "Average accurancy: {}".format(sum(goodnesses)/len(goodnesses))


def cleanup():
    remove(tmp_guess_path)

guess_all_log()

cleanup()
