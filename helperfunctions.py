import math
from collections import namedtuple

# Dictionaries to convert between days
days = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
actual_days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

# Named tuple objects representing a class timeslot
VarClass = namedtuple("VarClass", ["module", "type", "no", "day", "start", "end"]) #indicates the class slots can be varied for identification
FixedClass = namedtuple("FixedClass", ["module", "type", "no", "day", "start", "end"]) #indicates the class slots must be fixed for indentification


debugging = False

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def dprint(item):
    if debugging:
        print(item)

def range_overlapping(x, y): 
        if x.start == x.stop or y.start == y.stop: 
            return False 
        elif x.start == y.start and x.stop == y.stop: 
            return True 
        return x.start < y.stop and y.start < x.stop

def table_compressor(timetable):  #takes in a list of lists and/or namedtuple and compress it to just a list of namedtuple
    singlelist_timetable = []
    for each in timetable:
        if (type(each) == list):
            for eachpair in each:
                singlelist_timetable.append(eachpair)
        else: 
            singlelist_timetable.append(each)
    sorted_timetable = sorted(singlelist_timetable, key = lambda row: (row[3], int(row[4])))
    return sorted_timetable

    