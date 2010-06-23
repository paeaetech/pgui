
import pygame
from pygame.locals import *

from state import UIState

class Screen(object):
	"""docstring for PGui"""
	def __init__(self, size,**kwargs):
		pygame.init()
		self.icon = None
		
		if "title" in kwargs:
			pygame.display.set_caption(kwargs['title'])
		if "icon" in kwargs:
			self.icon = pygame.image.load(kwargs['icon'])
			pygame.display.set_icon(self.icon)

		self.size = size
		flags = HWSURFACE|DOUBLEBUF|RESIZABLE
		self.opengl =  "opengl" in kwargs
		
		if self.opengl:
			from OpenGL.GL import *
			from OpenGL.GLU import *
			from OpenGL.GLUT import *
			
			flags |= OPENGL
			
		self.screen = pygame.display.set_mode(size, flags,32)
		
		if self.opengl: 
			self.initGL(*self.size)
			UIState.setFlag("opengl",True)
			
	def getSize(self):
		return self.size
		
	def getScreen(self):
		return self.screen
		
	def initGL(self,w,h):
		self.resize(w,h)
		glClearColor(0,0,0,0)
		glShadeModel(GL_FLAT)
		glDisable(GL_ALPHA_TEST)
		glDisable(GL_DITHER)
#		glEnable(GL_LINE_SMOOTH)
		glDisable(GL_DEPTH_TEST)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	def resize(self,width, height):
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, width,height, 0, 0, 1)
		
#		gluPerspective(60.0, float(width)/height, .1, 1000.)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()


	def beginFrame(self,clearcolor=(0,0,0,0)):
		if self.opengl:
			glClearColor(*clearcolor)
			glClear(GL_COLOR_BUFFER_BIT)
			pass
		else:
			self.screen.fill(clearcolor)
		pass
		
	def endFrame(self):
		self.flip()
		
	def flip(self):
		pygame.display.flip()
#		glutSwapBuffers()
		