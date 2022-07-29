import requests


def day_to_index(day):
    day_dict = {"Monday": 0, "Tuesday": 1, "Wednesday": 2,
                "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
    return day_dict[day]


def get_module_info(module, acad_year, semester):
    response = requests.get("http://api.nusmods.com/v2/" +
                            acad_year + "/modules/" + module + ".json")
    data = response.json()

    if len(data['semesterData']) > 1:
        all_timeslots = data['semesterData'][semester - 1]['timetable']
    elif len(data['semesterData']) == 0:
        all_timeslots = []
    else:
        all_timeslots = data['semesterData'][0]['timetable']
    # handle semester error later

    module_info = {}
    # create a set of class numbers

    lesson_types = set()
    for timeslot in all_timeslots:
        lesson_types.add(timeslot['lessonType'])

    for lesson_type in lesson_types:
        module_info[lesson_type] = []

        class_groups = set()
        for timeslot in all_timeslots:
            if timeslot['lessonType'] == lesson_type:
                class_groups.add(timeslot['classNo'])

        for group in class_groups:
            grouping = []
            for timeslot in all_timeslots:
                if timeslot['classNo'] == group and timeslot['lessonType'] == lesson_type:
                    lesson = [timeslot['classNo'], day_to_index(
                        timeslot['day']), timeslot['startTime'], timeslot['endTime']]
                    grouping.append(lesson)
            module_info[lesson_type].append(grouping)

    return module_info


def get_all_module_info(module_list, acad_year, semester):
    container = {}
    for module in module_list:
        container[module] = get_module_info(module, acad_year, semester)

    print(container)
    return container
