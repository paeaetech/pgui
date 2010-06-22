

from pgui.state import UIState,Buttons

import math

class SurfaceContext(object):
	"""docstring for SurfaceContext"""
	def __init__(self,nolock=False):
		self.surface = UIState.screen
		self.lock = not nolock
	def __enter__(self):
		if self.lock:
			self.surface.lock()
		return self.surface
		
	def __exit__(self,exc_type, exc_value, traceback):
		if self.lock:
			self.surface.unlock()

class BlitContext(object):
	"""docstring for SurfaceContext"""
	def __init__(self,surface):
		self.surface = surface

	def __enter__(self):
		self.count = 0
		while self.surface.get_locked():
			self.surface.unlock()
			self.count += 1
			
		return self.surface

	def __exit__(self,exc_type, exc_value, traceback):
		for i in range(self.count):
			self.surface.lock()

		
def isInside(mpos,pos,size,**kwargs):
		mx,my = mpos
		x,y = pos
		w,h = size

		if "circle" in kwargs:
			r = kwargs['radius']
			_x = mx-x
			_y = my-y
			l = math.sqrt(_x*_x + _y*_y)
			if l < r:
				return True
		else:
			if mx >= x and mx < x+w and my >= y and my < y+h:
				return True

		return False


def mouseIsInside(pos,size,**kwargs):
	return isInside(UIState.getMousePos(),pos,size,**kwargs)
	
def mousePressed():
	return UIState.isPressed(Buttons.Left)
	
def mouseClicked():
	return UIState.isClicked(Buttons.Left)