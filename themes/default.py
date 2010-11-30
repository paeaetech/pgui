# coding=utf-8

from pgui.theme import add_theme,Theme,Icons
from pgui.state import UIState
import pgui.textUtils
import math


class DefaultTheme(Theme):
	"""docstring for DefaultTheme"""
	
	Data = {
		"boxColor" : (127,127,127,255),
		"boxActiveColor" : (80,80,127,255),
		
		"boxEdgeColor" : (255,255,255,255),
		"boxEdgeWidth" : 2,
		
		"checkboxFont" : ("Helvetica",12,False,False),
		"checkboxClickedColor" : (80,80,127,255),
		
		"buttonColor" : (63,63,63,255),
		"buttonEdgeColor" : (255,255,255,255),
		"buttonEdgeWidth" : 2,
		"buttonFont" : ("Helvetica",12,False,False),
		"buttonTextColor" : (255,255,255,255),
		"buttonActiveColor" : (80,80,80,255),
		"buttonActiveEdgeColor" : (255,255,255,255),
		"buttonActiveTextColor" : (255,255,255,255),
		"buttonDisabledColor" : (32,32,32,255),
		"buttonDisabledEdgeColor" : (32,32,32,255),
		"buttonDisabledTextColor" : (127,127,127,255),
		"buttonClickedColor" : (80,80,127,255),
		"buttonClickedEdgeColor" : (255,255,255,255),
		"buttonClickedTextColor" : (255,255,255,255),

		"textColor" : (255,255,255,255),
		"textFont" : ("Helvetica",12,False,False),
		"textBoxPadding" : 0,
		
		"iconColor" : (255,255,255,255),
	}
	
	
	def __init__(self):
		super(DefaultTheme,self).__init__()

	def __str__(self):
		return "default"
		
	def load(self):
		super(DefaultTheme,self).load()
		self._loadFont("buttonFont")
		self._loadFont("checkboxFont")
		self._loadFont("textFont")
		
	def drawIcon(self,icon,pos,size,**kwargs):
		super(DefaultTheme,self).drawIcon(icon,pos,size,**kwargs)
		draw = UIState.getDraw()
		
		color = self._get("iconColor")
		x,y = pos
		w,h = size
		if icon == Icons.Move:
			draw.drawRect((x,y),(w,h),color)
			draw.drawCircle((x+w/2,y+h/2),h/4,color)
		elif icon == Icons.MoveActive:
			draw.drawRect((x,y),(w,h),color)
			draw.drawCircle((x+w/2,y+h/2),h/4,color,0)
		elif icon == Icons.Close:
			draw.drawRect((x,y),(w,h),color)
			draw.drawLine((x+2,y+h/2),(x+w-2,y+h/2),color)
		elif icon == Icons.Open:
			draw.drawRect((x,y),(w,h),color)
			draw.drawLine((x+w/2,y+2),(x+w/2,y+h-2),color)
		elif icon == Icons.Resize:
			draw.drawRect((x,y),(w,h),color)
			draw.drawLines([(x+w-4,y+4),(x+w-4,y+h-4),(x+4,y+h-4)],color,True)
		elif icon == Icons.ResizeActive:
			draw.drawRect((x,y),(w,h),color)
			draw.drawPolygon([(x+w-4,y+4),(x+w-4,y+h-4),(x+4,y+h-4)],color,0)
		
	def drawRect(self,pos,size,width,color,**kwargs):
		super(DefaultTheme,self).drawRect(pos,size,width,color,**kwargs)
		draw = UIState.getDraw()

		draw.drawRect(pos,size,color,width)
	
		return (pos,size)
		
	def drawBox(self,pos,size,color=None,**kwargs):
		super(DefaultTheme,self).drawBox(pos,size,color,**kwargs)
		draw = UIState.getDraw()

		active = kwargs.pop("active",False)
		if not color:
			if active:
				color = self._get("boxActiveColor")
			else:
				color = self._get("boxColor")
			
		edgeColor = self._get("boxEdgeColor")
		
