

import pygame
from pygame.locals import *
import types

def getTextExtents(text,font):
	if type(text) == types.ListType:
		lines = text
	else:
		lines = text.splitlines()
	
	w = 0
	h = 0
	
	for l in lines:
		x,y = font.size(l)
		w = max(x,w)
		h += y
		
	return (w,h)
	
def wrapText(text,font,maxwidth):
	fh = 0
	words = text.split()
	lines = []
	line=""
	for word in words:
		_w,_h = font.size(line+" "+word)
		if _w > maxwidth:
			fh+=_h
			if len(line) == 0:
				lines.append(word)
			else:
				lines.append(line)
				line=word
		else:
			if len(line) > 0:
				line+=" "+word
			else:
				line=word
				
	lines.append(line)
	return lines