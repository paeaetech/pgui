import pygame
from pygame.locals import *
import time




class Buttons:
	Left = 0
	Middle = 1
	Right = 2


class _UIState:
	
	def __init__(self):
		self.activedata = None
		self.hotItem = (0,0)
		self.activeItem = (0,0)
		self.keyboardActive = (0,0)
		self.lastKeyboardActive = (0,0)
		self.mousebuttons = (False,False,False)
		self.clicked = [False,False,False]
		self.layouts = []
		self.repeatkey = None
		self.eventHandler = None
		self.flags = {}
		self.draw = None
		
	def isPressed(self,button):
		return self.mousebuttons[button]
	def isClicked(self,button):
		return self.clicked[button]
	
	def setFlag(self,name,v):
		self.flags[name]=v
	def getFlag(self,name):
		if name in self.flags:
			return self.flags[name]
		return None
	def getDraw(self):
		if not self.draw:
			
			if self.getFlag("opengl"):
				import gldraw
				self.draw = gldraw.GlDraw()
			else:
				import draw
				self.draw = draw.Draw()

		return self.draw
		
	def isActive(self,p,s):
		return self.activeItem == (p,s)
	def isHot(self,p,s):
		return self.hotItem == (p,s)
	def isKeyboardActive(self,p,s):
		return self.keyboardActive == (p,s)
	def wasKeyboardActive(self,p,s):
		return self.lastKeyboardActive == (p,s)

	def doLayout(self,pos,size,**kwargs):
		if len(self.layouts) > 0:
			return self.layouts[0].doLayout(pos,size,**kwargs)
			
		return (pos,size)
	def updateLayout(self,pos,size,**kwargs):
		if len(self.layouts) > 0:
			self.layouts[0].updateLayout(pos,size,**kwargs)
			
	def beginLayout(self,l):
		self.layouts.insert(0,l)
	def endLayout(self):
		self.layouts.pop(0)
		
	def hasActive(self):
		return self.activeItem != (0,0)
	def hasHot(self):
		return self.hotItem != (0,0)
	def hasKeyboardActive(self):
		return self.keyboardActive != (0,0)
		
	def setTheme(self,theme):
		self.theme = theme
	def getTheme(self):
		return self.theme
			
	def setActive(self,p=(0,0),s=(0,0)):
		self.activeItem = (p,s)
	def setHot(self,p=(0,0),s=(0,0)):
		self.hotItem = (p,s)	
		
	def setKeyboardActive(self,p=(0,0),s=(0,0)):
		self.lastKeyboardActive = self.keyboardActive
		self.keyboardActive = (p,s)
		
	def setLastKeyboardActive(self,p=(0,0),s=(0,0)):
		self.lastKeyboardActive = (p,s)
		
	def getKeyboardActive(self):
		return self.keyboardActive
	def getMousePos(self):
		return self.mousepos

	def getActiveData(self):
		return self.activeData
	def setActiveData(self,data):
		self.activeData = data

	def hasKeypresses(self):
		return len(self.keypresses)
	def getKeypress(self):
		if self.hasKeypresses():
			return self.keypresses.pop(0)
		return None
	
	def getScreen(self):
		return self.screen

	def getScreenSize(self):
		return self.screen.get_size()
	
		
	def setEventHandler(self,h):
		self.eventHandler=h
		
	def begin(self,screen,mousepos,mousebuttons,keys=[]):
		self.mousepos = mousepos
		oldmouse = self.mousebuttons
		self.mousebuttons = mousebuttons
		self.keypresses = keys
		self.clicked = [False,False,False]
		
		for i in range(3):
			if mousebuttons[i] and mousebuttons[i] != oldmouse[i]:
				self.clicked[i]=True
		
		self.hotItem = (0,0)
#		self.activeItem = (0,0)
		self.screen = screen
		
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				self.repeatkey = event
				self.repeattime = time.clock()
				self.keypresses.append(event)
			elif event.type == KEYUP:
				self.repeatkey = None
			else:
				if self.eventHandler:
					self.eventHandler(event)
					
		if self.repeatkey:
			if time.clock() - self.repeattime > 0.2:
				self.keypresses.append(self.repeatkey)
				
	def end(self):
		if not self.isPressed(Buttons.Left):
			self.activeItem = (0,0)
			self.activeData = None
		else:
			if not self.hasActive():
				self.activeItem = (-1,-1)
				self.lastKeyboardActive = self.keyboardActive
				self.keyboardActive = (0,0)
				
UIState = _UIState()
	
