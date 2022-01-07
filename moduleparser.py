import requests, json

def parser(module_list, acad_year, semester):
    response = requests.get("http://api.nusmods.com/v2/" + acad_year + "/modules/" + 'CS1101S' + ".json")
    data = response.json()

    all_timeslots = data['semesterData'][semester - 1]['timetable']

    for timeslot in (all_timeslots):
        print(timeslot)