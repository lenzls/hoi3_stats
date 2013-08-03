import overlay

class Logger():
	def __init__(self):
		root_widget, hotkey = overlay.init()
		self.window = overlay.Overlay(root_widget, hotkey)

	def start(self):
		self.window.start()

if __name__ == '__main__':
	logger = Logger()
	logger.start()