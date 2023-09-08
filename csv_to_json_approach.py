import json
import pandas as pd

ref_name = "2021-03_C&A0020FX - CDT"
full_data = rf"C:\Users\hugol\Downloads\04-Apr_2023\recup_st_csv\{ref_name}.csv"

test_data = "src\generated_csv\recup_st_loja_373-374_fill.csv"
# partial_data = "nf-data_partial.csv"


def combine_test(dictionaries):
    combined_dict = {}
    for dictionary in dictionaries:
        for key, value in dictionary.items():
            combined_dict.setdefault(key, []).append(value)
    return combined_dict


mapping_first = ["Nfe"]
mapping_second = ["SKU", "ICMS", "ST"]

df = pd.read_csv(full_data, sep=";", encoding="utf-8-sig")

wrapped_list = []
for key, group in df.groupby(mapping_first):
    for merc, icms, st in zip(group["SKU"], group["ICMS"], group["ST"]):
        sub_item = {f"{int(key)}": [f"{int(merc)}", f"{icms}", f"{st}"]}
        # sub_item_k = {f"{key}": [f"Merc = {merc}", f"ICMS = {icms}", f"ST = {st}"]}

        # sub_item_a = {f"{key}": [f"'Merc' : {merc} , 'ICMS' : {icms}, 'ST' : {st}"]}
        wrapped_list.append(sub_item)

# print(wrapped_list)

combined_list = combine_test(wrapped_list)


# print(combined_list)
# stringfy_dict = str(combined_list)
# print(stringfy_dict[0:3])  # Neat way to inspect irregularities on str
# json_dump = json.loads(stringfy_dict)
json_object = json.dumps(combined_list, indent=4)

with open(f"{ref_name}.json", "w") as fp:
    fp.write(json_object)
    fp.close()
