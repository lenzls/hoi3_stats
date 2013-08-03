import Tkinter as Tk
import lib.pyhk
from PIL import ImageGrab 


class Overlay:
	def __init__(self, master, hotkey):
		self.master = master
		frame = Tk.Frame(master)
		frame.pack()

		self.screenshot_button = Tk.Button(frame, text="Screenshot (Ctrl + Alt + s)", command=self.makeScreenshot)
		self.screenshot_button.pack(side=Tk.LEFT)

		self.quit_button = Tk.Button(frame, text="Quit", command=frame.quit)
		self.quit_button.pack(side=Tk.LEFT)


		screenshot_shortcut = hotkey.addHotkey(['Ctrl','Alt','S'], self.makeScreenshot)

	def makeScreenshot(self):
		screenshot_path = "data/screenshot.png"
		print "Generate Screenshot at {}".format(screenshot_path)
		ImageGrab.grab().save(screenshot_path)

	def start(self):
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
	overlay = Overlay(root_widget, hotkey)
	overlay.start()

