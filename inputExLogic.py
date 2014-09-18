#Logic file for fit.py's InputExerciseWindow
import datetime
import copy
import tkinter as tk

#Make dict for the 
def delete_unnecessary_parts(s):
    """
    Deletes all the unneccessary parts of a string.
    """
    list_of_strings = s.split('\n')
    
    values_to_be_deleted = ('', '--------------------','       ')
    for string in list_of_strings:
        if string in values_to_be_deleted:
            list_of_strings.remove(string)
    return list_of_strings

def put_in_separate_lists(s):
    """
    Takes a string and puts them in a list of lists while deleting unnecessary data and
    where each list is an individual group of exercises. 
    """
    
    list_of_strings = delete_unnecessary_parts(s)
    string_list = [[] for x in range(0, int(len(list_of_strings) /2 ))]
    for string_list_index in range(0,len(string_list)):
        for i in range(0,2):
            string_list[string_list_index].append(list_of_strings.pop(0))
    return string_list
def delete_extra_words(list_of_lists):
    """
    Takes a structure of separated lists and removes the words:
    Exercise, Sets, Reps, and Weight
    """
    lol_copy = copy.copy(list_of_lists)
    data_list = []
    extra_words = ('Sets:','Reps:', 'Weight:','')
    for string in lol_copy:
        data_list.append(string[1].split(' '))
    for outer_list in data_list:
        for inner_list_item in outer_list:
            
            if inner_list_item in extra_words:
                outer_list.remove(inner_list_item)
    for outer_list_index in range( len(lol_copy)):
        list_of_lists[outer_list_index][1] = data_list[outer_list_index]
    return lol_copy
    
            
        
    
    
def make_dict(s):
    """
    Makes a data dict out of  a DisplayArea.get() for use with
    sqlite3 data entry.
    """
    
    string_list = put_in_separate_lists(s)
    
    string_lists = delete_extra_words(string_list)
    #Loop to Delete the word "Exercise" from the first strings
    for j in range( len(string_lists)):
        string_lists[j][0] = string_lists[j][0][10:]
    
    
    
    final_string_dict = {}
    for k in string_lists:
        if k[0] in final_string_dict:
                final_string_dict[k[0]] += [k[1]]
        else:
            final_string_dict[k[0]] = [k[1]]
    return final_string_dict
    
        
