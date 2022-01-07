from collections import namedtuple
from helperfunctions import *

# Named tuple objects representing a class timeslot
VarClass = namedtuple("VarClass", ["module", "type", "no", "day", "start", "end"]) #indicates the class slots can be varied for identification
FixedClass = namedtuple("FixedClass", ["module", "type", "no", "day", "start", "end"]) #indicates the class slots must be fixed for indentification

debugging = False


# Check for bounds being exceeded in the overall timetable, returns the reciprocal of the number of bounds exceptions
def check_bounds(timetable, start, end):
    exceeded_bounds = 0
    fixed_exceeded_bounds = 0
    for session in timetable:
        if type(session).__name__ == "VarClass":  #Filters out the variable classes
            if int(session.start) < int(start) or int(session.end) > int(end):  #Checks if start of lesson is before bound or end of lesson is after bound
                exceeded_bounds += 1
        else:
            if int(session.start) < int(start) or int(session.end) > int(end):
                fixed_exceeded_bounds += 1

    # print("Bounds exceeded containing variable classes: " + str(exceeded_bounds))
    # print("Bounds exceeded containing fixed classes: " + str(fixed_exceeded_bounds))
    return 1 / (exceeded_bounds + 1)


# Check for free days being conflicted in the overall timetable, returns the reciprocal of the number of conflicts
def check_free_days(timetable, day_arr):
    week_days = [days[day] for day in day_arr]  #list of index of days in day_arr
    free_day_conflicts = 0
    fixed_free_day_conflicts = 0
    for session in timetable:
        for week_day in week_days:
            if type(session).__name__ == "VarClass":  #Filters out the variable classes
                if session.day == week_day: 
                    free_day_conflicts += 1
            else:
                if session.day == week_day:
                    fixed_free_day_conflicts += 1

    dprint("Free day conflicts containing variable classes: " + str(free_day_conflicts))
    dprint("Free day conflicts containing fixed classes: " + str(fixed_free_day_conflicts))
    return 1 / (free_day_conflicts + 1)


# Checks for time conflict in the overall timetable, returns the reciprocal of the number of conflicts
def check_conflict(timetable):
    days_of_week = []
    for lesson in timetable:
        day_index = lesson.day
        if day_index not in days_of_week:
            days_of_week.append(day_index)

    conflicts = 0
    full_week = []
    for weekday in days_of_week: 
        week_day = []
        for lesson in timetable:
            if lesson.day == weekday:
                week_day.append(lesson)
        full_week.append(week_day)
    count = 0
    for day in full_week:
        dprint("\n" + actual_days[count] + ":")
        count += 1
        if len(day) == 1:
            dprint("No conflict detected")
            pass
        else:
            for i in range(len(day) - 1):
                t1_start = day[i].start
                t1_end = day[i].end
                t2_start = day[i + 1].start
                if int(t1_start) <= int(t2_start) < int(t1_end):
                    conflicts += 1
                    dprint("Conflict detected between: " + str(day[i]) + " and " + str(day[i + 1]))
                else:
                    dprint("No conflict detected")
                    pass
    dprint("\nNumber of conflicts: " + str(conflicts) + "\n")
    for i in timetable:
        dprint(str(i))
    dprint("\n") 
    return 1 / (conflicts + 1)


