import demographic
import comedian

#This is a class that is used to read in the requirements from the problem folder and convert
#them into a list of comedians and demographics

class ReaderWriter:

	#This converts a text file into a list of comedians and demographics, so that they can be fit to a schedule
	#Each line in the text file is a comma separated list of attributes
	def readRequirements(self,filename):
		comedian_List = list()
		demographic_List = list()
		with open(filename) as f:
			demographics = False
			for line in f:
				#comedians are listed first, up until the deliminator, '==='
				if "===" in line:
					demographics = True
				else:
					line = line.replace("\n","")
					line = line.split(",")
					#dealing with an comedian, their name is the first element in the list and the rest
					#are the themes of the comedian
					if not demographics:
						themes = list()
						for i in range(1,len(line)):
							themes.append(line[i])
						com = comedian.Comedian(name=line[0], themes=themes)
						comedian_List.append(com)
					else:
						#with demographics, the reference code is the first element of the list, and the topics next
						topics = list()
						for i in range(1,len(line)):
							topics.append(line[i])
						demo = demographic.Demographic(reference=line[0], topics=topics)
						demographic_List.append(demo)

		#returns a list of comedian and demographic objects
		return [comedian_List, demographic_List]

	#This will convert a list of comedian and demographic objects into a text file, so that it can be used later
	def writeRequirements(self,comedian_List, demographic_List, filename):
		#Each comedian object and demographic object is converted into a string of comma separated values
		for c in comedian_List:
			comedian_String = str(c.name)

			for thm in c.themes:
				comedian_String = comedian_String + "," + str(thm)

			with open(filename, "a") as f:
				f.write(comedian_String + "\n")

		with open(filename, "a") as f:
			f.write("===\n")

		for d in demographic_List:
			demographic_String = str(d.reference)

			for top in d.topics:
				demographic_String = demographic_String + "," + str(top)

			with open(filename, "a") as f:
				f.write(demographic_String + "\n")
