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