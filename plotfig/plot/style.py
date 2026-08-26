
## MODULES
# none

## PARAMETERS
# default marker
default_marker = 'o'
# default markersize
default_markersize = 4

## METHODS
# none

## CLASSES
# handles styling of data series
class Style (object):
	""" contains information about plotting

	Attributes:
	-----------
	None

	Methods:
	--------
	None
	"""

	def __init__ (self, marker = None):
		""" initialize object
		
		Arguments:
		----------
		None

		Returns:
		--------
		Style
			initialized 'Style' object
		"""
		# marker
		self.set_marker(marker)
		# line style
		# hash
		# outer color
		# inner color
		# marker size
		# 

	def update_attributes (self, marker = None, markersize = None):
		""" updates object attributes which are non-None type.

		Arguments:
		----------
		marker : str
		markersize : int

		Returns:
		--------
		None
		"""
		if marker is not None: self.set_marker(marker)
		if markersize is not None: self.set_markersize(markersize)

	## MARKERS ## 
	# TODO :: check against accepted markers in matplotlib

	def reset_marker(self):
		""" reset marker assigned to object.

		Arguments:
		----------
		None

		Returns:
		--------
		None
		"""
		self.marker = None

	def set_marker (self, marker):
		""" assign marker to style.

		Arguments:
		----------
		marker : str or None
			marker type assigned to object

		Returns:
		--------
		None
		"""
		self.marker = marker

	def get_marker (self):
		""" returns marker assigned to style.

		Arguments:
		----------
		None

		Returns:
		--------
		str
			marker assigned to Style
		"""
		if self.marker is None:
			return default_marker
		else:
			return self.marker

	## MARKERSIZE ## 

	def reset_markersize (self):
		""" assign default markersize to object.

		Arguments:
		----------
		None

		Returns:
		--------
		None
		"""
		self.markersize = None

	def set_markersize (self, markersize = None):
		""" assign marker size to object.

		Arguments:
		----------
		markersize : int
			integer greater than zero

		Returns:
		--------
		None
		"""
		# TODO catch unaccepted types
		self.markersize = markersize

	def get_markersize (self):
		""" return markersize assigned to object.

		Arguments:
		----------
		None

		Returns:
		--------
		None
		"""
		if self.markersize is None:
			return default_markersize
		else:
			return self.markersize


## ARGUMENTS
# none

## SCRIPT
# none