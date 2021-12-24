#Simple class representing a demographic, which includes the reference code, and the list of topics
#topics is a list of strings
#reference is a string

class Demographic:
	def __init__(self,reference="", topics=list()):
		self.reference = reference
		self.topics = topics

	#this is used during set up and should not be used in your solution
	def setReference(self,name):
		self.reference = reference

	#this is used during set up and should not be used in your solution
	def setTopics(self,topics):
		self.topics = topics

	#this is used during set up and should not be used in your solution
	def addTopic(self,topic):
		self.topics.append(topic)

	def __str__(self):
		return str([self.reference, self.topics])

	def __repr__(self):
		return str(self)
