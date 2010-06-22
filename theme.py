
import pygame
from state import UIState

theme_list = {}

def add_theme(name,theme):
	print "added theme",name
	theme_list[name]=theme

def load_theme(name):
	l = theme_list[name]
	t = l()
	t.load()
	return t
	
def list_themes():
	return theme_list


class Icons:
	Move = 0
	MoveActive = 1
	Close = 2
	Open = 3
	Resize = 4
	ResizeActive = 5
	MAX = 6
	

class Theme(object):
	"""docstring for Theme"""
	
	def __init__(self):
		pass

	def load(self):
		pass
	
	def drawIcon(self,icon,pos,size,**kwargs):
		pass
	
	def drawRect(self,pos,size,width,color,**kwargs):
		return (pos,size)

	def drawBox(self,pos,size,color=None,**kwargs):
		"""docstring for drawBox"""
		return (pos,size)
		
	def drawButton(self,pos,size=None,text=None,**kwargs):
		"""docstring for drawButton"""
		return (pos,size)
	
	def drawActiveButton(self,pos,size=None,text=None,**kwargs):
		return (pos,size)
		
	def drawClickedButton(self,pos,size=None,text=None,**kwargs):
		"""docstring for drawClickedButton"""
		return (pos,size)
		
	def drawDisabledButton(self,pos,size=None,text=None,**kwargs):
		"""docstring for drawDisabledButton"""
		return (pos,size)
	
	def drawText(self,text,pos,size=None,**kwargs):
		return (pos,size)

	def drawCheckbox(self,value,pos,size,**kwargs):
		return (pos,size)
		
	def _loadFont(self,name):
		font,size,bold,italic = self._get(name)

#		if UIState.getFlag("opengl"):
#			from glfont import gl_load_font
#			self.Data['_font'+name] = gl_load_font(font,size)
#		else:
		self.Data['_font'+name] = pygame.font.SysFont(font,size,bold,italic)
		
	def _getFont(self,name):
		return self._get("_font"+name)
		
	def _get(self,name,default=None):
		if "Data" in self.__class__.__dict__:
			if name in self.Data:
				return self.Data[name]
				
		return default
		
	def getFont(self,name):
		return self._getFont(name)
		
	def getParam(self,name):
		return self._get(name)
	
	def __str__(self):
		return "theme"
		