#		drawShadow(pos,size)
		draw.fillRect(pos,size,color) 
		x,y = pos
		w,h = size
		width = self._get("boxEdgeWidth",1)
		draw.drawLines([pos,(x+w-width,y),(x+w-width,y+h-width),(x,y+h-width)],edgeColor,True,width)
		
		return (pos,size)

	def drawCheckbox(self,value,pos,size,**kwargs):
		super(DefaultTheme,self).drawCheckbox(value,pos,size,**kwargs)
		draw = UIState.getDraw()

		self.drawBox(pos,size,None,**kwargs)
		lcolor = self._get("boxEdgeColor")
		if value:
			x,y = pos
			w,h = size
			draw.drawLine((x,y),(x+w-1,y+h-2),lcolor,2)
			draw.drawLine((x+w-2,y),(x,y+h-2),lcolor,2)

		return (pos,size)


	def _drawRoundedButton(self,pos,size,color,borderColor,width,textColor,font,text=None,**kwargs):
		simulate = "simulate" in kwargs and kwargs['simulate']

		if text:
			tw,th = font.size(text)
			if not size:
				size = (tw+30,th+10)

		if simulate:
			return (pos,size)

		x,y = pos
		w,h = size
		roundedWidth=h/2.0
		draw = UIState.getDraw()
		

		draw.drawCircle((x+roundedWidth/2.0,y+h/2),roundedWidth,color,0)
		draw.drawCircle((x+w-roundedWidth/2.0,y+h/2),roundedWidth,color,0)

		def getArc(pos,startangle,endangle,radius):
			numdivs = endangle-startangle / 10
			sr = math.radians(startangle)
			er = math.radians(endangle)
			x,y = pos
			points=[]
			for i in range(numdivs):
				r = sr+(er-sr)/float(numdivs)*i
				points.append((x+math.cos(r)*radius,y+math.sin(r)*radius))
				
			return points
		
#		points = []
#		points.extend(getArc((x+roundedWidth/2.0,y+h/2),90,180+90,roundedWidth))
#		points.append((x+roundedWidth/2.0,y))
#		points.append((x+w-roundedWidth/2,y))
#		points.extend(getArc((x+w-roundedWidth/2.0,y+h/2),180+90,180+180+90,roundedWidth))
#		points.append((x+roundedWidth/2.0,y+h))
#		points.append((x+w-roundedWidth/2,y+h))
		draw.drawCircle((x+roundedWidth/2.0,y+h/2),roundedWidth,borderColor,width)
		draw.drawCircle((x+w-roundedWidth/2.0,y+h/2),roundedWidth,borderColor,width)
		draw.drawLine((x+roundedWidth/2.0,y),(x+w-roundedWidth/2,y),borderColor,width)
		draw.drawLine((x+roundedWidth/2.0,y+h),(x+w-roundedWidth/2,y+h),borderColor,width)
