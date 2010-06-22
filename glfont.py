# coding=utf-8

from OpenGL.GL import *
import pygame
from pygame.locals import *



class GlFont(object):
	def __init__(self,name):
		self.name = name
		self.lineHeight = 0
	
	def loadFromFont(self,font):
		self.lineHeight = font.get_linesize()
		self.ascent = font.get_ascent()
		self.descent = font.get_descent()
		self.createGlyphs(font)
		self.createTextures(font)
		
	def size(self,text):
		w = 0
		h = self.lineHeight
		for c in text:
			w += self.getGlyphAdvance(c)
		
		return (w,h)
		
	def createGlyphs(self,font):
		self.glyphs = {}
		
		s =""
		for i in xrange(0xffff):
			s += unichr(i)
			
		self.glyphs = font.metrics(s)
	
	def _createTexture(self):
		texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, texture)
		glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
#		glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
#		glTexParameter(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
#		glTexParameter(GL_TEXTURE_2D,GL_TEXTURE_MAX_FILTER,GL_LINEAR)
		return texture
		
	def createTextures(self,font):
		self.glyphtexture = {}
		self.texcoords = {}
		
		x = 0
		y = 0
		size = (1024,1024)
		surface = pygame.Surface(size,SRCALPHA)
		texture = self._createTexture()
		for i in xrange(0xffff):
			s = font.size(unichr(i))
			if s[0] == 0 or s[1] == 0:
				continue
			if s[0] == 3 and s[1] == 9:
				continue
				
			minx,maxx,miny,maxy,advance = self.glyphs[i]
			if x+maxx+1 > size[0]:
				if y+self.lineHeight >= size[1]:
					y = 0
					x = 0
					texture = self._createTexture()
					im = pygame.image.tostring(surface,"RGBA",0)
#					pygame.image.save(surface,"font%s.tga" % i)
					glTexImage2D(GL_TEXTURE_2D,0,GL_ALPHA,size[0],size[1],0,GL_RGBA,GL_BYTE,im)
					surface = pygame.Surface(size,SRCALPHA)
				else:
					y+=self.lineHeight
					x=0

			s = font.render(unichr(i),True,(255,255,255))
			surface.blit(s,(x,y))
			u = float(x)/float(size[0])
			v = float(y)/float(size[1])
			u2 = u+float(maxx)/float(size[0])
			v2 = v+float(self.lineHeight)/float(size[1])
			self.texcoords[i]=(u,v,u2,v2)
			self.glyphtexture[i]=texture
			x+=maxx+1
	
	def render(self,pos,text):
		glEnable(GL_TEXTURE_2D)
		curTex = None
		x,y = pos
		for c in text:
			i = ord(c)
			minx,maxx,miny,maxy,advance = self.glyphs[i]
			
			if i in self.glyphtexture:
				t = self.glyphtexture[i]
				if not curTex or t != curTex:
					if curTex:
						glEnd()
					glBindTexture(GL_TEXTURE_2D,t)
					glBegin(GL_QUADS)
					curTex = t
				u,v,u2,v2 = self.texcoords[i]
			
				glTexCoord2d(u,v)
				glVertex(x,y)
				glTexCoord2d(u2,v)
				glVertex(x+maxx,y)
				glTexCoord2d(u2,v2)
				glVertex(x+maxx,y+self.lineHeight)
				glTexCoord2d(u,v2)
				glVertex(x,y+self.lineHeight)
			x += advance
		if curTex:
			glEnd()
		glDisable(GL_TEXTURE_2D)
		
	def getGlyph(self,c):
		return self.glyphs[ord(c)]

	def getGlyphMinx(self,c):
		return self.glyphs[ord(c)][0]

	def getGlyphMaxx(self,c):
		return self.glyphs[ord(c)][1]

	def getGlyphMiny(self,c):
		return self.glyphs[ord(c)][2]

	def getGlyphMaxy(self,c):
		return self.glyphs[ord(c)][3]
	
	def getGlyphAdvance(self,c):
		return self.glyphs[ord(c)][4]

glfontcache = {}

def gl_load_font(name,size):
	if name in glfontcache:
		for s in glfontcache[name]:
			if s["size"] == size:
				return s["font"]
				
	pyfont = pygame.font.SysFont(name,size)
	
	font = GlFont(name)
	font.loadFromFont(pyfont)
	if not name in glfontcache:
		glfontcache[name]=[]
	
	glfontcache[name].append(dict(size=size,font=font))
	return font
	