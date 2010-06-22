#!/usr/bin/env python
# coding=utf-8

from pgui.theme import list_themes,load_theme,Icons
from pgui.themes import default,better
from pgui.state import UIState
from pgui.screen import Screen
from pgui.widgets import *
from pgui.layout import *
import pgui.draw
#import pgui.gldraw

import pygame
from pygame.locals import *

def main():
	screen = Screen((1024,720),title="pgui")

	themes = [] # load_theme("default")]
	for theme in list_themes():
		print "loading theme",theme
		themes.append(load_theme(theme))
	UIState.setTheme(themes[0])
	curtheme=0

	def handleEvent(event):
		if event.type == VIDEORESIZE:
			screen.resize(*event.size)
		
	UIState.setEventHandler(handleEvent)
	
	value = 100
	cv = False
	bv = True
	text = "jee"
	try:
		exit = False
		while not exit:
			screen.beginFrame((0,0,63.0/256.0,0))
			UIState.begin(screen.getScreen(),pygame.mouse.get_pos(),pygame.mouse.get_pressed())
			
			with AlignLeft((16,0)):
				Text("theme: %s" % UIState.getTheme())
			
				if Button("change theme"):
					curtheme = (curtheme+1)%len(themes)
					UIState.setTheme(themes[curtheme])
			
				cv = CheckedButton(cv,"check",(100,50))
				bv = CheckBox(bv,"jee",(200,50))
			
			value = ScrollBar(value,0,200,(200,100),(20,100))
			TextBox("%d" % value,(200,204),(30,24),center=True)
			
			TextBox(u"hiiohoi huolta nyt ei merimies käy merta päin",(100,300),(200,100))
			
			with VerticalLayout((300,10),(300,300)):
				Button("jaa")
				Button("jaa")
					
				with HorisontalLayout():
					Button("jaa")
					Button("jaa")
					Button("jaa")
					Button("jaa")
			
				with HorisontalLayout():
					Button("joo")
					Button("joo")
					Button("joo")
					Button("joo")
				text,done = EditText(text,None,(None,20),max_length=32)
					
			if done:
				print "done"
			
			Text("icons",(20,450))
			x = 10
			y = 470
			theme = UIState.getTheme()
			for i in range(Icons.MAX):
				theme.drawIcon(i,(x,y),(16,16))
				x+=20
			exit = pygame.key.get_pressed()[K_ESCAPE]
			UIState.end()
			screen.endFrame()
			
	except KeyboardInterrupt:
		pass
		

if __name__ == '__main__':
	main()