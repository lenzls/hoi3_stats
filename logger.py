import overlay
from PIL import Image, ImageOps, ImageFilter
from scipy.misc import imread, imsave
from scipy.ndimage.filters import gaussian_filter
from os.path import splitext
from subprocess import check_call
from PIL import ImageGrab 

class Logger():

	SCREENSHOT_PATH = "data/screenshot.png"
	GUESS_PATH_BASE = "./tmp_tesseract_file"
	GUESS_PATH = GUESS_PATH_BASE + ".txt"

	def __init__(self):
		self.overlay = overlay.Overlay(self)

	def makeScreenshot(self):
		statustext = "Generate Screenshot at {}".format(self.SCREENSHOT_PATH)
		print statustext
		self.overlay.set_status_text(statustext)

		ImageGrab.grab().save(self.SCREENSHOT_PATH)

		self.preprocess_image(self.SCREENSHOT_PATH)

	def preprocess_image(self, image_path, sigma=.8, img_scale_factor=2.7, scale_mode=Image.ANTIALIAS):
		statustext = "Preprocessing"
		print statustext
		self.overlay.set_status_text(statustext)

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

		self.ocr(prepared_path)

	def ocr(self, image_path):
		statustext = "OCR on {} to {}".format(image_path, self.GUESS_PATH_BASE)
		print statustext
		self.overlay.set_status_text(statustext)

		exe_loc = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
		check_call([exe_loc, image_path, self.GUESS_PATH_BASE, "quiet"])

		self.postprocess(self.GUESS_PATH)

	def postprocess(self, guess_path):
		statustext = "Postprocessing"
		print statustext
		self.overlay.set_status_text(statustext)

		guess_text = self.read_text_file(guess_path)
		self.validation(guess_text)

	def validation(self, postprocessed_text):
		statustext = "Validation"
		print statustext
		self.overlay.set_status_text(statustext)

		validated = False
		while not validated:
			# do tests and set validated to true if all of the work properly

			# else: request user intervention 
			postprocessed_text = self.overlay.request_corrections("This is a dummy text. But correct it!!")

		self.concatenate_logs(postprocessed_text)

	def concatenate_logs(self, validated_text_block):
		statustext = "Concatenate logs"
		print statustext
		self.overlay.set_status_text(statustext)

		print validated_text_block

	def read_text_file(self, filepath):
	    opened = open(filepath)
	    content = opened.read()
	    opened.close()
	    return content

	def start(self):
		print "starting logger"
		self.overlay.start()
		print "started logger"

if __name__ == '__main__':
	logger = Logger()
	logger.start()