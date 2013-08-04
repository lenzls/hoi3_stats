import overlay
from logger import LogAction

class StatLogger():
	def __init__(self):
		self.overlay = overlay.Overlay(self)
		self.logcount = 0

		self.overlay.start()

	def invoce_logging_action(self):
		self.logcount += 1

		LogAction(self.overlay, name="logaction #{}".format(self.logcount)).start()

if __name__ == '__main__':
	StatLogger()