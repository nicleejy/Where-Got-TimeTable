import datetime
from datetime import date
import math
from collections import namedtuple
from pytz import timezone
import pytz

sg_timezone = pytz.timezone("Asia/Singapore")

def get_sg_time():
    return datetime.datetime.now(sg_timezone)


# Keeps track of windows where users can create a new timetable based on year

relaxed_calendar = {'2021-2022': [date(2021, 5, 2), date(2021, 12, 5)],
                    '2022-2023': [date(2022, 5, 7), date(2022, 12, 4)],
                    '2023-2024': [date(2023, 5, 6), date(2023, 12, 10)],
                    '2024-2025': [date(2024, 5, 11), date(2024, 12, 8)],
                    '2025-2026': [date(2025, 5, 10), date(2025, 12, 8)]}


def get_academic_year():

    if relaxed_calendar["2021-2022"][0] <= get_sg_time().date() < relaxed_calendar["2022-2023"][0]:
        academic_year = '2021-2022'
    elif relaxed_calendar["2022-2023"][0] <= get_sg_time().date() < relaxed_calendar["2023-2024"][0]:
        academic_year = '2022-2023'
    elif relaxed_calendar["2023-2024"][0] <= get_sg_time().date() < relaxed_calendar["2024-2025"][0]:
        academic_year = '2023-2024'
    elif relaxed_calendar["2024-2025"][0] <= get_sg_time().date() < relaxed_calendar["2025-2026"][0]:
        academic_year = '2024-2025'
    else:
        academic_year = '2022-2023' # fallback

    return academic_year


# Dictionaries to convert between days
days = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
actual_days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

# Named tuple objects representing a class timeslot
VarClass = namedtuple("VarClass", ["module", "type", "no", "day", "start", "end"]) #indicates the class slots can be varied for identification
FixedClass = namedtuple("FixedClass", ["module", "type", "no", "day", "start", "end"]) #indicates the class slots must be fixed for indentification

debugging = False  

# Sigmoid functions
def sigmoid(x):
  return 1 / (1 + math.exp(-x))


# Debug print
def dprint(item):
    if debugging:
        print(item)


# Checks for overlapping between x and y
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


# Takes a timetable array and reduces it to a nested dictionary for better parsing
def parse_timetable(timetable_final, module_codes):
    all_classes = {}
    for mod in module_codes:
        mod_classes = {}
        for session in timetable_final:
            if mod == session.module:
                if session.type.upper() == "TUTORIAL TYPE 2":
                    mod_classes["TUT2"] = session.no
                else:
                    mod_classes[(session.type.upper())[0:3]] = session.no
        all_classes[mod] = mod_classes
    return all_classes

# {'MA1521': {'TUT': '3', 'LEC': '1'}, 
# 'CS1101S': {'TUT': '10D', 'LEC': '1', 'REC': '02A'}, 
# 'ACC1701X': {'TUT': 'X15', 'LEC': 'X1'}, 
# 'CS1231S': {'LEC': '1', 'TUT': '19A'}, 
# 'ES2660': {'SEC': 'G09'}, 'IS1103': {}}


# Generates an NUS Mods timetable link from a given timetable
def generate_link(timetable, semester, module_codes):
    parsed_timetable = parse_timetable(table_compressor(timetable), module_codes)
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