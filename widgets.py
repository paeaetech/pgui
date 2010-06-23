
from pgui.state import UIState
from pgui.util import *
from pgui.errors import *
from pgui.util import SurfaceContext
import pgui.textUtils
import time
import types

from pygame.locals import *

def Button(text=None,pos=None,size=None,**kwargs):
	ret = False
	
	theme = UIState.getTheme()
	
	pos,size = theme.drawButton(pos,size,text,simulate=True,**kwargs)
	pos,size = UIState.doLayout(pos,size,**kwargs)
	
	disabled = "disabled" in kwargs and kwargs['disabled']
	disabledFunc = None
	if disabled:
		disabledFunc = theme.drawDisabledButton
	
	drawFunc = theme.drawButton
	
	if mouseIsInside(pos,size):
		if not disabled:
			UIState.setHot(pos,size)
			drawFunc = theme.drawActiveButton
			
			if mousePressed():
				if not UIState.hasActive():
					UIState.setActive(pos,size)
					UIState.setKeyboardActive()
					
			else:
				if UIState.isActive(pos,size):
					ret = True
					UIState.setActive()
	else:
		if UIState.isActive(pos,size):
			UIState.setActive()

	if UIState.isActive(pos,size):
		drawFunc = theme.drawClickedButton
		
	drawFunc = disabledFunc or drawFunc
	drawFunc(pos,size,text,**kwargs)
	UIState.updateLayout(pos,size,**kwargs)
	
	return ret

def CheckedButton(value,text=None,pos=None,size=None,**kwargs):
	ret = False

	theme = UIState.getTheme()

	pos,size = theme.drawButton(pos,size,text,simulate=True,**kwargs)
	pos,size = UIState.doLayout(pos,size,**kwargs)

	disabled = "disabled" in kwargs and kwargs['disabled']
	disabledFunc = None
	if disabled:
		disabledFunc = theme.drawDisabledButton

	drawFunc = theme.drawButton

	if mouseIsInside(pos,size):
		if not disabled:
			UIState.setHot(pos,size)
			drawFunc = theme.drawActiveButton

			if mousePressed():
				if not UIState.hasActive():
					UIState.setActive(pos,size)
					UIState.setKeyboardActive()
					
			else:
				if UIState.isActive(pos,size):
					if value:
						value = False
					else:
						value = True
					UIState.setActive()
	else:
		if UIState.isActive(pos,size):
			UIState.setActive()

	if value:
		drawFunc = theme.drawClickedButton

	drawFunc = disabledFunc or drawFunc
	drawFunc(pos,size,text,**kwargs)
	UIState.updateLayout(pos,size,**kwargs)

	return value


	
def ScrollBar(value,minvalue=0,maxvalue=255,pos=None,size=None,**kwargs):
	
	# if type(value) != types.ListType:
	# 	raise ParameterError("value needs to be list")
	
	theme = UIState.getTheme()
	disabled = "disabled" in kwargs and kwargs['disabled']

	pos,size = theme.drawBox(pos,size,simulate=True,**kwargs)
	pos,size = UIState.doLayout(pos,size,**kwargs)
	
	isint = type(value) == types.IntType

	mx,my = UIState.getMousePos()
	
	x,y = pos
	w,h = size
	sliderh = h - 4
	bh = 10
	bw = w-4
	
	v = float(value - minvalue) / float(maxvalue)
	
	bx = x+2
	by = v * (sliderh-bh)
	
	drawFunc = theme.drawButton
	
	if mouseIsInside(pos,size):
		if not disabled:
			UIState.setHot(pos,size)
			drawFunc = theme.drawActiveButton
			
			if mousePressed():
				if not UIState.hasActive():
					UIState.setActive(pos,size)
					UIState.setKeyboardActive()
					
			else:
				if UIState.isActive(pos,size):
					UIState.setActive()
					
	active = UIState.isActive(pos,size)
	
	theme.drawBox(pos,size,active=active,**kwargs)
	if active:
		my = min(max(y,my),y+h)
		v = float(my-y)/float(h)
		drawFunc = theme.drawClickedButton
	 	
	drawFunc((bx,y+by+2),(bw-1,bh),straight=True)
	
	UIState.updateLayout(pos,size,**kwargs)
	
	
	retv = minvalue + v * (maxvalue-minvalue)
	if isint:
		return int(retv)
	
	return retv
	
	
