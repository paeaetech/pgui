
import pygame
from pygame.locals import *

from OpenGL.GL import *

from draw import Draw
from pgui.state import UIState
from util import SurfaceContext,BlitContext
import math

def quad(pos,size):
	x,y = pos
	w,h = size
	glVertex(x,y)
	glVertex(x+w,y)
	glVertex(x+w,y+h)
	glVertex(x,y+h)

def tofloat(color):
	if len(color) >3:
		r,g,b,a = color
	else:
		r,g,b = color
		a = 255
		
	return ( float(r)/256.0,float(g)/256.0,float(b)/256.0,float(a)/256.0 )
	
class GlDraw(Draw):
	def __init__(self):
		super(GlDraw,self).__init__()
		
	def drawLine(self,posa,posb,color,width=1):
		glEnable(GL_LINE_SMOOTH)
		glEnable(GL_BLEND)
		
		glLineWidth(width)
		glColor(*tofloat(color))
		glBegin(GL_LINE_STRIP)
		glVertex(*posa)
		glVertex(*posb)
		
		glEnd()
#		with SurfaceContext() as screen:
#			pygame.draw.line(screen,color,posa,posb,width)

	def drawLines(self,l,color,closed=False,width=1):
		glEnable(GL_LINE_SMOOTH)
		glEnable(GL_BLEND)

		glLineWidth(width)
		glColor(*tofloat(color))
		if closed:
			glBegin(GL_LINE_LOOP)
		else:
			glBegin(GL_LINE_STRIP)
			
		for v in l:
			glVertex(*v)
			
		glEnd()
		# with SurfaceContext() as screen:
		# 	pygame.draw.lines(screen,color,closed,l,width)

	def fillRect(self,pos,size,color):
		glEnable(GL_BLEND)
		
		glColor(*tofloat(color))
		glBegin(GL_QUADS)
		quad(pos,size)
		glEnd()
		
	def drawRect(self,pos,size,color,width=1):
		glEnable(GL_BLEND)
		
		x,y = pos
		w,h = size
		if width == 0:
			return self.fillRect(pos,size,color)
		self.drawLines([pos,(x+w,y),(x+w,y+h),(x,y+h)],color,True,width)

	def drawArc(self,pos,startangle,endangle,radius,color,width=1):
		glEnable(GL_BLEND)
		
		numdivs = endangle-startangle / 20
		glColor(*tofloat(color))
		if width == 0:
			glBegin(GL_POLYGON)
		else:
			glLineWidth(width)
			glBegin(GL_LINES)
		
		sr = math.radians(startangle)
		er = math.radians(endangle)
		x,y = pos
		for i in range(numdivs):
			r = sr+(er-sr)/float(numdivs)*i
			glVertex(x+math.cos(r)*radius,y+math.sin(r)*radius)
			
		glEnd()
		

	def drawCircle(self,pos,radius,color,width=1):
		glEnable(GL_BLEND)
		
		numdivs = 16
		x,y = pos
		glColor(*tofloat(color))
		if width == 0:
			glBegin(GL_POLYGON)
		else:
			glLineWidth(width)
			glBegin(GL_LINE_LOOP)
		for i in range(numdivs):
			a = (math.pi*2 / float(numdivs))*i
			glVertex(x+math.cos(a)*radius,y+math.sin(a)*radius)
			
		glEnd()

	def drawPolygon(self,l,color,width=1):
		if width > 0:
			return self.drawLines(l,color,True,width)

		glEnable(GL_BLEND)
		glColor(*tofloat(color))
			
		glBegin(GL_POLYGON)
		for v in l:
			glVertex(*v)
		glEnd()

	def fontRender(self,font,text,pos,color):
#		glColor(*tofloat(color))
#		font.render(pos,text)
		# with SurfaceContext(True) as screen:
		surface = font.render(text,True,color)
		data = pygame.image.tostring(surface,"RGBA",True)
		x,y = pos
		glRasterPos(x,y+font.get_linesize())
		glDrawPixels(surface.get_width(),surface.get_height(),GL_RGBA,GL_UNSIGNED_BYTE,data)
		# 	screen.blit(surface,pos,None)


	def drawShadow(self,pos,size):
		pass
	#	with SurfaceContext() as screen:
		# x,y = pos
		# 
		# fillRect((x+6,y+8),size,(0,0,0,180))