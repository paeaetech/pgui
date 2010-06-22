

import pygame
from pygame.locals import *
from util import SurfaceContext,BlitContext


class Draw(object):
	def __init__(self):
		pass
	
	def drawLine(self,posa,posb,color,width=1):
		with SurfaceContext() as screen:
			pygame.draw.line(screen,color,posa,posb,width)
	
	def drawLines(self,l,color,closed=False,width=1):
		with SurfaceContext() as screen:
			pygame.draw.lines(screen,color,closed,l,width)
	
	def fillRect(self,pos,size,color):
		with SurfaceContext() as screen:
			pygame.draw.rect(screen,color,pygame.Rect(pos,size),0)
	#		screen.fill(color,pygame.Rect(pos,size))
	
	def drawRect(self,pos,size,color,width=1):
		with SurfaceContext() as screen:
			x,y = pos
			w,h = size
			pygame.draw.rect(screen,color,pygame.Rect(x,y,w,h),width)
	#		drawLine((x,y),(x+w,y),color,width)
	#		drawLine((x+w,y),(x+w,y+h),color,width)
	#		drawLine((x+w,y+h),(x,y+h),color,width)
	#		drawLine((x,y+h),(x,y),color,width)
	
	def drawCircle(self,pos,radius,color,width=1):
		with SurfaceContext() as screen:
			pygame.draw.circle(screen,color,pos,int(radius),int(width))
	
	def drawPolygon(self,l,color,width=1):
		with SurfaceContext() as screen:
			pygame.draw.polygon(screen,color,l,width)
	
	def fontRender(self,font,text,pos,color):
		with SurfaceContext(True) as screen:
			surface = font.render(text,True,color)
			screen.blit(surface,pos,None)


	def drawShadow(self,pos,size):
	#	with SurfaceContext() as screen:
		x,y = pos
	
		fillRect((x+6,y+8),size,(0,0,0,180))