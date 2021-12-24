import comedian
import demographic
import ReaderWriter
import timetable
import random
import math

class Scheduler:

	def __init__(self,comedian_List, demographic_List):
		self.comedian_List = comedian_List
		self.demographic_List = demographic_List

	#Using the comedian_List and demographic_List, the this class will create a timetable of slots for each of the 5 work days of the week.
	#The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
	#	timetableObj.addSession("Monday", 1, comedian_Obj, demographic_Obj, "main")
	#This line will set the session slot '1' on Monday to a main show with comedian_obj, which is being marketed to demographic_obj.
	#Note here that the comedian and demographic are represented by objects, not strings.
	#The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
	#The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in Task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in Tasks 2 and 3.
	#Comedian (3rd argument) and Demographic (4th argument) can be assigned any value, but if the comedian or demographic are not in the original lists,
	#	your solution will be marked incorrectly.
	#The final, 5th argument, is the show type. For Task 1, all shows should be "main". For Tasks 2 and 3, you should assign either "main" or "test" as the show type.
	#In Tasks 2 and 3, all shows will either be a 'main' show or a 'test' show

	#demographic_List is a list of Demographic objects. A Demographic object, 'd' has the following attributes:
	# d.reference  - the reference code of the demographic
	# d.topics - a list of strings, describing the topics that the demographic like to see in their comedy shows e.g. ["Politics", "Family"]

	#comedian_List is a list of Comedian objects. A Comedian object, 'c', has the following attributes:
	# c.name - the name of the Comedian
	# c.themes - a list of strings, describing the themes that the comedian uses in their comedy shows e.g. ["Politics", "Family"]

	#For Task 1:
	#Keep in mind that a comedian can only have their show marketed to a demographic
	#	if the comedian's themes contain every topic the demographic likes to see in their comedy shows.
	#Furthermore, a comedian can only perform one main show a day, and a maximum of two main shows over the course of the week.
	#There will always be 25 demographics, one for each slot in the week, but the number of comedians will vary.
	#In some problems, demographics will have 2 topics and in others 3 topics.
	#A comedian will have between 3-8 different themes.

	#For Tasks 2 and 3:
	#A comedian can only have their test show marketed to a demographic if the comedian's themes contain at least one topic
	#	that the demographic likes to see in their comedy shows.
	#Comedians can only manage 4 hours of stage time a week, where main shows are 2 hours and test shows are 1 hour.
	#A Comedian cannot be on stage for more than 2 hours a day.

	#You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need.
	#Furthermore, you should not import anything else beyond what has been imported above.
	#To reiterate, the five calls are timetableObj.addSession, d.reference, d.topics, c.name, c.themes

	#This method should return a timetable object with a schedule that is legal according to all constraints of Task 1.
	def createSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(1)

		#Here is where you schedule your timetable

		#This line generates a random timetable, that is unlikely to be valid. You can use this or delete it.
		self.randomMainSchedule(timetableObj)

		#Do not change this line
		return timetableObj

	#Now, for Task 2 we introduce test shows. Each day now has ten sessions, and we want to market one main show and one test show
	#	to each demographic.
	#All slots must be either a main or a test show, and each show requires a comedian and a demographic.
	#A comedian can have their test show marketed to a demographic if the comedian's themes include at least one topic the demographic likes.
	#We are also concerned with stage hours. A comedian can be on stage for a maximum of four hours a week.
	#Main shows are 2 hours long, test shows are 1 hour long.
	#A comedian cannot be on stage for more than 2 hours a day.
	def createTestShowSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(2)

		#Here is where you schedule your timetable

		#This line generates a random timetable, that is unlikely to be valid. You can use this or delete it.
		self.randomMainAndTestSchedule(timetableObj)

		#Do not change this line
		return timetableObj

	#Now, in Task 3 it costs £500 to hire a comedian for a single main show.
	#If we hire a comedian for a second show, it only costs £300. (meaning 2 shows cost £800 compared to £1000)
	#If those two shows are run on consecutive days, the second show only costs £100. (meaning 2 shows cost £600 compared to £1000)

	#It costs £250 to hire a comedian for a test show, and then £50 less for each extra test show (£200, £150 and £100)
	#If a test shows occur on the same day as anything else a comedian is in, then its cost is halved.

	#Using this method, return a timetable object that produces a schedule that is close, or equal, to the optimal solution.
	#You are not expected to always find the optimal solution, but you should be as close as possible.
	#You should consider the lecture material, particular the discussions on heuristics, and how you might develop a heuristic to help you here.
	def createMinCostSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(3)

		#Here is where you schedule your timetable

		#This line generates a random timetable, that is unlikely to be valid. You can use this or delete it.
		self.randomMainAndTestSchedule(timetableObj)

		#Do not change this line
		return timetableObj


	#This simplistic approach merely assigns each demographic and comedian to a random slot, iterating through the timetable.
	def randomMainSchedule(self,timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for demographic in self.demographic_List:
			comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

			timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "main")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 6:
				sessionNumber = 1
				dayNumber = dayNumber + 1

	#This simplistic approach merely assigns each demographic to a random main and test show, with a random comedian, iterating through the timetable.
	def randomMainAndTestSchedule(self,timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for demographic in self.demographic_List:
			comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

			timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "main")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1

		for demographic in self.demographic_List:
			comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

			timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "test")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1
