import os
from datetime import datetime
import mss


from tkinter import *
root = Tk(className="Skrinshots")

usr = os.environ['USERPROFILE']
usrShots = usr + os.path.normpath("\\pictures\\Skrinshots")
if not os.path.isdir(usrShots):
	os.mkdir(usrShots)
class FullScreen(object):
	def __init__(self, master, **kwargs):
		initalXY = [0, 0]
		def pos(event):
			x, y = event.x, event.y
			self.cv.coords(rectt, [initalXY[0], initalXY[1], x, y])
		def clickHandler(event):
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

		self.clickTimes = 0
		self.positions = []
		self.master=master
		master.focus_force()
		master.bind('<Escape>', self.master.destroy)

		master.bind('<Button-1>', clickHandler)

		# create drawing canvas
		self.cv = Canvas(master)
		self.cv.pack(fill=BOTH, expand=1)
		rectt = self.cv.create_rectangle(0, 0, 0, 0, outline="blue", fill="black", width=2)
	def takeShot(self, coords):
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
			output = usrShots+f"\\skShot-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.png"

			sct_img = sct.grab(monitor)
			mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
			os.startfile(usrShots)
			return(output)

if __name__ == '__main__':

	app=FullScreen(root)
	root.attributes('-alpha', 0.4)
	root.attributes('-fullscreen', True)
	root.configure(bg="black")

	root.mainloop()