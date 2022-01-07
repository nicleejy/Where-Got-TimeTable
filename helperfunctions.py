import math
from collections import namedtuple


# Dictionaries to convert between days
days = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
actual_days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

# Named tuple objects representing a class timeslot
VarClass = namedtuple("VarClass", ["module", "type", "no", "day", "start", "end"]) #indicates the class slots can be varied for identification
FixedClass = namedtuple("FixedClass", ["module", "type", "no", "day", "start", "end"]) #indicates the class slots must be fixed for indentification


debugging = True

# Sigmoid functions
def sigmoid(x):
  return 1 / (1 + math.exp(-x))


# Debug print
def dprint(item):
    if debugging:
        print(item)


# 
def range_overlapping(x, y): 
        if x.start == x.stop or y.start == y.stop: 
            return False 
        elif x.start == y.start and x.stop == y.stop: 
            return True 
        return x.start < y.stop and y.start < x.stop


# Takes in a list of lists and/or namedtuple and compress it to just a list of namedtuple
def table_compressor(timetable):  
    singlelist_timetable = []
    for each in timetable:
        if (type(each) == list):
            for eachpair in each:
                singlelist_timetable.append(eachpair)
        else: 
            singlelist_timetable.append(each)
    sorted_timetable = sorted(singlelist_timetable, key = lambda row: (row[3], int(row[4])))
    return sorted_timetable

# Generates an NUS Mods timetable link from a given timetable
def generate_link(timetable):
    parsed_timetable = parse_timetable(table_compressor(timetable))
    link = "https://nusmods.com/timetable/sem-" + str(semester) + "/share?"
    for mod in parsed_timetable:
        counter = 1
        link += (mod + "=")
        length_session = len(parsed_timetable[mod])
        for class_type in parsed_timetable[mod]:
            link += class_type + ":" + (parsed_timetable[mod][class_type])
            if counter != length_session:
                link += ","
            counter += 1
        link += "&"
    return link[0:len(link) - 1]


def merge_scores(timetable, fitness_func, soft_constraints_func):
    soft_score = soft_constraints_func(timetable) / 100
    hard_score = fitness_func(timetable)
    avg_score = (soft_score + hard_score) / 2
    return avg_score