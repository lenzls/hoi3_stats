import Tkinter as Tk
import lib.pyhk
from PIL import ImageGrab 


hot = lib.pyhk.pyhk()

class Overlay:
	def __init__(self, master):
		self.master = master
		self.frame = Tk.Frame(master)
		self.frame.pack()

		self.screenshot_button = Tk.Button(self.frame, text="Screenshot (Ctrl + Alt + s)", command=self.makeScreenshot)
		self.screenshot_button.pack(side=Tk.LEFT)

		self.quit_button = Tk.Button(self.frame, text="Quit", command=self.frame.quit)
		self.quit_button.pack(side=Tk.LEFT)


		screenshot_shortcut = hot.addHotkey(['Ctrl','Alt','S'], self.makeScreenshot)

	def makeScreenshot(self):
		screenshot_path = "data/screenshot.png"
		print "Generate Screenshot at {}".format(screenshot_path)
		ImageGrab.grab().save(screenshot_path)

root_widget = Tk.Tk()
root_widget.attributes("-topmost", 1)
root_widget.title("HoI3_statistics overlay")
root_widget.iconbitmap(default='icon.ico')


overlay = Overlay(root_widget)

root_widget.mainloop()
