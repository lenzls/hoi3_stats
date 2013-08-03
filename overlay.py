import Tkinter as Tk

class Overlay:
	def __init__(self, master):
		frame = Tk.Frame(master)
		frame.pack()

		self.but1 = Tk.Button(frame, text="Quit", command=frame.quit)
		self.but1.pack(side=Tk.LEFT)

		self.but2 = Tk.Button(frame, text="Hey", command=self.printThis)
		self.but2.pack(side=Tk.LEFT)

	def printThis(self):
		print "hello"

root_widget = Tk.Tk()

overlay = Overlay(root_widget)

root_widget.mainloop()
