import overlay
from logger import LogAction
import threading
import pyHook
import pythoncom
import win32api
import win32con
import time

class HotkeyManager():
	def __init__(self, app):
		self.app = app
		self.hm = pyHook.HookManager()
		print "hkm initialized"
		self.hm.KeyDown = self.OnKeyboardEvent
		self.hm.HookKeyboard()

	def OnKeyboardEvent(self, event):
	    #    print 'MessageName:',event.MessageName
		#    print 'Message:',event.Message
		#    print 'Time:',event.Time
		#    print 'Window:',event.Window
		#    print 'WindowName:',event.WindowName
		#    print 'Ascii:', event.Ascii, chr(event.Ascii)
		#    print 'Key:', event.Key
		#print 'KeyID:', event.KeyID
		#    print 'ScanCode:', event.ScanCode
		#    print 'Extended:', event.Extended
		#    print 'Injected:', event.Injected
		#    print 'Alt', event.Alt
		#    print 'Transition', event.Transition

		# ctrl + c
		#if event.Ascii == 3:
		#	print "yeag... quit.."
		#	self.app.stop()

		# F9
		if event.KeyID == 120:
			print 'F9'
			self.app.invoce_logging_action()

		# alt + F8
		if event.Alt == 32 and event.KeyID == 119:
			print 'alt+f8'

		# return True to pass the event to other handlers
		return True


class StatLogger():
	def __init__(self):
		self.overlay = overlay.Overlay(self)
		self.hkm = HotkeyManager(self)
		self.logcount = 0
		self.running = True

		LogAction.generate_provinces_list()

		self.start()

	def invoce_logging_action(self):
		self.logcount += 1

		LogAction(self.overlay, name="logAction #{}".format(self.logcount)).start()

	def stop(self):
		self.running = False

	def start(self):
		while self.running:
		    self.overlay.root_widget.after(100, self.overlay.root_widget.quit)
		    self.overlay.root_widget.mainloop()
		    pythoncom.PumpWaitingMessages()

if __name__ == '__main__':
	StatLogger()