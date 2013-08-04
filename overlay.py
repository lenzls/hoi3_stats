import Tkinter as Tk
import lib.pyhk


class Overlay:
	def __init__(self, master, hotkey, logger):
		self.master = master
		self.logger = logger
		self.frame = Tk.Frame(master)
		self.frame.pack()

		self.status_label_text = Tk.StringVar()
		self.status_label_text.set("status label")
		self.status_label = Tk.Label(self.frame, textvariable=self.status_label_text)
		self.status_label.pack(side=Tk.BOTTOM)

		self.screenshot_button = Tk.Button(self.frame, text="Screenshot (Ctrl + Alt + s)", command=logger.makeScreenshot)
		self.screenshot_button.pack(side=Tk.LEFT)

		self.quit_button = Tk.Button(self.frame, text="Quit", command=self.frame.quit)
		self.quit_button.pack(side=Tk.LEFT)

		screenshot_shortcut = hotkey.addHotkey(['Ctrl','Alt','S'], logger.makeScreenshot)

	def update_status_text(self):
		self.status_label_text.set(self.logger.status_string)
		self.master.update()
		self.frame.after(100, self.update_status_text)

	def start(self):
		self.frame.after(100, self.update_status_text)
		self.master.mainloop()

def init():
	hotkey = lib.pyhk.pyhk()

	root_widget = Tk.Tk()
	root_widget.attributes("-topmost", 1)
	root_widget.title("HoI3_statistics overlay")
	root_widget.iconbitmap(default='icon.ico')
	return root_widget, hotkey

if __name__ == '__main__':
	root_widget, hotkey = init()
	overlay = Overlay(root_widget, hotkey, None)
	overlay.start()

