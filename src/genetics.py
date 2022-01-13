import random 
from random import choice
from collections import namedtuple
# Mutate a given timetable by choosing timeslots at random for VarClass objects, FixedClass objects are not mutated
# Mutation Frequency: Number of sessions to mutate
# Named tuple objects representing a class timeslot
VarClass = namedtuple("VarClass", ["module", "type", "no", "day", "start", "end"]) #indicates the class slots can be varied for identification
FixedClass = namedtuple("FixedClass", ["module", "type", "no", "day", "start", "end"]) #indicates the class slots must be fixed for indentification


def mutate(container, timetable):
    mutatable = 0
    mutation_frequency = 1
    number_of_classes = len(timetable)
    indexes_to_mutate = []
    generate_random = True

    for lesson in timetable:
        if type(lesson).__name__ == "VarClass":
            mutatable += 1
        elif type(lesson) == list:
            if type(lesson[0]).__name__ == "VarClass":
                mutatable += 1
    if mutatable < mutation_frequency:
        mutation_frequency = mutatable
    
    while generate_random:
        rand_index = random.randint(0, number_of_classes - 1)
        if type(timetable[rand_index]).__name__ == "VarClass":
            if rand_index not in indexes_to_mutate:
                indexes_to_mutate.append(rand_index)
        elif type(timetable[rand_index]) == list:
            if type(timetable[rand_index][0]).__name__ == "VarClass":
                if rand_index not in indexes_to_mutate:
                    indexes_to_mutate.append(rand_index)
        if len(indexes_to_mutate) == mutation_frequency:
            generate_random = False

    for index in indexes_to_mutate:
        current_session = timetable[index]
        # getting module name and class type
        if type(timetable[index]) == list:
            module_name, class_type = current_session[0].module, current_session[0].type
        else:
            module_name, class_type = current_session.module, current_session.type
        
        available_sessions = container[module_name][class_type]
        new_session = choice(available_sessions) 

        if len(new_session) > 1:
            print()
            print()
            print(f"new session 0 {new_session}")
            linked_session = []
            for session in new_session:
                linked_session.append(VarClass._make([module_name, class_type, 
                                                      session[0], session[1], 
                                                      session[2], session[3]]))
            print(f"\nMutating linked pair {timetable[index]} to {linked_session}")
            timetable[index] = linked_session
        else:
            new_class = VarClass._make([module_name, class_type, 
                                        new_session[0][0], new_session[0][1], 
                                        new_session[0][2], new_session[0][3]])
            print(f"\nMutating isolated class {timetable[index]} to {new_class}")
            timetable[index] = new_class
    return timetable

def filter_classes(timetable):
    fixed_classes = [i for i in timetable if type(i).__name__ == "FixedClass"]
    sorted_timetable = sorted([j for j in timetable if type(j).__name__ == "VarClass"], key=lambda row: (row[0], row[1]))
    linked_sessions = [k for k in timetable if type(k) == list]
    sorted_linked_sessions = sorted(linked_sessions, key=lambda x: (x[0][0], x[0][1]))
    for pair in sorted_linked_sessions:
        sorted_timetable.append(pair)
    return fixed_classes, sorted_timetable


# Crossover function which combines 2 parent timetables and outputs 2 child timetables
# Probability that traits are inherited from either parent is 50/50
def single_point_crossover(timetable_1, timetable_2):
    print("Crossing over...")
    fixed_1, var_parent_1 = filter_classes(timetable_1)
    fixed_2, var_parent_2 = filter_classes(timetable_2)
    child_1 = []
    child_2 = []
    for i in range(len(var_parent_1)):
        choice_int = random.randint(0, 1)
        if choice_int == 0:
            # print("Child 1 acquiring Parent 1's traits...")
            # print("Child 2 acquiring Parent 2's traits...")
            child_1.append(var_parent_1[i])
            child_2.append(var_parent_2[i])
        else:
            # print("Child 1 acquiring Parent 2's traits...")
            # print("Child 2 acquiring Parent 1's traits...")
            child_1.append(var_parent_2[i])
            child_2.append(var_parent_1[i])
    child_1.extend(fixed_1)
    child_2.extend(fixed_2)
    return child_1, child_2