#		draw.drawLines(points,borderColor,False,width)
		draw.fillRect((x+roundedWidth/2.0,y+1),(w-roundedWidth,h-2),color)

		if text:
			fx = size[0]/2-tw/2
			fy = size[1]/2-th/2
			draw.fontRender(font,text,(x+fx,y+fy),textColor)

		return (pos,size)

		
	def _drawButton(self,pos,size,color,borderColor,width,textColor,font,text=None,**kwargs):
		simulate = "simulate" in kwargs and kwargs['simulate']
		
		if text:
			tw,th = font.size(text)
			if not size:
				size = (tw+20,th+10)
		
		if simulate:
			return (pos,size)
			
		x,y = pos
		w,h = size
		draw = UIState.getDraw()

		draw.fillRect(pos,size,color)
		draw.drawLines([pos,(x+w-width,y),(x+w-width,y+h-width),(x,y+h-width)],borderColor,True,width)

		if text:
			if kwargs.pop("upper",False):
				text = text.upper()
			elif kwargs.pop("lower",False):
				text = text.lower()
			elif kwargs.pop("capitalize",False):
				text = text.capitalize()
				
			fx = size[0]/2-tw/2
			fy = size[1]/2-th/2-1
			draw.fontRender(font,text,(x+fx,y+fy),textColor)
				
		
		return (pos,size)
			
	def drawButton(self,pos,size=None,text=None,**kwargs):
		pos,size = super(DefaultTheme,self).drawButton(pos,size,text,**kwargs)
		if "straight" in kwargs and kwargs['straight']:
			return self._drawButton(pos,size,self._get("buttonColor"),self._get("buttonEdgeColor"),self._get("buttonEdgeWidth"),self._get("buttonTextColor"),self._getFont("buttonFont"),text,**kwargs)
		return self._drawRoundedButton(pos,size,self._get("buttonColor"),self._get("buttonEdgeColor"),self._get("buttonEdgeWidth"),self._get("buttonTextColor"),self._getFont("buttonFont"),text,**kwargs)
		
	def drawActiveButton(self,pos,size=None,text=None,**kwargs):
		pos,size = super(DefaultTheme,self).drawActiveButton(pos,size,text,**kwargs)
		if "straight" in kwargs and kwargs['straight']:
			return self._drawButton(pos,size,self._get("buttonActiveColor"),self._get("buttonActiveEdgeColor"),self._get("buttonEdgeWidth"),self._get("buttonActiveTextColor"),self._getFont("buttonFont"),text,**kwargs)

		return self._drawRoundedButton(pos,size,self._get("buttonActiveColor"),self._get("buttonActiveEdgeColor"),self._get("buttonEdgeWidth"),self._get("buttonActiveTextColor"),self._getFont("buttonFont"),text,**kwargs)
		
	def drawClickedButton(self,pos,size=None,text=None,**kwargs):
		pos,size = super(DefaultTheme,self).drawClickedButton(pos,size,text,**kwargs)
		if "straight" in kwargs and kwargs['straight']:
			return self._drawButton(pos,size,self._get("buttonClickedColor"),self._get("buttonClickedEdgeColor"),self._get("buttonEdgeWidth"),self._get("buttonClickedTextColor"),self._getFont("buttonFont"),text,**kwargs)

		return self._drawRoundedButton(pos,size,self._get("buttonClickedColor"),self._get("buttonClickedEdgeColor"),self._get("buttonEdgeWidth"),self._get("buttonClickedTextColor"),self._getFont("buttonFont"),text,**kwargs)
		
	def drawDisabledButton(self,pos,size=None,text=None,**kwargs):
		pos,size = super(DefaultTheme,self).drawDisabledButton(pos,size,text,**kwargs)
		if "straight" in kwargs and kwargs['straight']:
			return self._drawButton(pos,size,self._get("buttonDisabledColor"),self._get("buttonDisabledEdgeColor"),self._get("buttonEdgeWidth"),self._get("buttonDisabledTextColor"),self._getFont("buttonFont"),text,**kwargs)

		return self._drawRoundedButton(pos,size,self._get("buttonDisabledColor"),self._get("buttonDisabledEdgeColor"),self._get("buttonEdgeWidth"),self._get("buttonDisabledTextColor"),self._getFont("buttonFont"),text,**kwargs)
		
	def drawText(self,text,pos,size=None,**kwargs):
		pos,size = super(DefaultTheme,self).drawText(text,pos,size,**kwargs)
		draw = UIState.getDraw()
		
		text = unicode(text)
		font = self._getFont("textFont")
		pad = self._get("textBoxPadding")

		lines = None
		if size != None:
			lines = pgui.textUtils.wrapText(text,font,size[0]-pad*2)
		else:
			lines = text.splitlines()
		
		if not size:
			fw,fh = pgui.textUtils.getTextExtents(lines,font)
			size = (fw+pad*2,fh+pad*2)

		if "simulate" in kwargs and kwargs['simulate']:
			return (pos,size)

		x,y = pos
		w,h = size

		color = self._get("textColor")
		tx = x+pad
		ty = y+pad
		
		doCenter = "center" in kwargs and kwargs['center']
		doRight = "right" in kwargs and kwargs['right'] and not doCenter
		
		for line in lines:
			_w,_h = font.size(line)
			lx = 0
			if doCenter:
				lx = w/2-_w/2
			elif doRight:
				lx = w-pad*2-_w
			
			draw.fontRender(font,line,(tx+lx,ty),color)
			ty += _h

		return (pos,size)
		
add_theme("default",DefaultTheme)

