import Tkinter as Tk
import Queue
import threading

class NonRecognizedRequestTypeException(Exception):
	pass

class Overlay():

	REQUEST_STATUS_UPDATE = 1
	REQUEST_CORRECTION = 2

	def __init__(self, logger):

		self.root_widget = Tk.Tk()
		self.root_widget.attributes("-topmost", 1)
		self.root_widget.title("HoI3_statistics overlay")
		self.root_widget.iconbitmap(default='icon.ico')
		self.root_widget.wm_protocol("WM_DELETE_WINDOW", logger.stop)

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

		self.continue_button = Tk.Button(self.frame, text="Continue", command=self.continue_button_pressed)
		self.continue_button.pack(side=Tk.LEFT)

		self.quit_button = Tk.Button(self.frame, text="Quit", command=self.logger.stop)
		self.quit_button.pack(side=Tk.LEFT)

		self.unlock_buttons_except_continue()

		self.req_queue = Queue.Queue()
		self.res_queue = Queue.Queue()

		self.wait_for_gui_continue_event = threading.Event()

		self.root_widget.after(100, self.check_req_queue)

	def set_correction_text(self, multiline_String):
		self.correction_text.delete(1.0, Tk.END)
		self.correction_text.insert(1.0, multiline_String)
		self.root_widget.update()

	def get_correction_text(self):
		return self.correction_text.get(1.0, Tk.END)
		
	def set_status_text(self, status_string):
		self.status_label_text.set(status_string)
		self.root_widget.update()

	def continue_button_pressed(self):
		self.unlock_buttons_except_continue()
		self.wait_for_gui_continue_event.set()
		self.wait_for_gui_continue_event.clear()

	def check_req_queue(self):
		while not self.req_queue.empty():
			request_code, request_msg = self.req_queue.get()
			if request_code == Overlay.REQUEST_STATUS_UPDATE:
				self.set_status_text(request_msg)
			elif request_code == Overlay.REQUEST_CORRECTION:
				self.set_correction_text(request_msg)
				self.lock_buttons_except_continue()
			else:
				raise NonRecognizedRequestTypeException("The request code {} is not known.".format(request_code))
		self.root_widget.after(100, self.check_req_queue)

	def lock_buttons_except_continue(self):
		self.screenshot_button.config(state=Tk.DISABLED)
		self.quit_button.config(state=Tk.DISABLED)
		self.continue_button.config(state=Tk.NORMAL)

	def unlock_buttons_except_continue(self):
		self.screenshot_button.config(state=Tk.NORMAL)
		self.quit_button.config(state=Tk.NORMAL)
		self.continue_button.config(state=Tk.DISABLED)

if __name__ == '__main__':
	overlay = Overlay(None)
	overlay.start()

