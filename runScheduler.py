import comedian
import demographic
import ReaderWriter
import timetable
import scheduler
import time

choice = int(input("schedule (1), test schedule (2), min cost test schedule (3)"))

totalTime = 0
totalCost = 0
for i in range(1, 251):
	rw = ReaderWriter.ReaderWriter()
	[comedian_List, demographic_List] = rw.readRequirements(f"ExampleProblems/Problem{i}.txt")
	sch = scheduler.Scheduler(comedian_List, demographic_List)
	tt = None
	start = time.perf_counter_ns()	
	#this method will be used to create a schedule that solves task 1
	if choice == 1:
		tt = sch.createSchedule()
	elif choice == 2:
		tt = sch.createTestShowSchedule()
	elif choice == 3:
		tt = sch.createMinCostSchedule()

	finish = time.perf_counter_ns()

	duration = (finish - start) / 1000000.0
	totalTime += duration
	
	print(f"Problem {i}:")
	# for key in tt.schedule.keys():
	# 	print(key)
	# 	for j in tt.schedule[key].keys():
	# 		print (j, tt.schedule[key][j])
	# 	print("\n")

	if tt.scheduleChecker(comedian_List, demographic_List):
		print("Schedule is legal.")

		#For problem 1, the cost will be printed, but will be 0
		#For problem 2, the cost will be printed, but can be ignored.
		print("Schedule has a cost of " + str(tt.cost))
		totalCost += tt.cost
	else:
		print("FAILURE")
		break
		
	print(f"ELAPSED: {duration}ms\n")

print(f"TOTAL: {totalTime}ms")
print(f"AVG TIME: {totalTime / 250.0}ms")
print(f"AVG COST: {totalCost / 250.0}")