def TextBox(text,pos=None,size=None,**kwargs):
	theme = UIState.getTheme()

	pos,size = theme.drawText(text,pos,size,simulate=True,**kwargs)
	pos,size = UIState.doLayout(pos,size,**kwargs)
	x,y = pos
	w,h = size
	theme.drawBox(pos,size,**kwargs)
	theme.drawText(text,(x+5,y+5),(w-10,h-10),**kwargs)
	UIState.updateLayout(pos,size,**kwargs)

def Text(text,pos=None,size=None,**kwargs):
	theme = UIState.getTheme()

	pos,size = theme.drawText(text,pos,size,simulate=True,**kwargs)
	pos,size = UIState.doLayout(pos,size,**kwargs)
#	theme.drawBox(pos,size,**kwargs)
	theme.drawText(text,pos,size,**kwargs)
	UIState.updateLayout(pos,size,**kwargs)


def CheckBox(value,text,pos=None,size=None,**kwargs):
	theme = UIState.getTheme()
	
	xsize = 16
	boxsize = (xsize,xsize)
	
	if not size and text:
		pos,textsize = theme.drawText(text,pos,size,simulate=True,**kwargs)
		boxsize = (textsize[1]+4,textsize[1]+4)
		size = (textsize[0]+boxsize[0]+4,textsize[1])
	else:
		size = boxsize
		
	pos,size = UIState.doLayout(pos,size,**kwargs)
	disabled = "disabled" in kwargs and kwargs['disabled']
	
	if mouseIsInside(pos,boxsize):
		if not disabled:
			UIState.setHot(pos,boxsize)
			
			if mousePressed():
				if not UIState.hasActive():
					UIState.setActive(pos,boxsize)
					UIState.setKeyboardActive()
					
			else:
				if UIState.isActive(pos,boxsize):
					UIState.setActive()
					if value:
						value = False
					else:
						value = True
	
	theme.drawCheckbox(value,pos,boxsize,active=UIState.isActive(pos,boxsize))

	if text:
		theme.drawText(text,(pos[0]+4+boxsize[0],pos[1]),textsize,checkbox=True,**kwargs)
	
	UIState.updateLayout(pos,size,**kwargs)
	
	return value

def EditText(text,pos=None,size=None,**kwargs):
	theme = UIState.getTheme()
	
	ret = False
	disabled = "disabled" in kwargs and kwargs['disabled']
	maxlength = kwargs.pop("max_length",255)
	font = theme.getFont("textFont")
	if not size:
		size = (None,font.get_linesize())
		
#	_p,textsize = theme.drawText(text,pos,size,simulate=True,**kwargs)
	pos,size = UIState.doLayout(pos,size,**kwargs)
	
	if mouseIsInside(pos,size):
		if not disabled:
			UIState.setHot(pos,size)
		
			if mousePressed():
				if not UIState.hasKeyboardActive():
					UIState.setKeyboardActive(pos,size)
					UIState.setActive(pos,size)
					data = {
						"cursorpos" : len(text),
						
					}
					UIState.setActiveData(data)
	
	if UIState.isKeyboardActive(pos,size):
		data = UIState.getActiveData()
		
#		if not UIState.isActive(pos,size):
#			UIState.setKeyboardActive()
#		else:
		breakKeys = [K_RETURN,K_TAB,K_ESCAPE]
		
		while UIState.hasKeypresses():
			k = UIState.getKeypress()
			if k.key in breakKeys: # K_RETURN or k.key == K_TAB or k.key == K_ESCAPE:
				UIState.setKeyboardActive()
#				UIState.setActive()
				UIState.setLastKeyboardActive()
				ret = True
				break
			elif k.key == K_BACKSPACE:
				text = text[:-1]
			elif k.unicode != '':
				if len(text) < maxlength:
					text += k.unicode
	elif UIState.wasKeyboardActive(pos,size):
		ret = True
		UIState.setLastKeyboardActive()
		
	if not size:
		size = (textsize[0]+4,textsize[1]+4)

	
	
	theme.drawBox(pos,size,active=UIState.isKeyboardActive(pos,size),**kwargs)
	theme.drawText(text,(pos[0]+2,pos[1]+2),size,**kwargs)
	
	if UIState.isKeyboardActive(pos,size):
		if time.clock()*1000 % 500 < 250:
			x,y = pos
			if len(text) > 0:
				w,h = pgui.textUtils.getTextExtents(text,font)
			else:
				w = 2
				h = size[1]-6
#			with SurfaceContext() as screen:
			draw = UIState.getDraw()
			draw.drawLine((x+2+w,y+4),(x+2+w,y+h),(255,255,255,255),1)
		
#	value[0] = text
	
	UIState.updateLayout(pos,size,**kwargs)
	return text,ret
	