from collections import namedtuple
from random import choice
from moduleparser import get_all_module_info, get_module_info
from helperfunctions import *

#input: container
#output: random generated timetable based on available slots in container

def generate_timetable(container):
    selected_classes = []
    for module in container:
        for lesson_types in container[module]:
            available_slots = container[module][lesson_types]
            print(f'\nMODULE: {module}')
            print(f'LESSON TYPE: {lesson_types}')
            print(f'SLOTS: {available_slots}')
            if len(available_slots) == 1:
                if type(available_slots[0][0]) == list:
                    for slot in available_slots[0]:
                        block_1 = [module, lesson_types] + slot
                        print(f'BLOCK 1: {block_1}')
                        fixed_class = FixedClass._make(block_1)
                        selected_classes.append(fixed_class)
                else:
                    block_1 = [module, lesson_types] + available_slots[0]
                    print(f'BLOCK 1: {block_1}')
                    fixed_class = FixedClass._make(block_1)
                    selected_classes.append(fixed_class)            
            else:
                #randomly select a slot
                selected_slot = choice(available_slots)
                set_of_classes = []     
                print(f"Selected slot: {selected_slot}")            
                if len(selected_slot) > 1: #variable lecture/tutorial pairs which must stay paired throughout
                    for lesson in selected_slot:
                        block_2 = [module, lesson_types] + lesson
                        variable_class = VarClass._make(block_2)
                        set_of_classes.append(variable_class)
                    selected_classes.append(set_of_classes)
                else:
                    block_2 = [module, lesson_types] + selected_slot[0] #single variable slot
                    variable_class = VarClass._make(block_2)
                    selected_classes.append(variable_class)
    print("Selected classes:")
    for i in selected_classes:
        print(i)
    print()
    return selected_classes


# slots can be of type:
#  1. [[['1', 3, '1200', '1400'], ['1', 4, '1500', '1600']]] Fixed lecture pairs, has length of 1
#  2. [['1', 0, '1200', '1400']] Single fixed lecture slot, also with length 1
#  3. [['4', 2, '1000', '1100'], ['5', 4, '1100', '1200'], ['7', 1, '1300', '1400']] Different variable tutorial slots
#  4. [[['G21', 0, '1000', '1200'], ['G21', 3, '1000', '1200']], [['G19', 1, '1200', '1400'], ['G19', 4, '1200', '1400']]] Different variable tutorial/lecture pairs
