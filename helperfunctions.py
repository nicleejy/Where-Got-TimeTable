import math

debugging = False

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def dprint(item):
    if debugging:
        print(item)

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