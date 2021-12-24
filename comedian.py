import demographic

#Class for storing a comedian object, which tracks their name, and themes
#themes are a list of strings
#name is a string

class Comedian:

	def __init__(self,name="", themes=list()):
		self.name=name
		self.themes=themes

	#this is used during set up and should not be used in your solution
	def setName(self,name):
		self.name = name

	#this is used during set up and should not be used in your solution
	def setThemes(self,themes):
		self.themes = themes

	#this is used during set up and should not be used in your solution
	def addTheme(self,theme):
		self.themes.add(theme)

	def __str__(self):
		return str([self.name, self.themes])

	def __repr__(self):
		return str(self)
