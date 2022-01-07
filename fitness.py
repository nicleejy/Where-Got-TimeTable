from helperfunctions import days, actual_days, dprint, range_overlapping


# Check for bounds being exceeded in the overall timetable, returns the reciprocal of the number of bounds exceptions
def check_bounds(timetable, start, end):
    exceeded_bounds = 0
    fixed_exceeded_bounds = 0
    for session in timetable:
        if type(session).__name__ == "VarClass":
            if int(session.start) < int(start) or int(session.end) > int(end):
                exceeded_bounds += 1
        else:
            if int(session.start) < int(start) or int(session.end) > int(end):
                fixed_exceeded_bounds += 1

    # print("Bounds exceeded containing variable classes: " + str(exceeded_bounds))
    # print("Bounds exceeded containing fixed classes: " + str(fixed_exceeded_bounds))
    return 1 / (exceeded_bounds + 1)


# Check for free days being conflicted in the overall timetable, returns the reciprocal of the number of conflicts
def check_free_days(timetable, day_arr):
    week_days = [days[day] for day in day_arr]
    free_day_conflicts = 0
    fixed_free_day_conflicts = 0
    for session in timetable:
        for week_day in week_days:
            if type(session).__name__ == "VarClass":
                if session.day == week_day:
                    free_day_conflicts += 1
            else:
                if session.day == week_day:
                    fixed_free_day_conflicts += 1

    # print("Free day conflicts containing variable classes: " + str(free_day_conflicts))
    # print("Free day conflicts containing fixed classes: " + str(fixed_free_day_conflicts))
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


#Checks for lunchtime conflict in the overall timetable
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

