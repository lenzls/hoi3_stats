import Tkinter as Tk
import lib.pyhk
import Queue
import threading

class NonRecognizedRequestTypeException(Exception):
	pass

class Overlay():

	REQUEST_STATUS_UPDATE = 1

	def __init__(self, logger):

		#hotkey = lib.pyhk.pyhk()
		self.root_widget = Tk.Tk()
		self.root_widget.attributes("-topmost", 1)
		self.root_widget.title("HoI3_statistics overlay")
		self.root_widget.iconbitmap(default='icon.ico')

		self.logger = logger
		self.frame = Tk.Frame(self.root_widget)
		self.frame.pack()

		self.status_label_text = Tk.StringVar()
		self.status_label_text.set("status label")
		self.status_label = Tk.Label(self.frame, textvariable=self.status_label_text)
		self.status_label.pack(side=Tk.BOTTOM)

		self.correction_text = Tk.Text(self.frame)
		self.correction_text.pack(side=Tk.BOTTOM)
		self.correction_text.insert(1.0, "This is the correction text field")

		self.screenshot_button = Tk.Button(self.frame, text="Screenshot (Ctrl + Alt + s)", command=logger.invoce_logging_action)
		self.screenshot_button.pack(side=Tk.LEFT)

		self.continue_button = Tk.Button(self.frame, text="Continue", command=self.set_correction_text)
		self.continue_button.pack(side=Tk.LEFT)

		self.quit_button = Tk.Button(self.frame, text="Quit", command=self.frame.quit)
		self.quit_button.pack(side=Tk.LEFT)

		#screenshot_shortcut = hotkey.addHotkey(['Ctrl','Alt','S'], logger.invoce_logging_action)

		self.req_queue = Queue.Queue()
		self.res_queue = Queue.Queue()

	def request_corrections(self, invalid_textblock):
		"""the logger requests the user to make corrections to the text"""
		self.set_correction_text(invalid_textblock)
		self.root_widget.update()

	def set_correction_text(self, multiline_String="test"):
		self.correction_text.delete(1.0, Tk.END)
		self.correction_text.insert(1.0, multiline_String)
		
	def set_status_text(self, status_string):
		self.status_label_text.set(status_string)
		self.root_widget.update()

	def check_req_queue(self):
		while not self.req_queue.empty():
			request_code, request_msg = self.req_queue.get()
			if request_code == Overlay.REQUEST_STATUS_UPDATE:
				self.set_status_text(request_msg)
			else:
				raise NonRecognizedRequestTypeException("The request code {} is not known.".format(request_code))
		self.root_widget.after(100, self.check_req_queue)

	def start(self):
		self.root_widget.after(100, self.check_req_queue)
		self.root_widget.mainloop()

if __name__ == '__main__':
	overlay = Overlay(None)
	overlay.start()

