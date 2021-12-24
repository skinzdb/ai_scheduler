import demographic
import comedian

#This class is used to create the timetable object that you will assign a schedule to
#Importantly, it creates a dictionary of dictionaries. Each day of the week is its own dictionary, which can have a key value pair assigned to it.
#The key will be the slot number, and the value a list of objects that represent the comedian, demographic and show_type in that order.
#Comedian will be a comedian object, demographic will be a demographic object and show_type is a string that should be either 'main' or 'test'
class Timetable:

	def __init__(self, taskNumber):
		self.schedule = {"Monday" : {}, "Tuesday" : {}, "Wednesday" : {}, "Thursday" : {}, "Friday" : {}}
		self.cost = 0
		self.taskNumber = taskNumber


	#This method is used by other classes, and should not be used by you
	def getSession(self, day, timeslot):
		if day not in self.schedule:
			raise ValueError("Day can only be Monday, Tuesday, Wednesday, Thursday or Friday")
		else:
			if timeslot in self.schedule[day]:
				return self.schedule[day][timeslot]
			else:
				raise ValueError("timeslot not yet assigned")

	#This method is used by other classes, and should not be used by you
	def sessionAssigned(self,day,timeslot):
		if day not in self.schedule:
			raise ValueError("Day can only be Monday, Tuesday, Wednesday, Thursday or Friday")
		else:
			if timeslot in self.schedule[day]:
				return True
			else:
				return False

	#This method will take all the information needed to assign a comedian and a demographic to a particular show slot.
	#day should be one of the days of the working week, as defined in the schedule dictionary above
	#timeslot should be a number between and including 1-5 or 1-10 based on the task being attempted.
	#comedian should be a comedian object
	#demographic should be a demographic object
	#show_type should be either 'main' or 'test'
	def addSession(self, day, timeslot, comedian, demographic, show_type):
		if day not in self.schedule:
			raise ValueError("Day can only be Monday, Tuesday, Wednesday, Thursday or Friday")
		elif self.taskNumber == 1:
			if timeslot == 0 or timeslot > 5:
				raise ValueError("timeslot can only be: 1, 2, 3, 4 or 5")
			else:
				self.schedule[day][timeslot] = [comedian, demographic, "main"]
		else:
			if timeslot == 0 or timeslot > 10:
				raise ValueError("timeslot can only be: 1, 2, 3, 4, 5, 6, 7, 8, 9 or 10")
			elif show_type != "main" and show_type != "test":
				raise ValueError("show_type must be either: main or test")
			else:
				self.schedule[day][timeslot] = [comedian, demographic, show_type]

	#This method calls the correct checker based on the task
	def scheduleChecker(self, comedian_List, demographic_List):

		if self.taskNumber == 1:
			return self.task1Checker(comedian_List, demographic_List)
		else:
			return self.task23Checker(comedian_List, demographic_List)

	#Small utility method to check if a comedian can market a show to a demographic
	def canMarket(self, comedian, demographic, isTest):
		#if it is not a test show, we make sure every one of the demographics' topics is matched by the comedian's themes.
		if not isTest:
			topics = demographic.topics

			i = 0
			for t in topics:
				if t not in comedian.themes:
					print(str(comedian.name) + " cannot be marketed to demographic " + str(demographic.reference))
					return False

			return True

		#if it is a test show, we make sure the comedian has at least one theme that matches a topic of the demographic.
		else:
			topics = demographic.topics

			i = 0
			for t in topics:
				if t in comedian.themes:
					return True

			print(str(comedian.name) + " cannot be marketed to demographic " + str(demographic.reference))
			return False

	#A checker to make sure your Task 1 schedule is legal.
	def task1Checker(self, comedian_List, demographic_List):
		comedian_Count = dict()
		demographic_Assigned = list()

		#We make sure to check that every day has all its timeslots assigned
		for day in self.schedule:
			day_List = self.schedule[day]
			if len(day_List) != 5:
				print(str(day) + " does not have every slot assigned.")
				return False
			comedians_Today = list()

			#We then check the validty of each entry
			for entry in self.schedule[day]:
				[comedian, demographic, show_type] = day_List[entry]

				#Make sure that every demographic is only marketed to once a week
				if demographic.reference in demographic_Assigned:
					print(str(demographic.reference) + " is being marketed to more than once a week.")
					return False
				else:
					demographic_Assigned.append(demographic.reference)

				#We make sure every comedian is only a single show a day
				if comedian.name in comedians_Today:
					print(str(comedian.name) + " is hosting multiple shows on " + str(day))
					return False
				else:
					comedians_Today.append(comedian.name)

				#This makes sure a comedian is in a maximum of two shows a week.
				if comedian.name in comedian_Count:
					show_Count = comedian_Count[comedian.name]
					comedian_Count[comedian.name] = comedian_Count[comedian.name] + 1
					if show_Count == 2:
						print(str(comedian.name) + " is in more than two shows a week.")
						return False
				else:
					comedian_Count[comedian.name] = 1

				#Finally, we make sure that the comedian in each show can be marketed to the assigned demographic
				if not self.canMarket(comedian, demographic, False):
					print(str(comedian.name) + " can not be marketed to demographic " + str(demographic.reference) + ", their themes do not match the topics.")
					return False

		return True


	#This checks the validity of a solution to Tasks 2 and 3, and also calculates the cost.
	def task23Checker(self, comedian_List, demographics_List):

		comedian_Count = dict()
		main_demographics_Assigned = list()
		test_demographics_Assigned = list()
		schedule_Cost = 0
		comedians_Yesterday = list()
		main_show_Count = dict()
		test_show_Count = dict()

		for comedian in comedian_List:
			main_show_Count[comedian.name] = 0
			test_show_Count[comedian.name] = 0
			comedian_Count[comedian.name] = 0


		for day in self.schedule:
			day_List = self.schedule[day]

			#Again, we check each day has all of its slots assigned
			if len(day_List) != 10:
				print(str(day) + " does not have every slot assigned.")
				return False

			comedians_Today = dict()
			possible_Discount = dict()

			#process the validity of each entry
			for entry in self.schedule[day]:
				[comedian, demographic, show_type] = day_List[entry]

				#We check that each demographic has only a single entry for both main and test shows
				if show_type == "main":
					if demographic.reference in main_demographics_Assigned:
						print(str(demographic.reference) + " is being marketed more than one main show a week.")
						return False
					else:
						main_demographics_Assigned.append(demographic.reference)

				elif show_type == "test":
					if demographic.reference in test_demographics_Assigned:
						print(str(demographic.reference) + " is being marketed more than one test show a week.")
						return False
					else:
						test_demographics_Assigned.append(demographic.reference)

				#We make sure that an illegal session type hasn't been entered somehow
				else:
					print(str(show_type) + " is not 'main' or 'test'.")
					return False

				#We now go through every comedian to make sure they are not on stage for too long in a week
				if comedian.name in comedians_Today:
					#This branch means the comedian is already on stage today.
					if comedians_Today[comedian.name] >= 2:
						print(str(comedian.name) + " is already on stage for two hours on " + str(day))
						return False
					else:
						#We calculate the cost for the show, if it is a main show.
						if show_type == "main":
							comedians_Today[comedian.name] = comedians_Today[comedian.name] + 2
							main_show_Count[comedian.name] = main_show_Count[comedian.name] + 1
							if main_show_Count[comedian.name] == 1:
								schedule_Cost = schedule_Cost + 500
							elif comedian.name in comedians_Yesterday:
								schedule_Cost = schedule_Cost + 100
							else:
								schedule_Cost = schedule_Cost + 300
						else:
							#We calculate the cost of a test show
							comedians_Today[comedian.name] = comedians_Today[comedian.name] + 1
							test_show_Count[comedian.name] = test_show_Count[comedian.name] + 1
							initial_test_show_Cost = (300 - (50 * test_show_Count[comedian.name])) / 2
							schedule_Cost = schedule_Cost + initial_test_show_Cost

							if comedian.name in possible_Discount:
								schedule_Cost = schedule_Cost - possible_Discount.pop(comedian.name)
				else:
					#This branch means the comedian has not yet been on stage today
					#We calculate the costs correspondingly
					if show_type == "main":
						comedians_Today[comedian.name] = 2
						main_show_Count[comedian.name] = main_show_Count[comedian.name] + 1
						if main_show_Count[comedian.name] == 1:
							schedule_Cost = schedule_Cost + 500
						elif comedian.name in comedians_Yesterday:
							schedule_Cost = schedule_Cost + 100
						else:
							schedule_Cost = schedule_Cost + 300
					else:
						comedians_Today[comedian.name] = 1

						test_show_Count[comedian.name] = test_show_Count[comedian.name] + 1
						initial_test_show_Cost = (300 - (50 * test_show_Count[comedian.name]))
						schedule_Cost = schedule_Cost + initial_test_show_Cost
						possible_Discount[comedian.name] = initial_test_show_Cost / 2

				#We update the hours the comedian is on stage for the week
				if show_type == "main":
					comedian_Count[comedian.name] = comedian_Count[comedian.name] + 2
				else:
					comedian_Count[comedian.name] = comedian_Count[comedian.name] + 1

				#Make sure a comedian is not on stage for more than four hours a week
				if comedian_Count[comedian.name] > 4:
						print(str(comedian.name) + " is already on stage for 4 hours")
						return False

				#check if the comedian can be marketed to the assigned demographic
				if not self.canMarket(comedian, demographic, show_type=="test"):
					print(str(comedian.name) + " can not be marketed to demographic " + str(demographic.reference) + ", their themes do not match the topics.")
					return False

			#One last check to make sure daily stage hours haven't been exceeded
			for name in comedians_Today:
				if comedians_Today[name] > 2:
					print(str(name) + " is on stage for more than two hours in a day.")
					return False

			comedians_Yesterday = comedians_Today

		#One final check to make sure total hours haven't been exceeded
		for name in comedian_Count:
			if comedian_Count[name] > 4:
				print(str(name) + " is on stage for more than four hours a week")
				return False

		#If we get here, schedule is legal, so we assign the cost and return True
		self.cost = schedule_Cost
		return True