# Checks for lunchtime conflict in the overall timetable, return the number of conflicts
def check_lunch_break(timetable): 
    lunch_break = range(1200, 1400) 
    week = [] 
    conflicts = 0 

    for session in timetable: 
        if session.day not in week: 
            week.append(session.day)

    grouped_sessions = [] 
    for day in week: 
        each_day = [] 
        for slot in timetable: 
            lesson_start = int(slot.start) 
            lesson_end = int(slot.end) 
            lesson_range = range(lesson_start, lesson_end) 
             
            if day == slot.day: 
                if range_overlapping(lesson_range, lunch_break): 
                    each_day.append(slot) 
        if len(each_day) != 0: 
            grouped_sessions.append(each_day) 
     
    for daily_sessions in grouped_sessions: 
        if len(daily_sessions) > 1: 
            for i in range(len(daily_sessions) - 1): 
                interval = int(daily_sessions[i + 1].start) - int(daily_sessions[i].end) 
                if interval < 100: 
                    conflicts += 1 
                    dprint(f"No break time for {daily_sessions}") 
                    break 
                elif interval >= 100: 
                    dprint(f"Suitable break time from {daily_sessions[i].end} to {daily_sessions[i + 1].start} for {daily_sessions}") 
                    pass
        elif len(daily_sessions) == 1: 
            start_time = int(daily_sessions[0].start) 
            end_time = int(daily_sessions[0].end) 
            if start_time <= 1200 and 1400 - end_time >= 100: 
                dprint(f"Suitable break time from {end_time} to 1400 for {daily_sessions[0]}") 
                pass
            elif end_time >= 1400 and start_time - 1200 >= 100: 
                dprint(f"Suitable break time from 1200 to {start_time} for {daily_sessions[0]}") 
                pass
            else: 
                dprint(f"No break time for {daily_sessions[0]}") 
                conflicts += 1 
    dprint(f"\nLunchtime Conflicts: {conflicts}") 
    return conflicts  #returns the reciprocal of the number of conflicts


# Checks for desired freetime and presence of lunchtime and returns a score 
def soft_constraints(desired_freetime, lunch, sorted_timetable):
    sorted_timetable = table_compressor(sorted_timetable)
    totalhours = 14  #total valid hours in a day
    maxscore = 5  #max score for soft constraints
    penalty= 0.7  #penalty for each conflict

    week_days = []  #list of corresponding days with lessons
    for i in sorted_timetable:  
        if i.day not in week_days:
            week_days.append(i.day)

    classes_byday = []  #list of lists of classes on the same day
    for week_day in week_days:
        classes = []  
        for j in sorted_timetable:
            if week_day == j.day:
                classes.append(j)
        classes_byday.append(classes)

    data = []  
    for same_day in classes_byday:
        no_of_failures = 0  #number of failures
        class_duration = 0  #total duration of classes in the same day 
        no_of_classes = len(same_day)  #number of classes on the same day
        no_of_intervals = no_of_classes - 1  #number of intervals between classes of the same day

        for each_class in same_day:
            individual_duration = int(each_class.end) - int(each_class.start)
            class_duration += individual_duration
        
        totalfreetime = totalhours - (class_duration / 100)  #total free time available in the same day
        idealfreetime = (desired_freetime * no_of_intervals)  #ideal free time available in the same day

        if idealfreetime > totalfreetime:  #if what you want is more than total free time available
            realistic_freetime = math.floor(totalfreetime/ no_of_intervals)  #we readjust and give you a realistic free time
            dprint(f"Sorry but your realistic rest time on {actual_days[same_day[1][3]]} is only {realistic_freetime} hours :(")
        else:
            realistic_freetime = desired_freetime  #else you get what you want

        for i in range(no_of_intervals):  #check for number of intervals that does not minimally have the desired rest time
            if int(same_day[i + 1].start) - int(same_day[i].end) < (realistic_freetime * 100):
                no_of_failures += 1
        
        data_dict = {"totalDuration": int(class_duration/100), 
                     "noClasses": no_of_classes, 
                     "failures": no_of_failures}
        data.append(data_dict)
    
    for each in data:  #penalize for each failure
        maxscore -= (each["failures"] * penalty)

    if lunch:
        lunchtime_conflicts = check_lunch_break(sorted_timetable)
        maxscore -= (lunchtime_conflicts * penalty)

    #print(f"Max score is {maxscore} out of 5")
    return sigmoid(maxscore) * 100  #max score is 99.3 after scaling up


# Combines values from all 3 constraint functions and returns a fitness score
# Parameters are the respective user constraints:
# bound_start = "1000"
# bound_end = "1800"
# free_day_arr = ["Monday", "Tuesday"] (in the event the user selects multiple days)
def fitness_function(bound_start, bound_end, free_day_arr, timetable):
    bounds_weight = 1
    free_days_weight = 1
    conflict_weight = 1
    compressed_timetable = table_compressor(timetable)

    fitness_score = ((check_bounds(compressed_timetable, bound_start, bound_end) * bounds_weight) * 
                    (check_free_days(compressed_timetable, free_day_arr) * free_days_weight) * 
                    (check_conflict(compressed_timetable) * conflict_weight))

    return fitness_score
