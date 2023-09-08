#!/usr/bin/python3
import base64
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import END, PhotoImage, TclError
from tkinter import filedialog
import json
import win32api, win32con
import time
import simulate_shortcut
from data_handle import list_notes, fetch_merc, query_item

# import win32clipboard
import glob
import os
import os.path
from threading import Thread
from tkinter import messagebox
import subprocess
from itertools import count
import configparser
import automate_desk_task as automate

# from ttkwidgets.autocomplete import AutocompleteCombobox
from PIL import Image
import io

VK_RETURN = 0x0D

field_layset = b"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dGFuY2VJRD0ieG1wLmlpZDpkOGI4MzdhYS03NGY0LTRmOGMtYWZmNS1lM2M1NjVmNTU0MDciCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo2MmY1NmU3MS00MTE2LTQ0ODItYjBjOC04NjBmNzM2YzZhMzYiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICBHSU1QOkFQST0iMi4wIgogICBHSU1QOlBsYXRmb3JtPSJXaW5kb3dzIgogICBHSU1QOlRpbWVTdGFtcD0iMTY1NDg4MzM3MDI2OTg3MyIKICAgR0lNUDpWZXJzaW9uPSIyLjEwLjMwIgogICB0aWZmOk9yaWVudGF0aW9uPSIxIgogICB4bXA6Q3JlYXRvclRvb2w9IkdJTVAgMi4xMCI+CiAgIDx4bXBNTTpIaXN0b3J5PgogICAgPHJkZjpTZXE+CiAgICAgPHJkZjpsaQogICAgICBzdEV2dDphY3Rpb249InNhdmVkIgogICAgICBzdEV2dDpjaGFuZ2VkPSIvIgogICAgICBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOmM1YTQ2YjI2LTE5YTUtNDg1Ny04OTkwLTU5MTgyZDgwMjkyNSIKICAgICAgc3RFdnQ6c29mdHdhcmVBZ2VudD0iR2ltcCAyLjEwIChXaW5kb3dzKSIKICAgICAgc3RFdnQ6d2hlbj0iMjAyMi0wNi0xMFQxNDo0OTozMCIvPgogICAgPC9yZGY6U2VxPgogICA8L3htcE1NOkhpc3Rvcnk+CiAgPC9yZGY6RGVzY3JpcHRpb24+CiA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgCjw/eHBhY2tldCBlbmQ9InciPz4/RbAXAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH5gYKETEezYK0bQAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAOTSURBVGje7ZnNaxtXFMV/epoPJ3It5CI7GJkiSMEptJASgrWq25W96MZLm1IQ9TpJN120y5J65ZJ/IASKNym0XRRUKBRvAq4b7LbEdhaiEkiYpgxyYlsdezQf3cxknhwlkkdRN5kDF6ThncN97917RwdBDB86UAS+BSpAy4+K/6zor+kJS8A24HWJbX9tGxLS51HgC+AGgLh2AeVqBpEbQowoALgHNm79GHtjH/fW3wHva+BLoHFacAW4kZgdRl3Mobwz8sJt2H8e0Fqt4/10FIh+CpCUtnkzMTuMtvQGyqXXup6LGNcR+fO4ByaUrQKwB2wK/3CvA6iLOZIXUz3fXPJiCnUxF3y9DuhJ4GPgE3HtAtrs2JnLQYzrOLqD9+tRFqgIYA5AuZqJXGMSd04AVwBEbiiyoMS9IoAc8LQ0IgmG3Jx42S0mgHpQtFEhcesCuA/g1o+jC4bc+wIoAdgb+5EFJW4p4Rf2JvCW9s1U15br1ILWRw8BdoB3k4Djj6YPXfMYkT+PGNV6EnPKTVp3alC2AD4HNoJe3gTSlK2Ce2CSGNcR43r34XCnJg+Hr+ThAPAboFG2Cs73Bo7ugCpAEyQ0AR64T2yc8r9YPz7C/qwaZBaML3MgA/Z/eQXEiBEjRowYr5hPmUkVyacuM6pNcC45DIDpHNGw9qg0t1hr3u7Np0ypM0xn5pk8d+mF26iZu6zvf8fD1trzfcqUOsN7ry8wMfRm13NJq1my2iTNk0MMt9rZp0xn5hnT8z3f3JieZzoz39mnzKSKvJ1+/8zlkFazCFul2tpq9yn51OXINSZxQ58yqk1EFpS4oU8JSiMKJO4AfYrpHEUWkbihT2lYe5EFJW7oUyrNrciCErckgFVgZ615m5q5e2axmrkb9PUOsNrmU44tk6w2SUrpzTv/c1LhXuMuhlvt7FMMt1ponhwyomRJq9mumd1r3JWHQ2efYrjVwu/NEsJWSSZUFKGhCBXwMJ1DHp1U+OPJz/zw+GaQWexTYsSIESPGK+oCOOUCVgLCMngb4Bng2X4Y/rPlduEVn/sMVgBvAbx18Lwuse6vlUSf2aa3AN6DHsSCeNAuuiRfwDY9ZtYpU+lMdfwb85YjiAUhnWnxqQv4oI8ak7hz+LXlGX1kaIQZVhJ+wSr2qZ9iZ4ED+P9X2INzAY/7EJG4oQv4qw9BiRu6gF/6EJS4pYEU9ktvvYEMh4GMr9gFRMN/+WuSDA2jTM0AAAAASUVORK5CYII="
icon_16_automate = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABhWlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9TpVIqRewg4pCh6mJBVIqjVLEIFkpboVUHk0u/oElDkuLiKLgWHPxYrDq4OOvq4CoIgh8gjk5Oii5S4v+SQotYD4778e7e4+4dIDQqTDV7JgFVs4xUPCZmc6ui7xV+BDGAKMYlZuqJ9GIGXcfXPTx8vYvwrO7n/hz9St5kgEcknmO6YRFvEEc3LZ3zPnGIlSSF+Jx4wqALEj9yXXb5jXPRYYFnhoxMap44RCwWO1juYFYyVOIZ4rCiapQvZF1WOG9xVis11ronf2Egr62kuU5zBHEsIYEkRMiooYwKLERo1UgxkaL9WBf/sONPkksmVxmMHAuoQoXk+MH/4He3ZmF6yk0KxIDeF9v+GAV8u0Czbtvfx7bdPAG8z8CV1vZXG8DsJ+n1thY+AoLbwMV1W5P3gMsdYOhJlwzJkbw0hUIBeD+jb8oBg7eAf83trbWP0wcgQ10t3wAHh8BYkbLXu7y7r7O3f8+0+vsB4INy05F1H4QAAAAGYktHRAD/AIAAgD+q5FMAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQfmCg8ROwgxl/SFAAAB20lEQVQ4y43TTYiPURQG8N/8GcwwE0UjFEr5aGrMaFbcBflYsHBXsiSXKdFMWVgoYWMjyWe9YmNhgXelpBTeyDRSYzNSiiaKjCZTaCQ2d+pvUO7unM55znOe81z+8xVlVSvKqnFyfuo/imehAwvxCO3YjFs5/jtAUVZTsAk9aMYQ3uAAtqK5KKvXKYa3Ez21eorYiyO4iR3oTTH04wSuYxouF2W1aqKvoQ5gGw6jL8UwkHNtWIF+zMA3HEI3dqcYRqbmwlbsw8UUw0BRVh2Yh04cxB5Mx2OcwhXsxLmJFdZkPW7neEOmvC7njuIsFqcYvuIaNhVl1TIB0I6XKYbRoqzmZLD72JVi6EFfFnNOPuUgZmJRrSirBszFgqKslmN7FvJJiuFTHjCILziPZRjDD7TWsBYRW7AAJU6iuyir2XUMm9CLV2jBFIzVMIALedenKYbRPG0jrhZldRZnsBTvUwzjWJ1rhhvqPNCB1hTDg6KsutCWC/fnCzXjIUYy2+8phrv1PliD0ziWYriXc/OxMtu3MZ90PW6nGM5MtvIzXMLxoqy6cQPD+Rqt6MpadeY/8bsT88SG7ImU1f6M8TrR7uAdhlIMz/8AqANqxJIM0oSPeJFi+JCHSDH8hF9OoZ16VHbS3wAAAABJRU5ErkJggg=="
icon_128_automate = b"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"


