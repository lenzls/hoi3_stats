import logger
import re
import csv
import codecs

base = "C:\\Program Files (x86)\\Steam\\SteamApps\\common\\Hearts of Iron 3"

def create_variables_list(filepath):
	variables = []

	full_file_lines = logger.read_text_file(filepath, enc="latin1").split("\n")
	event_regex = "(?P<type>[^;]*);(?P<english>[^;]*);.*"
	for line in full_file_lines:
		match = re.match(event_regex, line)
		if match == None:
			continue

		var_regex = "\$.*?\$"
		for var in re.findall(var_regex, match.group("english")):
			if var not in variables:
				variables.append(var)
	variables = [var[1:-1] for var in variables]
	return variables

def print_variables_list(variables):
	for var in variables:
		print "- " + var.encode("utf-8") + " : \n"

def print_template_variables_dict(variables):
	for var in variables:
		print "\"{}\" : \"(?P<{}>[\w ]*)\",".format(var.encode("utf-8"), var.encode("utf-8"))

def print_template_log_msg(variables):
	template_log_msg = " > "
	for var in variables:
		template_log_msg += "{}=${}$ + ".format(var.encode("utf-8"), var.encode("utf-8"))
	print template_log_msg
	return template_log_msg

def check_for_new_variables(relpath):
	var_list = create_variables_list(base + relpath)
	print "in {}".format(relpath)
	print_template_log_msg(var_list)
	#print "in {} aber nicht in bisherigen: ".format(relpath)
	#diff =  set(var_list) - set(everything)
	#print_template_variables_dict(diff)
	#print_variables_list(diff)
	return var_list

def put_template_in_csv():
	# with notepad++:
	#search: ((\w*)_LOG);(.*)
	#replace: \1;\1 > "template string" \3

	# done in:
	# =========
	# unitmessages, 
	# ftm 302 motherland, 
	# Motherland
	# tfh,
	# tfh_4_0
	# tfh_4_1
	# espionage
	# gold
	# diplomatic_messages
	# v1
	# v3
	# messages
	pass


unit_messages_vars = check_for_new_variables("\\localisation\\unit_messages.csv")
ftm_3_02_vars = check_for_new_variables("\\tfh\\localisation\\ftm_3_02.csv")
Motherland_vars = check_for_new_variables("\\tfh\\localisation\\Motherland.csv")
tfh_vars = check_for_new_variables("\\tfh\\localisation\\tfh.csv")
tfh4_0_vars = check_for_new_variables("\\tfh\\localisation\\tfh_4_0.csv")
tfh4_01_vars = check_for_new_variables("\\tfh\\localisation\\tfh_4_01.csv")
espionage_vars = check_for_new_variables("\\tfh\\localisation\\espionage.csv")
gold_vars = check_for_new_variables("\\tfh\\localisation\\gold.csv")

diplomatic_messages_vars = check_for_new_variables("\\localisation\\diplomatic_messages.csv")
v1_vars = check_for_new_variables("\\localisation\\v1.csv")
v3_vars = check_for_new_variables("\\localisation\\v3.csv")
messages_vars = check_for_new_variables("\\localisation\\messages.csv")

#put_template_in_csv(print_template_log_msg(unit_messages_vars), "\\localisation\\unit_messages.csv")