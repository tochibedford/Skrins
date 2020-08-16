import os
from sys import exit
from datetime import datetime
import mss
from PIL import Image as imm
from PIL import ImageOps
from PIL import ImageDraw

from tkinter import *
root = Tk(className="Skrinshots")

usr = os.environ['USERPROFILE']
usrShots = usr + os.path.normpath("\\pictures\\Skrinshots")
if not os.path.isdir(usrShots):
	os.mkdir(usrShots)

class FullScreen(object):
	def __init__(self, master, **kwargs):
		initalXY = [0, 0]
		self.circleMode	= False
		def pos(event):
			if not self.circleMode:
				x, y = event.x, event.y
				self.cv.coords(rectt, [initalXY[0], initalXY[1], x, y])
			else:
				x, y = event.x, event.y
				if x > 0 and y > 0:
					self.cv.coords(circc, [initalXY[0], initalXY[1], x, x-initalXY[0]+initalXY[1]])
		def clickHandler(event):
			if not self.circleMode:
				if self.clickTimes == 0:
					initalXY[0] = event.x
					initalXY[1] = event.y
					self.master.bind('<Motion>', pos)
				self.clickTimes += 1
				self.positions.append([event.x, event.y])
				if self.clickTimes == 2:
					self.master.unbind("<Button 1>")
					self.master.unbind('<Motion>')
					self.cv.coords(rectt, [0,0,0,0])
					self.master.wm_state('iconic')
					self.takeShot(self.positions)
					self.master.destroy()
			else:
				if self.clickTimes == 0:
					initalXY[0] = event.x
					initalXY[1] = event.y
					self.master.bind('<Motion>', pos)
				self.clickTimes += 1
				self.positions.append([event.x, event.x-initalXY[0]+initalXY[1]])
				if self.clickTimes == 2:
					self.master.unbind("<Button 1>")
					self.master.unbind('<Motion>')
					self.cv.coords(circc, [0,0,0,0])
					self.master.wm_state('iconic')
					self.takeShot(self.positions, "circle")
					self.master.destroy()
		def clickHandlerCirc(event):
			self.circleMode	= True
			self.cv.coords(rectt, [0,0,0,0])

		def clickHandlerRect(event):
			self.circleMode	= False
			self.cv.coords(circc, [0,0,0,0])

		self.clickTimes = 0
		self.positions = []
		self.master=master
		master.focus_force()
		master.bind('<Escape>', exit)
		master.bind('<Button-1>', clickHandler)
		master.bind('2', clickHandlerCirc)
		master.bind('1', clickHandlerRect)

		# create drawing canvas
		self.cv = Canvas(master)
		self.cv.pack(fill=BOTH, expand=1)
		rectt = self.cv.create_rectangle(0, 0, 0, 0, outline="blue", fill="black", width=2)
		circc = self.cv.create_oval(0, 0, 0, 0, outline="blue", fill="black", width=2)

	def takeShot(self, coords, shape="rect"):
		with mss.mss() as sct:
			top = coords[0][1]
			left = coords[0][0]
			width = coords[1][0]-coords[0][0]
			height = coords[1][1]-coords[0][1]
			if width<0:
				left += width
				width = 0-width
			if height<0:
				top += height
				height = 0-height
			monitor = {
			"top": top,
			"left": left,
			"width": width,
			"height": height}
			now = datetime.now()
			if shape == "rect":
				output = usrShots+f"\\skShot-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.png"
				sct_img = sct.grab(monitor)
				mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
				os.startfile(usrShots)
				return(output)
			elif shape == "circle":
				output = usrShots+f"\\skShot-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.png"
				sct_img = sct.grab(monitor)
				mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)		

				# mask to circle			
				im = imm.open(output)
				bigsize = (im.size[0] * 3, im.size[1] * 3)
				mask = imm.new('L', bigsize, 0)
				draw = ImageDraw.Draw(mask) 
				draw.ellipse((0, 0) + bigsize, fill=255)
				mask = mask.resize(im.size, imm.ANTIALIAS)
				im.putalpha(mask)
				outputt = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
				outputt.putalpha(mask)
				outputt.save(output)
				os.startfile(usrShots)
				return(output)

if __name__ == '__main__':
	app=FullScreen(root)
	root.attributes('-alpha', 0.4)
	root.attributes('-fullscreen', True)
	root.configure(bg="black")
	root.mainloop()