
from state import UIState

class Layout(object):
	"""docstring for Layout"""
	def __init__(self):
		pass
	
	def doLayout(self,pos,size,**kwargs):
		return (pos,size)
		
	def updateLayout(self,pos,size,**kwargs):
		pass
		
	def __enter__(self):
		pass
	
	def __exit__(self,exc_type,exc_value,traceback):
		pass
		
		

class HorisontalLayout(Layout):
	def __init__(self,pos=None,size=None,**kwargs):
		"""docstring for __init__"""
		super(HorisontalLayout,self).__init__()

		self.pos = pos
		self.size = size
		self.curpos = pos
		self.padding = kwargs.pop("padding",16)
		self.maxsize = (0,0)

	def doLayout(self,pos,size,**kwargs):
		x,y = self.curpos

		if not size or not size[0] or not size[1]:
			_x,_y = self.curpos
			_x -= self.pos[0]
			if size:
				w,h = size
			else:
				w = None
				h = None
				
			size = (w or self.size[0]-_x,self.size[1])

		return ((x,y),size)
		
	def updateLayout(self,pos,size,**kwargs):
		self.curpos = (self.curpos[0]+size[0]+self.padding,self.curpos[1])
		self.maxsize = (max(size[0],self.maxsize[0]),max(size[1],self.maxsize[1]))

		
	def __enter__(self):
		self.pos,self.size = UIState.doLayout(self.pos,self.size)
		self.curpos = self.pos
		UIState.beginLayout(self)

	def __exit__(self,exc_type,exc_value,traceback):
		UIState.endLayout()
#		if self.size:
#			size = self.size
#		else:
		size = (self.curpos[0]-self.pos[0],self.maxsize[1])
			
		UIState.updateLayout(self.pos,size)
		
		
class VerticalLayout(Layout):
	def __init__(self,pos=None,size=None,**kwargs):
		"""docstring for __init__"""
		super(VerticalLayout,self).__init__()
		
		self.pos = pos
		self.size = size
		self.curpos = pos
		self.padding = kwargs.pop("padding",8)
		self.maxsize = (0,0)
		
	def doLayout(self,pos,size,**kwargs):
		x,y = self.curpos
		
		if not size or not size[0] or not size[1]:
			_x,_y = self.curpos
			_y -= self.pos[1]
			if size:
				w,h = size
			else:
				w = None
				h = None
				
			size = (self.size[0],h or self.size[1]-_y)
		
		return ((x,y),size)
		
	def updateLayout(self,pos,size,**kwargs):
		self.curpos = (self.curpos[0],self.curpos[1]+size[1]+self.padding)
		self.maxsize = (max(size[0],self.maxsize[0]),max(size[1],self.maxsize[1]))
		
	def __enter__(self):
		self.pos,self.size = UIState.doLayout(self.pos,self.size)
		self.curpos = self.pos
		UIState.beginLayout(self)
		
	def __exit__(self,exc_type,exc_value,traceback):
		UIState.endLayout()
#		if self.size:
#			size = self.size
#		else:
		size = (self.maxsize[0],self.curpos[1]-self.pos[1])
			
		UIState.updateLayout(self.pos,size)

class GridLayout(Layout):
	def __init__(self,pos=None,gridsize=None,size=None,**kwargs):
		"""docstring for __init__"""
		super(GridLayout,self).__init__()

		self.pos = pos
		self.size = size
		self.gridsize = gridsize
		self.numcells = (0,0)
		self.curgrid = (0,0)
		self.padding = kwargs.pop("padding",4)
		
	def calcGrid(self):
		gx,gy = self.gridsize
		self.numcells=(self.size[0]/gx,self.size[1]/gy)
		self.curgrid = (0,0)

	def doLayout(self,pos,size,**kwargs):
		cx,cy = self.curgrid
		
	
	def updateLayout(self,pos,size,**kwargs):
		cx,cy = self.curgrid
		cx+=1
		if cx > self.gridsize[0]:
			cx = 0
			cy+=1
		
		
	def __enter__(self):
		self.pos,self.size = UIState.doLayout(self.pos,self.size)
		self.calcGrid()
		UIState.beginLayout(self)

	def __exit__(self,exc_type,exc_value,traceback):
		UIState.endLayout()

class AlignLeft(Layout):
	def __init__(self,pos=None,size=None,**kwargs):
		self.pos = pos or (0,0)
		self.size = size
		self.padding = kwargs.pop("padding",8)
		self.maxsize = (0,0)
		
	def doLayout(self,pos,size,**kwargs):
		pos = self.curpos
		if not size or not size[0] or not size[1]:
			_x,_y = self.curpos
			_y -= self.pos[1]
			if size:
				w,h = size
			else:
				w = None
				h = None
				
			size = (w or self.size[0]-_x,h or self.size[1]-_y)
		return (pos,size)
		
	def updateLayout(self,pos,size,**kwargs):
		self.curpos = (self.curpos[0],self.curpos[1]+size[1]+self.padding)
		self.maxsize = (max(size[0],self.maxsize[0]),max(size[1],self.maxsize[1]))
		
	def __enter__(self):
		self.pos,self.size = UIState.doLayout(self.pos,self.size)
		self.pos = self.pos or (0,0)
		if not self.size:
			w,h = UIState.getScreenSize()
			self.size = (w-self.pos[0],h-self.pos[1])
			
		self.curpos = self.pos
		
		UIState.beginLayout(self)

	def __exit__(self,exc_type,exc_value,traceback):
		UIState.endLayout()
		size = (self.maxsize[0],self.curpos[1]-self.pos[1])
		UIState.updateLayout(self.pos,size)
		
