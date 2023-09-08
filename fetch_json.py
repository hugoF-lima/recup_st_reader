import json

string_test = "result_partial_k.json"
query_num = "25276"
with open(string_test) as file_in:
    json_set = json.load(file_in)
    """ total_val = len(json_set)
        print("Number of notes:", total_val) """
    for _ in json_set:  # keys_in
        for count_it, val in enumerate(json_set[query_num], start=1):
            grab_total = int(count_it)
            print(len(val))
            # items_per_note.append(val)


def read_json_unused(file_string, nnf):
    output_base = []
    with open(file_string) as json_file:
        try:
            data = json.load(json_file)
            json_key = data[nnf]
            output_base.append(json_key)
            not_found = False
        except KeyError:
            print("No Results found")  # show labor instead
            not_found = True
        return output_base, not_found


data_out = read_json_unused(string_test, "25276")

print(len(data_out))