# TODO: Add a option to generate a json from excel file
class RoughSketchApp:
    def __init__(self, master=None):
        # build ui.. tk's don't work with winfochildren...
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        self.frame1 = tk.Frame(self.toplevel1)
        self.nnf_v_lbl = tk.Label(self.frame1)
        self.nnf_v_lbl.configure(cursor="arrow", justify="left", text="Num. NF:")
        self.nnf_v_lbl.grid(column="0", padx="15", pady="10", row="2", sticky="e")
        self.icms_v_lbl = tk.Label(self.frame1)
        self.icms_v_lbl.configure(cursor="arrow", justify="left", text="ICMS:")
        self.icms_v_lbl.grid(column="0", padx="15", pady="10", row="4", sticky="e")
        self.st_v_lbl = tk.Label(self.frame1)
        self.st_v_lbl.configure(cursor="arrow", justify="left", text="ST:")
        self.st_v_lbl.grid(column="0", padx="15", pady="10", row="5", sticky="e")
        self.json_f_v_lbl = tk.Label(self.frame1)
        self.json_f_v_lbl.configure(
            cursor="arrow", justify="left", text=": Arquivo Json"
        )
        self.json_f_v_lbl.grid(column="1", pady="10", row="0", sticky="w")
        self.merc_v_lbl = tk.Label(self.frame1)
        self.merc_v_lbl.configure(cursor="arrow", justify="left", text="Mercadoria:")
        self.merc_v_lbl.grid(column="0", padx="15", pady="10", row="3", sticky="e")

        # Buttons
        self.start = tk.Button(self.frame1)
        self.start.configure(text="Iniciar!")
        self.start.configure(command=self.call_automate)
        self.start.configure(state="disabled")
        self.start.grid(column="0", padx="10", row="6")
        self.pick_json = tk.Button(self.frame1)
        self.pick_json.configure(text="Abrir!")
        self.pick_json.configure(command=self.read_and_populate)
        self.pick_json.grid(column="0", row="0", sticky="e")
        self.next_merc_btn = tk.Button(self.frame1)
        self.next_merc_btn.configure(text=">", command=self.next_merc)
        self.next_merc_btn.configure(state="disabled")
        self.next_merc_btn.grid(column="2", padx="10", row="6", sticky="e")
        self.prev_merc_btn = tk.Button(self.frame1)
        self.prev_merc_btn.configure(text="<", command=self.prev_merc)
        self.prev_merc_btn.configure(state="disabled")
        self.prev_merc_btn.grid(column="1", row="6", sticky="e")
        self.prev_nnf_btn = tk.Button(self.frame1)
        self.prev_nnf_btn.configure(text="<", command=self.prev_nnf)
        self.prev_nnf_btn.configure(state="disabled")
        self.prev_nnf_btn.grid(column="1", row="2", sticky="e")
        self.next_nnf_btn = tk.Button(self.frame1)
        self.next_nnf_btn.configure(text=">", command=self.next_nnf)
        self.next_nnf_btn.configure(state="disabled")
        self.next_nnf_btn.grid(column="2", row="2")

        self.insert_img = tk.Label(self.frame1)
        self.img_recup_lay_set = tk.PhotoImage(data=(field_layset))
        self.insert_img.configure(
            cursor="arrow", image=self.img_recup_lay_set, justify="left"
        )
        self.insert_img.grid(column="1", row="3", rowspan="3", sticky="e")

        # custom vars and related... Read pandas from JSon rather than XML

        self.item_list = []

        self.incr_decr_nnf = int(0)  # One of the data attrib's
        self.nnf_incr_decr_s_var = tk.StringVar(value=f"{self.incr_decr_nnf} of")
        self.nnf_total = int(0)
        self.nnf_total_s_var = tk.StringVar(value=f"{self.nnf_total}")

        self.incr_decr_merc = int(0)  # One of the data attrib's
        self.merc_item = tk.StringVar(value=f"{self.incr_decr_merc} of")
        self.merc_total = int(0)
        self.merc_total_s_var = tk.StringVar(value=f"{self.merc_total}")

        self.pick_folder = ""

        # Changeable Labels

        self.total_num_merc_lbl = tk.Label(self.frame1)
        self.total_num_merc_lbl.configure(
            cursor="arrow", justify="left", textvariable=self.merc_total_s_var
        )
        self.total_num_merc_lbl.grid(column="1", padx="15", pady="10", row="6")
        self.current_note_merc_lbl = tk.Label(self.frame1)
        self.current_note_merc_lbl.configure(
            justify="left", textvariable=self.merc_item
        )

        self.current_note_merc_lbl.grid(
            column="1", columnspan="4", padx="50", pady="10", row="6", sticky="w"
        )

        self.total_nnf_lbl = tk.Label(self.frame1)
        self.total_nnf_lbl.configure(
            cursor="arrow", justify="left", textvariable=self.nnf_total_s_var
        )
        self.total_nnf_lbl.grid(column="2", pady="10", row="1")

        self.current_lbl_nnf = tk.Label(self.frame1)
        self.current_lbl_nnf.configure(
            justify="left", textvariable=self.nnf_incr_decr_s_var
        )
        self.current_lbl_nnf.grid(
            column="1", columnspan="4", padx="45", row="1", sticky="e"
        )

        # Entries
        self.mercadoria_val = ttk.Entry(self.frame1)
        self.mercadoria_val.grid(column="1", padx="30", row="3")
        self.icms_val = ttk.Entry(self.frame1)
        self.icms_val.grid(column="1", padx="30", row="4")
        self.st_val = ttk.Entry(self.frame1)
        self.st_val.grid(column="1", padx="30", row="5")
        self.json_path = ttk.Entry(self.frame1)
        self.json_path.grid(column="0", columnspan="4", padx="45", row="1", sticky="w")
        self.entry_nnf = ttk.Combobox(self.frame1)
        self.entry_nnf.configure(width="12")
        self.entry_nnf.grid(column="1", row="2", sticky="w")

        self.frame1.configure(height="200", width="200")
        self.frame1.grid(column="0", row="0")
        self.toplevel1.configure(height="200", width="200")
        self.toplevel1.title("Recup ST Automate")

        self.icon_16_img = PhotoImage(data=(icon_16_automate))
        # self.icon_128_img = PhotoImage(data=(icon_128_automate))
        self.toplevel1.iconphoto("-default", self.icon_16_img)

        # decode_b64 = base64.decode(icon_128_automate)
        # decoded_icon = io.StringIO(decode_b64)

        self.icon_128_img = PhotoImage(data=(icon_128_automate))
        # setting icon through b64string
        self.toplevel1.tk.call("wm", "iconphoto", self.toplevel1._w, self.icon_128_img)
        # Main widget
        self.mainwindow = self.toplevel1

        # Binding

        for entry in filter(
            lambda w: isinstance(w, ttk.Entry), self.frame1.winfo_children()
        ):
            entry.bind("<ButtonRelease-1>", self.select_all)

        # Selection only returns value upon this bind... I wonder how for AutocompleteBox
        self.entry_nnf.bind(
            "<<ComboboxSelected>>",
            lambda _: self.filter_combo(self.entry_nnf.current()),
        )

    def run(self):
        self.mainwindow.mainloop()

    def select_all(self, *event):  # That kind of return is new
        for e in event:  # unpacking star args
            e.widget.select_range(0, "end")  # widget abstraction
        return "break"

    def retrieve_from_num_get(self, retrieved_number):
        found_note = False
        for index, item in enumerate(self.item_list):
            if item == retrieved_number:
                found_note = True
                print(index, item)
                self.entry_nnf.current(index)
                # Doubts of the indexing here
                self.incr_decr = index + 1

                self.change_event(qnf=self.incr_decr, qmerc=self.incr_decr_merc)

                print("Would you budge?", self.incr_decr)
        return found_note

    def automate_start(self):
        try:
            automate.window_restore()
            # got_nf = True
            got_nf, coords = automate.update_coords()
            fill_merc = False
            while got_nf == True:  # For future improve
                fill_merc = False
                # nnf_total_run = self.nnf_total
                # take from tk window instead
                # print("Start Merc is", start_merc)
                get_num = automate.number_get(coords)
                # Condition match not Working yet
                # print("Does note match:", get_num, note_compare)

                found_note = self.retrieve_from_num_get(str(get_num))

                current_value = 1  # Maybe this was causing the glitch (Nope)
                start_merc = count(self.incr_decr_merc)
                # start_merc = count(1)
                note_compare = self.entry_nnf.get()
                # put an internal_list
                _, grab_mercs = fetch_merc(self.pick_folder, note_compare)
                merc_fill_loop = self.merc_total

                # if get_num != int(note_compare):
                if found_note == False:
                    automate.call_next_note(coords)
                else:
                    # for i in range(merc_fill_loop):
                    while fill_merc == False:
                        match_merc, merc_check, tax_values = automate.match_merc(
                            grab_mercs, coords
                        )
                        # this repeats for some reason...
                        # print("Does it match true here", match_merc, merc_check)

                        if match_merc == False:
                            automate.call_next_merc(coords)  # A simple solution
                        else:
                            self.mercadoria_val.delete(0, END)
                            self.icms_val.delete(0, END)
                            self.st_val.delete(0, END)
                            self.mercadoria_val.insert(END, merc_check)
                            self.icms_val.insert(END, tax_values[0])
                            self.st_val.insert(END, tax_values[1])

                            values_changed = automate.change_merc_items_unord(
                                coords, merc_check, tax_values
                            )
                            if values_changed == True:  # I hope this conditioning works
                                self.next_merc_btn.invoke()
                                current_value = next(
                                    start_merc
                                )  # only increase if filled
                                print(
                                    "cur_val", current_value, "to", self.incr_decr_merc
                                )
                                print("merc_val", merc_fill_loop)
                            else:
                                # current_value = next(start_merc)  # only increase if filled
                                print("cur_val", current_value)
                                print(
                                    "cur_val", current_value, "to", self.incr_decr_merc
                                )
                                print("merc_val", merc_fill_loop)

                            if merc_fill_loop == 1 or current_value == merc_fill_loop:
                                # This eval doesn't work if merc_runtimes is already 1?

                                print(self.incr_decr_merc)
                                automate.gravar_last_item()
                                automate.call_next_note(coords)
                                """ time.sleep(0.5)
                                simulate_shortcut.PressKey(VK_RETURN) """
                                self.next_nnf_btn.invoke()
                                merc_fill_loop = self.merc_total
                                fill_merc = True
                                automate.clear_clipboard()
        except IndexError:
            messagebox.showerror(
                title="Janela Não Encontrada",
                message=f"Não foi possível encontrar janela do Synchro.\n\n Certifique que o Synchro esteja no modulo: 'Recup ST' > \n 'Digitação/Manutenção de Documentos Fiscais' \n'.",
            )

    def call_automate(self):
        try:
            paralel_t = Thread(target=self.automate_start, daemon=True)
            paralel_t.start()
        except TclError as tc:
            messagebox.showerror(title="Error", message="Unable to launch")

    def read_and_populate(self):  # gonna have to chain here
        store_path = self.pick_folder
        self.pick_folder = self.return_file_path(self.json_path)
        if self.pick_folder != None:
            self.zero_labels()  # Because labels need their own tree for erasing
            # call the main populate
            self.incr_decr_nnf += 1
            self.incr_decr_merc += 1
            # value change in qnf and qmerc
            self.nnf_total, self.merc_total = self.change_event(
                qnf=self.incr_decr_nnf, qmerc=self.incr_decr_merc
            )

            # correct
            # todo: Check the glitchy number 1 being displayed... when 240 notes are in...
            self.nnf_total_s_var.set(f"{self.nnf_total}")  # I smell redundancy here
            print("Number of notes from Integer", self.nnf_total)
            print("Number of notes from tk", self.nnf_total_s_var.get())
            self.merc_total_s_var.set(f"{self.merc_total}")

            self.nnf_incr_decr_s_var.set(f"{self.incr_decr_nnf} of ")
            self.merc_item.set(f"{self.incr_decr_merc} of ")  # correct
            # todo: Check the glitchy number 1 being displayed... when 240 notes are in...
            self.nnf_total_s_var.set(f"{self.nnf_total}")  # I smell redundancy here
            print("Number of notes from Integer", self.nnf_total)
            print("Number of notes from tk", self.nnf_total_s_var.get())
            self.merc_total_s_var.set(f"{self.merc_total}")
            # enable buttons
            self.start.configure(state="active")

        elif self.pick_folder == None:
            self.pick_folder = store_path

    def prev_btn_nnf_state(self, *widget):
        for w in widget:
            if self.incr_decr_nnf == 1:
                w.configure(state="disabled")
            else:  # too primitive
                w.configure(state="active")

    def prev_btn_merc_state(self, *widget):
        for w in widget:
            if self.incr_decr_merc == 1:
                w.configure(state="disabled")
            else:  # too primitive
                w.configure(state="active")

    def next_btn_nnf_state(self, *widget):
        for w in widget:
            if self.incr_decr_nnf == self.nnf_total:
                w.configure(state="disabled")
            else:  # too primitive
                w.configure(state="active")

    def next_btn_merc_state(self, *widget):
        for w in widget:
            if self.incr_decr_merc == self.merc_total:
                w.configure(state="disabled")
            else:  # too primitive
                w.configure(state="active")

    def next_nnf(self):
        self.incr_decr_nnf += 1
        self.incr_decr_merc = 1
        self.change_event(qnf=self.incr_decr_nnf)
        self.update_display()
        self.prev_btn_merc_state(self.prev_merc_btn)
        self.next_btn_merc_state(self.next_merc_btn)

    def next_merc(self):
        self.incr_decr_merc += 1
        self.change_event(qnf=self.incr_decr_nnf, qmerc=self.incr_decr_merc)
        self.update_display()

    def prev_nnf(self):
        self.incr_decr_nnf -= 1
        self.incr_decr_merc = 1
        self.change_event(qnf=self.incr_decr_nnf, qmerc=self.incr_decr_merc)
        self.update_display()
        self.prev_btn_merc_state(self.prev_merc_btn)
        self.next_btn_merc_state(self.next_merc_btn)

    def prev_merc(self):
        self.incr_decr_merc -= 1
        self.change_event(qnf=self.incr_decr_nnf, qmerc=self.incr_decr_merc)
        self.update_display()

    def zero_labels(self):
        self.incr_decr_nnf = 0
        self.nnf_total = 0
        self.nnf_incr_decr_s_var.set(f"{self.incr_decr_nnf} of")
        self.nnf_total_s_var.set(f"{self.nnf_total}")

        self.incr_decr_merc = 0
        self.merc_total = 0
        self.merc_total_s_var.set(f"{self.nnf_total_s_var}")
        self.merc_item.set(f"{self.merc_total}")

    def return_file_path(self, text_widget):
        json_string = filedialog.askopenfilename(
            initialdir=r"C:\Users\AS informática\Downloads"
        )

        if json_string != "":
            text_widget.insert(END, json_string)

            # self.display_path.insert(END, json_text)  #

            return json_string

    def update_display(self):
        # I smell redundancy here
        self.nnf_incr_decr_s_var.set(f"{self.incr_decr_nnf} of")
        self.merc_item.set(f"{self.incr_decr_merc} of")

        self.nnf_total_s_var.set(f"{self.nnf_total}")  # I smell redundancy here
        self.merc_total_s_var.set(f"{self.merc_total}")

    def filter_combo(self, grabbed_index):
        self.incr_decr = grabbed_index + 1
        self.change_event(qnf=self.incr_decr)
        self.prev_btn_nnf_state(self.prev_nnf_btn)  # feels redundant

    def change_event(self, qnf=1, qmerc=1):
        # v1 and v2 are for real_time use
        # Cleaning and loading xml data
        for entry in filter(
            lambda w: isinstance(w, ttk.Entry), self.frame1.winfo_children()
        ):
            entry.delete(0, END)

        total_notes_of, self.item_list = list_notes(self.pick_folder)
        corrected_q_nf = qnf - 1
        self.entry_nnf["values"] = self.item_list
        # self.entry_nnf.configure(completevalues=self.item_list)  # So apparently this doesn't sort alphabetically?
        self.entry_nnf.current(corrected_q_nf)  # first_insert
        # self.entry_nnf.insert(END, item_list[corrected_q_nf])  # first_insert
        # v1 and v2 need a role here...
        print("val_list index", qnf)
        total_merc_of, merc_items = fetch_merc(
            self.pick_folder, self.item_list[corrected_q_nf]
        )
        # the above brings 45 rather than 16
        # I see, fetch_merc
        correct_q_merc = qmerc - 1
        items_result = query_item(correct_q_merc, merc_items)
        self.mercadoria_val.insert(END, items_result[0])
        self.icms_val.insert(END, items_result[1])
        self.st_val.insert(END, items_result[2])
        self.prev_btn_nnf_state(self.prev_nnf_btn)
        self.next_btn_nnf_state(self.next_nnf_btn)
        self.prev_btn_merc_state(self.prev_merc_btn)
        # the issue might be here!
        self.next_btn_merc_state(self.next_merc_btn)
        # nnf_item_merc
        # incr_decr_nnf
        # self.update_display()
        self.incr_decr_nnf = qnf
        self.incr_decr_merc = qmerc
        self.merc_total = total_merc_of
        self.nnf_total = total_notes_of
        self.nnf_incr_decr_s_var.set(f"{self.incr_decr_nnf} of ")
        self.merc_item.set(f"{self.incr_decr_merc} of ")
        self.nnf_total_s_var.set(f"{self.nnf_total}")  # I smell redundancy here
        self.merc_total_s_var.set(f"{self.merc_total}")
        """ self.nnf_incr_decr_s_var.set(f"{self.incr_decr_nnf} of")
        self.merc_item.set(f"{self.incr_decr_merc} of")

        self.nnf_total_s_var.set(f"{self.nnf_total}")  # I smell redundancy here
        self.merc_total_s_var.set(f"{self.merc_total}") """

        return total_notes_of, total_merc_of


if __name__ == "__main__":
    app = RoughSketchApp()
    app.run()
