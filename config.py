
import ConfigParser
import types

parser = None

def config_init(filenames):
	global parser
	parser = ConfigParser.SafeConfigParser()
	parser.read(filenames)

def get_section(name):
	global parser
	return ConfigSection(parser,name)

def config_save(filename):
	global parser
	fp = open(filename,"w")
	parser.write(fp)
	fp.close()

class Types:
	Int = 0
	RGB = 1
	String = 2
	Float = 3
	Font = 4

class ConfigType(object):
	def __init__(self,t,default):
		self.type = t
		self.value = default
		
	def convert(self):
		pass
		
	def __str__(self):
		return str(self.value)
		
	def __call__(self):
		return self.convert()

class ConfigInt(ConfigType):
	
	def __init__(self,default):
		super(ConfigInt,self).__init__(Types.Int,default)
		
	def convert(self):
		return int(self.value)

class ConfigString(ConfigType):

	def __init__(self,default):
		super(ConfigString,self).__init__(Types.String,default)

	def convert(self):
		return str(self.value)


class ConfigFloat(ConfigType):

	def __init__(self,default):
		super(ConfigFloat,self).__init__(Types.Float,default)

	def convert(self):
		return float(self.value)

class ConfigRGB(ConfigType):

	def __init__(self,default):
		super(ConfigRGB,self).__init__(Types.RGB,default)

	def __str__(self):
		return "%d,%d,%d" % (self.value[0],self.value[1],self.value[2])
		
	def convert(self):
		l = self.value.split(',')
		return (int(l[0]),int(l[1]),int(l[2]))


class ConfigFont(ConfigType):

	def __init__(self,default,size):
		super(ConfigFont,self).__init__(Types.Font,default)
		self.name = default
		self.size = size
		self.font = None
		
	def __str__(self):
		return "%s,%d" % (self.name,self.size)
		
	def convert(self):
		if not self.font:
			l = self.value.split(',')
			self.name = l[0]
			self.size = int(l[1])
			self.font = pygame.font.SysFont(self.name,self.size)
		
		return self.font
	
class ConfigSection(object):
	def __init__(self,parser,name):
		self.name = name
		self.parser = parser
		
		
	def loadSectionFromTemplate(self,template):
		section = {}
		
		for k,v in template.items():
			v.value = self.get(k,str(v))
			section[k] = v()
		
		return section
	
	def saveSectionWithTemplate(self,template,values):
		
		for k,v in values.items():
			configvalue = template[k]
			configvalue.value = v
			self.set(k,str(configvalue))
	
	def get(self,k,default=None):
		if not self.parser.has_option(self.name,k):
			self.set(k,default)
			
		return self.parser.get(self.name,k,default)

	def set(self,k,v):
		if not self.parser.has_section(self.name):
			self.parser.add_section(self.name)
		
		self.parser.set(self.name,k,str(v))
