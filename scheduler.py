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

	# TASK 1:
	# Firstly, a dictionary called `domain` (hashset) is made to map every demographic to a valid list of comedians.
	# A second dictionary called `bookings` maps comedians to a list of days they have booked. This is used to quickly track constraints.
	# Maintain a list of assignments: `assigned`
	# A recursive backtracking function is utilised to create a valid timetable: 
	# 1) We look at every possible (comedian, demographic) pair, not considering any that violate the (< 2 shows per day constraint).
	# 2) Choose the very next session and sort list of pairs to get MRV.
	# 3) Iterate through the sorted list. In each iteration: 
	# - we assign a (comedian, demographic) pair to the chosen session.
	# - prune (from `domain`) the demographic, and any occurences of the comedian if they now have 2 shows. Create a copy() of `domain` called `oldDomain` before doing this.
	# - recursivley call the backtracking algorithm with this new assignment and domain.
	# - if the backtracking call fails (i.e. returns None) then re-assign `domain = oldDomain.copy()`
	# 4) If all iterations return None, then there is no solution.
	# 5) Otherwise, once the length of `assigned` == 25, return assigned list
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``
	# We try to pick a (comedian, demographic) pair, where the demographic has the least possible valid comedians remaining. 
	# This is our MRV, because we can instantly backtrack if we now pick a demographic that has no possible comedians. It narrows
	# the search tree when we begin searching so we don't have to explore unnecessarily long branches.
	# When choosing the day number and sessions, we always try to assign the very next session chronologically. This is also part of the MRV.
	# Choosing sessions on the same day has more chance of failure, as each session has the < 2 shows per day constraint for a comedian.
	# This yet again reduces the list of possible comedians.
	# Lastly, the domain is made more 'consistent' after each successful assignment. We can remove demographics that have already been assigned, because
	# we can't assign the same demographic twice. We can also remove comedians that have been given > 1 show, because no comedian can have 3 shows.
	# This reduces the size of the domain, which reduces the amount of backtracking calls, i.e., reduces branching factor of search tree => speeds up search.
	def createSchedule(self):
		timetableObj = timetable.Timetable(1)

		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

		# Create hashset of demographics that each point to a list of compatible comedians
		# This reduces the size of our domain, and makes it consistent
		domain = {}
		for d in self.demographic_List:
			domain[d] = []
			for c in self.comedian_List:
				if set(d.topics).issubset(set(c.themes)): 	# Every demographic topic needs to be a comedian theme
					domain[d].append(c)

		# Hashset that has comedians as the keys. Used to keep track on constraints.
		# Each comedian points to a list of days they perform
		bookings = {}	
		for c in self.comedian_List:
			bookings[c] = []

		# Call recursive backtracking algorithm
		assigned = self.backtrack([], bookings, domain)
		for dayNo, sessionNo, comedian, demographic in assigned:
			timetableObj.addSession(days[dayNo], sessionNo, comedian, demographic, "main")

		return timetableObj

	def backtrack(self, assigned, bookings, domain):
		index = len(assigned)	# Select unassigned variable (The next session in time)
		if index == 25:	# Assignment complete => return
			return assigned
		dayNo = index // 5	
		sessionNo = index % 5 + 1

		valid = []	# List of valid assignments
		for demographic in domain.keys():
			for comedian in domain[demographic]:
				# Check domain values are consistent with the constraints
				if len(bookings[comedian]) == 0 or bookings[comedian][0] != dayNo:
					valid.append((comedian, demographic))
			
		# Sort valid list in increasing order of available comedians per demographic
		# We want to assign demographics that have the least possible valid comedians first (MRV) 
		sortedValid = sorted(valid, key=lambda x: len(domain[x[1]]))

		for comedian, demographic in sortedValid: # Now get the least constraining chungus first 
			assigned.append((dayNo, sessionNo, comedian, demographic)) # Add session to assignments

			bookings[comedian].append(dayNo)
			
			oldDomain = domain.copy()
			if len(bookings[comedian]) == 2: # If comedian has used up all their allotted slots, remove any occurrence of them from the domain
				for k in domain.keys():
					try:
						domain[k].remove(comedian)
					except ValueError: pass	# comedian already removed, don't care
			domain.pop(demographic, None) # Remove this demographic, don't need to consider again as it can't be assigned twice

			result = self.backtrack(assigned, bookings, domain)

			if result != None:
				return result

			assigned.pop()	# Remove session from assigned
			bookings[comedian].pop()
			domain = oldDomain.copy()
		return None	# Failure		

	# TASK 2
	# Firstly, a dictionary called `possible` (hashset) maps (demographic, showType) pairs to a list of eligible comedians.
	# A second dictionary called `bookings` maps comedians to an integer list of length = 5. Each element tracks the number of hours the comedian has performed per day.
	# - `sum(bookings[<comedian>]) <= 4` checks comedian has performed less than 4 hours.
	# - `max(bookings[<comedian>]) < 2` checks comedian doesn't have a day where they perform for more than 2 hours.
	# Stochastic local search, specifically simulated annealing, is used to find a consistent timetable:
	# 1) Create a random assignment of comedians to a main and test timetable (the comedians are valid for each show, but may not have valid hour constraints)
	# 2) While there are still conflicts (code inside `getValidAssignments()`):
	# - choose a random variable `var` that is involved in conflicts
	# - 25% chance of:
	# -- swap two variables if they're overbooked on their respective days
	# - 75% chance of:
	# -- choose a random new comedian for `var`
	# -- if it results in less conflicts: assign them
	# -- otherwise, assign them based on probability caclulated using temperature value `temp`
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# The heuristic = number of conflicted variables found in the assignment.
	# The temperature is linearly decreased, therefore the algorithm will have less chance of taking `worsening` steps when we get closer to a solution.
	# Stochastic local search is more sophisticated than simple backtracking, because backtracking can get stuck down very long branches of a
	# search tree where there are no solutions. A combination of randomness and swapping two variables if they're both overbooked can find solutions much faster.
	# The variables are stored in the `assigned` list. `assigned` contains sessions in time order:
	# - day number = assigned_i // 10
	# - session number = assigned_i % 10 + 1
	# The values (each element of `assigned`) are a tuple with the following structure: (comedian, demographic, showType)
	def createTestShowSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(2)

		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

		# Same as Task 1 `domain`, but includes valid comedians for test shows
		possible = self.getPossible()

		# Hashset that has comedians as the keys. Used to keep track on constraints.
		# Every comedian points to a list (already initialised with 5 elements, each element = no. of hours performed per day)
		bookings = {}
		for c in self.comedian_List:
			bookings[c] = [0] * 5

		counter = 0
		for comedian, demographic, showType in self.getValidAssignments(possible, bookings):
			timetableObj.addSession(days[counter // 10], counter % 10 + 1, comedian, demographic, showType)
			counter += 1

		return timetableObj

	# TASK 3
	# Firstly, calls TASK 2 to get a valid assignment.
	# Then uses stochastic local search (simulated annealing again) over a fixed amount of iterations to reduce costs:
	# 1) While the algorithm hasn't reached N=20000 iterations 
	# - 90% chance:
	# -- Pick a random variable and assign it a random valid comedian if schedule is still consistent
	# -- If new cost > old cost, adopt based on probability calculated using temperature
	# - 10% chance:
	# -- Pick two random variables and swap them in the timetable (only if schedule is still consistent)
	# -- '' 		''				''			''			''			''			  ''
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Temperature = initial_temp / (iterations + 1). This is called fast annealing, a popular aprroach for calculating temperature.
	# The temperature will look like a 1/x curve, rapidly decreasing as it gets closer to a solution. Again, this prevents any `worsening` steps when we 
	# are exploring low cost timetables. We have higher chance of random steps at the start to ensure we fit into a good `valley` of assignments, and so the algorithm doesn't plateau on local minima.
	# More iterations => lower cost in general. The algorithm has more chances to make improvements. However this reduces speed, so a compromise was made around 20000.
	# Heuristic = cost function. Never pick an assignment that makes the schedule inconsistent; sometimes pick a schedule that has worse cost (based on temperature).
	# The reason why there is 10% chance to swap variables, is because a certain assignment of demographics may never have an optimal assignment of comedians,
	# so some shuffling may need to be done.
	def createMinCostSchedule(self):
		timetableObj = timetable.Timetable(3)

		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

		possible = self.getPossible()

		bookings = {}
		for c in self.comedian_List:
			bookings[c] = [0] * 5

		assigned = self.getValidAssignments(possible, bookings)

		iterations = 0
		MAX_ITERATIONS = 20000  # max times we can try to lower cost
		INIT_TEMP = 10
		temp = INIT_TEMP
		cost = self.calcCost(assigned, bookings)
		while iterations < MAX_ITERATIONS:
			index = random.randint(0, 49)
			var = assigned[index]

			comedian, demographic, showType = var

			if random.uniform(0, 1) <= 0.9:	# 90% chance to give a randomly select var a random valid comedian
				newComedian = random.choice(possible[(demographic, showType)])
				self.assignVariable(index, (newComedian, demographic, showType), assigned, bookings)
				newCost = self.calcCost(assigned, bookings)
				if ((not self.isConsistent(assigned, bookings)) # If not consistent or costlier and not adopted
						or newCost > cost and math.exp((-(newCost - cost) / 10.0) / temp) <= random.uniform(0, 1)):
					self.assignVariable(index, var, assigned, bookings)
				else:
					cost = newCost
			else:	# 10% chance swap two randomly chosen variables
				otherIndex = random.randint(0, 49)
				otherVar = assigned[otherIndex]
				self.assignVariable(otherIndex, var, assigned, bookings)
				self.assignVariable(index, otherVar, assigned, bookings)
				newCost = self.calcCost(assigned, bookings)
				if ((not self.isConsistent(assigned, bookings)) or # If not consistent or costlier and not adopted
						(newCost > cost and math.exp((-(newCost - cost) / 10.0) / temp) <= random.uniform(0, 1))):
					self.assignVariable(index, var, assigned, bookings)
					self.assignVariable(otherIndex, otherVar, assigned, bookings)
				else:
					cost = newCost

			temp = INIT_TEMP / (iterations + 1)	# Fast annealing
			iterations += 1
	
		counter = 0
		for comedian, demographic, showType in assigned:
			timetableObj.addSession(days[counter // 10], counter % 10 + 1, comedian, demographic, showType)
			counter += 1

		#Do not change this line
		return timetableObj

	# Returns a valid list of assignments for main and test shows
	def getValidAssignments(self, possible, bookings):
		# Assign all slots with random demographics and comedians (demographics will be given a valid comedian, but constraints involving hours performed are not checked)
		assigned = self.randomMainAndTestSchedule(possible, bookings) 

		INIT_TEMP = 1.0
		temp = INIT_TEMP # Temperature parameter
		iterations = 0
		while not self.isConsistent(assigned, bookings):  # Keep searching until we find a valid solution
			conflicted = self.getConflictedVars(assigned, bookings)
			
			var = random.choice(conflicted) 			  # Choose a random variable that is involved in a conflict
			index = assigned.index(var)					
			
			temp -= 0.0001

			dayNo = index // 10
			comedian, demographic, showType = var	# Unpack var tuple
			hours = 2 if showType == "main" else 1	# Get how long show lasts

			if random.uniform(0, 1) <= 0.25:
				if bookings[comedian][dayNo] > 2:	# If comedian is overbooked on this day
					for i in range(50):				
						otherDay = i // 10
						if otherDay != dayNo:		# Find a different comedian from a different day
							otherHours = (2 if assigned[i][2] == "main" else 1) 	
							if (bookings[comedian][otherDay] + hours <= 2 and	# Check that swapping the slots will remove their <=2 hour constraints
									bookings[assigned[i][0]][dayNo] + otherHours <= 2):
								# Swap the assigned variables
								tmp = assigned[i]
								self.assignVariable(i, var, assigned, bookings)
								self.assignVariable(index, tmp, assigned, bookings)
								break
			else: 
				newComedian = random.choice(possible[(demographic, showType)])  # Randomly choose new comedian that can perform for the (demographic, showType)
				newVar = (newComedian, demographic, showType)			  

				oldh = len(conflicted)		  								  # Calculate heuristic of assignments BEFORE adding newComedian
				self.assignVariable(index, newVar, assigned, bookings)	  	  # Assign new variable
				newh = len(self.getConflictedVars(assigned, bookings))		  # Calculate heuristic of assignments AFTER adding newComedian

				if newh >= oldh:	# If new heuristic is worse (i.e. is larger because of more conflicts)
					prob = math.exp((newh - oldh) / max(temp, 0.01))	# Calculate probability that this assignment gets adopted
					u = random.uniform(0, 1)
					if u > prob: # Assignment doesn't get adopted, so undo change
						self.assignVariable(index, var, assigned, bookings)

			iterations += 1
		return assigned

	# Calculates the cost of an assignment
	def calcCost(self, assigned, bookings):
		cost = 0
		comedianShowCount = {}
		possibleDiscount = {}
		sessionNo = 0

		for comedian, _, showType in assigned:
			dayNo = sessionNo // 10
			comedianShowCount[(comedian, showType)] = comedianShowCount.get((comedian, showType), 0) + 1
			if showType == "main":
				if comedianShowCount[(comedian, showType)] == 1:
					cost += 500
				elif dayNo != 0 and bookings[comedian][dayNo - 1] > 0:
					cost += 100
				else:
					cost += 300
			else:
				#We calculate the cost of a test show
				initialTestCost = (300 - (50 * comedianShowCount[(comedian, showType)]))
				
				if (comedian, dayNo) in possibleDiscount:
					cost += initialTestCost / 2 - possibleDiscount.pop((comedian, dayNo))
				else:
					possibleDiscount[(comedian, dayNo)] = initialTestCost / 2
					cost += initialTestCost
			sessionNo += 1

		return cost
	
	# Returns hashset that maps (demographic, showType) pairs to a list of eligible comedians
	def getPossible(self):
		possible = {}
		for d in self.demographic_List:
			possible[(d, "main")] = []
			possible[(d, "test")] = []
			for c in self.comedian_List:
				validNo = 0
				for topic in d.topics:
					if topic in c.themes:
						validNo += 1
				if validNo > 0:	# At least one topic matches => can do test show
					possible[(d, "test")].append(c)
					if validNo == len(d.topics):	# All topics match => can do main show
						possible[(d, "main")].append(c)
		return possible

	# Checks that all assigned variables do not break constraints
	def isConsistent(self, assigned, bookings):
		for comedian, _, _ in assigned:
			if sum(bookings[comedian]) > 4 or max(bookings[comedian]) > 2:
				return False
		
		return True

	# Gets every variable that contributes to a conflict, returns a list of these variables
	def getConflictedVars(self, assigned, bookings):	
		conflicted = []
		for comedian, demographic, showType in assigned:
			if sum(bookings[comedian]) > 4 or max(bookings[comedian]) > 2:
				conflicted.append((comedian, demographic, showType))

		return conflicted

	# Assign a variable, this includes keeping record of the comedian's hours
	def assignVariable(self, index, assignment, assigned, bookings):
		day = index // 10
		oldComedian, _, oldShowType = assigned[index]
		newComedian, _, newShowType = assignment

		bookings[oldComedian][day] -= (2 if oldShowType == "main" else 1)
		assigned[index] = assignment
		bookings[newComedian][day] += (2 if newShowType == "main" else 1)

	# Create a random main and test timetable that assigns comedians to valid shows (doesn't check any other constraints)
	def randomMainAndTestSchedule(self, possible, bookings):
		assigned = []
		index = 0

		variables = list(possible.keys())
		random.shuffle(variables)

		for demographic, showType in variables:
			comedian = random.choice(possible[(demographic, showType)])
			hours = hours = (2 if showType == "main" else 1)
			bookings[comedian][index // 10] += hours
			assigned.append((comedian, demographic, showType))

			index += 1
			
		return assigned
		
