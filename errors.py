
class Error(Exception):
	"""docstring for ParameterError"""
	def __init__(self, arg):
		self.arg = arg
	
	def __str__(self):
		return repr(self.arg)
		
class ParameterError(Error):
	pass
	