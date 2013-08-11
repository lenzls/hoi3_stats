import overlay
from PIL import Image, ImageOps, ImageFilter
from scipy.misc import imread, imsave
from scipy.ndimage.filters import gaussian_filter
from os.path import splitext
from subprocess import check_call
from PIL import ImageGrab 
import threading
import re
import codecs

class NotCorrectInitializedException(Exception):
	pass

def read_text_file(filepath, mode="r", enc="utf-8"):
    opened = codecs.open(filepath, mode, enc)
    content = opened.read()
    opened.close()
    return content

class LogAction(threading.Thread):

	SCREENSHOT_PATH = "data/screenshot.png"
	GUESS_PATH_BASE = "./tmp_tesseract_file"
	GUESS_PATH = GUESS_PATH_BASE + ".txt"
	PROVINCE_NAMES_PATH = "C:\\Program Files (x86)\\Steam\\SteamApps\\common\\Hearts of Iron 3\\tfh\\mod\\hoi3_stats\\localisation\\province_names.csv"
	EVENT_PATTERNS_PATH = "C:\\Program Files (x86)\\Steam\\SteamApps\\common\\Hearts of Iron 3\\tfh\\mod\\hoi3_stats\\localisation\\unit_messages.csv"
	LOG_POSITION = (861, 815)  # position of the game log in absolute screen coordinates
	LOG_DIMENSIONS = (437, 139)  # dimensions of the game log

	provinces_list = []
	event_patterns = {}


	time_regex = "([0-9]|1[0-9]|2[0-3]):([0-5][0-9])"
	day_regex = "([1-9]|1[0-9]|2[0-9]|3[0-1])"
	month_regex = "(January|February|March|April|May|June|July|August|September|October|November|Decemeber)"
	year_regex = "(19(?:2[6-9]|4[0-8]))"
	date_regex = "{}, {} {}, {}".format(time_regex, day_regex, month_regex, year_regex)

	@staticmethod
	def generate_provinces_list(debug=False):
		print "generating provinces list"
		full_file_lines = read_text_file(LogAction.PROVINCE_NAMES_PATH).split("\n")
		prov_regex = "(?P<generic_name>[^;]*);(?P<english>[^;]*);.*"
		LogAction.provinces_list = [re.match(prov_regex, line).group("english") for line in full_file_lines if not re.match(prov_regex, line) == None]
		if debug:
			print "{} provinces found".format(len(LogAction.provinces_list))
			print "Here are the first entries:"
			for line in LogAction.provinces_list[:11]:
				print "{} : {}".format(type(line), line.encode("utf-8"))

	@staticmethod
	def generate_event_pattern_dict(debug=False):
		print "generating event pattern dictionary"

		def replace_variables_to_regex(line):
			variables = {
				"chief_of_navy" : "(?P<chief_of_navy>[\w ]*)",
				"MONARCHTITLE" : "(?P<MONARCHTITLE>[\w ]*)",
				"OUR_FLEET" : "(?P<OUR_FLEET>[\w ]*)",
				"PROV" : "(?P<PROV>[\w ]*)",
				"OTHER" : "(?P<OTHER>[\w ]*)",
				"OTHERS" : "(?P<OTHERS>[\w ]*)",
				"RESERVE" : "(?P<RESERVE>[\w ]*)",
				"TARGET" : "(?P<TARGET>[\w ]*)",
				"CAP" : "(?P<CAP>[\w ]*)",
				"SUB" : "(?P<SUB>[\w ]*)",
				"chief_of_air" : "(?P<chief_of_air>[\w ]*)",
				"NUM" : "(?P<NUM>[\w ]*)",
				"minister_of_security" : "(?P<minister_of_security>[\w ]*)",
				"COUNTRY" : "(?P<COUNTRY>[\w ]*)",
				"chief_of_staff" : "(?P<chief_of_staff>[\w ]*)",
				"TYPE" : "(?P<TYPE>[\w ]*)",
				"NAME" : "(?P<NAME>[\w ]*)",
				"SCR" : "(?P<SCR>[\w ]*)",
				"TRA" : "(?P<TRA>[\w ]*)",
				"BRIG" : "(?P<BRIG>[\w ]*)",
				"UNIT" : "(?P<UNIT>[\w ]*)",
				"MEN" : "(?P<MEN>[\w ]*)",
				"FIG" : "(?P<FIG>[\w ]*)",
				"BOM" : "(?P<BOM>[\w ]*)",
				"DEFENDER" : "(?P<DEFENDER>[\w ]*)",
				"ATTACKER" : "(?P<ATTACKER>[\w ]*)",
				"ATTUNIT" : "(?P<ATTUNIT>[\w ]*)",
				"DEFUNIT" : "(?P<DEFUNIT>[\w ]*)",
				"chief_of_army" : "(?P<chief_of_army>[\w ]*)",
				"RESULT" : "(?P<RESULT>[\w ]*)",
				"USLOSS" : "(?P<USLOSS>[\w ]*)",
				"USNUM" : "(?P<USNUM>[\w ]*)",
				"OTHERRESULT" : "(?P<OTHERRESULT>[\w ]*)",
				"THEIRNUM" : "(?P<THEIRNUM>[\w ]*)",
				"THEIRLOST" : "(?P<THEIRLOST>[\w ]*)",
				"SHIPS" : "(?P<SHIPS>[\w ]*)",
				"THEIRSHIP" : "(?P<THEIRSHIP>[\w ]*)",
				"ORDER" : "(?P<ORDER>[\w ]*)",
				"DAMAGE" : "(?P<DAMAGE>[\w ]*)",
				"ATTACKER_ADJ" : "(?P<ATTACKER_ADJ>[\w ]*)",
				"DAMAGE_SHORT" : "(?P<DAMAGE_SHORT>[\w ]*)",
				"SIZE" : "(?P<SIZE>[\w ]*)",
				"SUNK" : "(?P<SUNK>[\w ]*)"
			}
			for var in variables.keys():
				regex = variables[var]
				line = line.replace("${}$".format(var), regex)
			return line

		full_file_lines = read_text_file(LogAction.EVENT_PATTERNS_PATH, enc="latin1").split("\n")
		event_regex = "(?P<type>[^;]*);(?P<english>[^;]*);.*"
		for line in full_file_lines:
			match = re.match(event_regex, line)
			if match == None:
				continue
			if match.group("type").endswith("LOG"):
				LogAction.event_patterns[match.group("type")] = replace_variables_to_regex(match.group("english"))

		if debug:
			print "{} event patterns found".format(len(LogAction.event_patterns))
			print "Here are the first entries:"
			for pat_name in LogAction.event_patterns.keys()[:11]:
				print "{} : {} : {}".format(type(pat_name), pat_name.encode("utf-8"), LogAction.event_patterns[pat_name].encode("utf-8"))

	def __init__(self, overlay, **kwargs):
		print len(LogAction.provinces_list)
		if len(LogAction.provinces_list) == 0:
			print "Please generate provinces list before logging"
			raise NotCorrectInitializedException("Provinces list not generated")

		threading.Thread.__init__(self, **kwargs)
		self.overlay = overlay

	def makeScreenshot(self):
		statustext = "Generate Screenshot at {}".format(self.SCREENSHOT_PATH)
		print statustext
		self.overlay.req_queue.put((overlay.Overlay.REQUEST_STATUS_UPDATE, statustext))

		ImageGrab.grab().save(self.SCREENSHOT_PATH)

		self.preprocess_image(self.SCREENSHOT_PATH)

	def preprocess_image(self, image_path, sigma=.8, img_scale_factor=2.7, scale_mode=Image.ANTIALIAS):
		statustext = "Preprocessing"
		print statustext
		self.overlay.req_queue.put((overlay.Overlay.REQUEST_STATUS_UPDATE, statustext))

		image = Image.open(image_path)
		prepared_path = splitext(image_path)[0] + "-edited.png"

		# crop the gamelog out
		x1 = self.LOG_POSITION[0]
		y1 = self.LOG_POSITION[1]
		x2 = self.LOG_POSITION[0] + self.LOG_DIMENSIONS[0]
		y2 = self.LOG_POSITION[1] + self.LOG_DIMENSIONS[1]
		image = image.crop((x1, y1, x2, y2))

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
		self.overlay.req_queue.put((overlay.Overlay.REQUEST_STATUS_UPDATE, statustext))

		exe_loc = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
		check_call([exe_loc, image_path, self.GUESS_PATH_BASE, "quiet"])

		self.postprocess(self.GUESS_PATH)

	def postprocess(self, guess_path):
		statustext = "Postprocessing"
		print statustext
		self.overlay.req_queue.put((overlay.Overlay.REQUEST_STATUS_UPDATE, statustext))

		guess_text = read_text_file(guess_path)

		def split_text_in_message_lines(multiline_text):
			text = multiline_text
			# split on new line
			lines = text.split("\n")
			# remove empty lines
			#print lines
			lines = [line for line in lines if not line == ""]
			#print lines

			return lines

		message_lines = split_text_in_message_lines(guess_text)

		self.validation(message_lines)

	def validation(self, message_lines):
		statustext = "Validation"
		print statustext
		self.overlay.req_queue.put((overlay.Overlay.REQUEST_STATUS_UPDATE, statustext))

		def check_for_pattern(line):
			found = 0
			for name in LogAction.event_patterns.keys():
				event_pattern = LogAction.event_patterns[name]
				pattern = "{} {}".format(LogAction.date_regex, event_pattern)
				#print "searching for pattern {} in {}".format(pattern, line.encode("utf-8"))
				if re.match(pattern, line):
					found += 1
					print "Pattern \"{}\" matched for line: {}".format(name, line.encode("utf-8"))
			print "Found {} pattern matching this line.".format(found)

		for line in message_lines:
			check_for_pattern(line)

		validated = True
		while not validated:
			# do tests and set validated to true if all of the work properly

			# else: request user intervention 
			self.overlay.req_queue.put((overlay.Overlay.REQUEST_CORRECTION, "This is a dummy text. But correct it!!"))
			self.overlay.wait_for_gui_continue_event.wait()
			corrected_text = self.overlay.get_correction_text()
			#splitting, rechecking...

			validated = True

		self.concatenate_logs(message_lines)

	def concatenate_logs(self, validated_msg_lines):
		statustext = "Concatenate logs"
		print statustext
		self.overlay.req_queue.put((overlay.Overlay.REQUEST_STATUS_UPDATE, statustext))

		for line in validated_msg_lines:
			print line.encode("utf-8")

	def run(self):
		self.makeScreenshot()

if __name__ == '__main__':
	logger = Logger()
	logger.start()