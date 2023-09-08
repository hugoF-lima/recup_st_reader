from itertools import count
import json

# from pandas import DataFrame
import pandas as pd

# file_string = "result.json"
# string_test = r"C:\Users\HF_FL\Documents\Python_Scripts\06-Jun_2022\recup_automate\recup_st_030-CDP_serie_10_1-05-21.json"
not_found = False
retrieve = ""

# One angle
cols_use = ["Number_Note", "Mercadoria", "ICMS", "ST"]


def read_json_unused(file_string):
    output_base = []
    with open(file_string) as json_file:
        try:
            data = json.load(json_file)
            retrieve = data  # [nnf]
            output_base = retrieve
            not_found = False
        except KeyError:
            print("No Results found")  # show labor instead
            not_found = True
        return output_base, not_found


# So the query string is here
# Move the ennumerate to the list of items
def list_notes(file_access):
    list_of_notes = []
    with open(file_access) as file_in:
        json_set = json.load(file_in)
        total_notes = len(json_set)
        print("Number of notes:", total_notes)
        for keys_in in json_set:
            list_of_notes.append(keys_in)

        return total_notes, list_of_notes


# notes_in, nnf_numbers = list_notes(string_test)
# print("notes, in: ", nnf_numbers)

""" for key, num in key_index.items():
    print(num) """

""" items_per_note
for count_it, val in enumerate(json_set, start=1):
    grab_total = int(count_it)
    # print(val)
    items_per_note.append(val) """


def fetch_merc_dict(json_string, query_num):
    # place_holder_zero = ["MERC", "ICMS", "ST"]
    items_dict = {}
    items_per_note = []
    with open(json_string) as file_in:
        json_set = json.load(file_in)
        """ total_val = len(json_set)
        print("Number of notes:", total_val) """
        for keys_in in json_set:  # keys_in
            for count_it, val in enumerate(json_set[query_num], start=1):
                grab_total = int(count_it)
                items_per_note.append(val)
            # items_dict[query_num] = items_per_note

        return grab_total, items_per_note


def fetch_merc(json_string: str, query_num: str):
    # place_holder_zero = ["MERC", "ICMS", "ST"]
    items_per_note = []
    with open(json_string) as file_in:
        json_set = json.load(file_in)
        """ total_val = len(json_set)
        print("Number of notes:", total_val) """
        # for keys_in in json_set:
        for count_it, val in enumerate(json_set[query_num], start=1):
            grab_total = int(count_it)
            items_per_note.append(val)

        return grab_total, items_per_note


def query_item(v2, list_grab):
    unpack_item = []  # ["zero_index_0", "zero_index_1", "zero_index_2"]
    for sub in list_grab[v2]:
        print(sub)
        unpack_item.append(sub)

    return unpack_item


# number_of_notes, items_in = list_notes(string_test)

# grab_total, items_per_note = fetch_merc(string_test, items_in[0])
# print("items_note", grab_total)
# print("merc_items", items_per_note)

# unpack_item = query_item(3, items_per_note)
# fetch merc takes number of nnf

# print(len(sixteen_items))


""" def query_item(item_n, items_list):
    return items_list[item_n] """


""" item_val = query_item(17, sixteen_items)
print(item_val) """

""" append_occurs = []
for item in grab_list[0]:
    print("merc_iterate", item)
    append_occurs.append(item)

print("occurs:", append_occurs) """

# items_of = query_item(0, sixteen_items)
# print("merc:", items_of)
# 0,1,2 indexes, to put on their fields
# set_field = query_item(1)

""" for num, item in enumerate(note_list, start=1):
    print(num) """


"""Merc : 10214682
ICMS: 0,01
ST: 1,86"""
