# Automate the stuff here
import time
from pyperclip import paste
from win32 import win32clipboard
from base64 import b64decode
import io
from PIL import Image

# import keyboard  # Because pyautogui keyboard doesn't give a damn
import simulate_shortcut
import pyautogui as pg
from pyautogui import locateCenterOnScreen as locate_element
from win32 import win32gui
import pygetwindow
from pygetwindow import getWindowsWithTitle as get_win
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed
from itertools import count
from threading import Event as exit_event

# To enable LocateOnScreen on all monitors
from PIL import ImageGrab
from functools import partial

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

locate_warning_remove = b"""<plain_txt_msg:img>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JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNC40LjAtRXhpdjIiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iCiAgICB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIgogICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICAgeG1sbnM6R0lNUD0iaHR0cDovL3d3dy5naW1wLm9yZy94bXAvIgogICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iCiAgIHhtcE1NOkRvY3VtZW50SUQ9ImdpbXA6ZG9jaWQ6Z2ltcDpjY2M2MTk3Ny0yMzUzLTQ3MWQtODIyOC02ZDQ0MTlkYjVhZmYiCiAgIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6OWEwYjkyNWEtNTViOS00NjNkLWI1ZDAtNjYxMjVhMzFkYmMyIgogICB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ZTU0ZjliODctZDI1OS00YWJhLWI0NTMtMGZjMzI5MGNlZDk3IgogICBkYzpGb3JtYXQ9ImltYWdlL3BuZyIKICAgR0lNUDpBUEk9IjIuMCIKICAgR0lNUDpQbGF0Zm9ybT0iV2luZG93cyIKICAgR0lNUDpUaW1lU3RhbXA9IjE2NjQ2NTUzMDExNjY4OTEiCiAgIEdJTVA6VmVyc2lvbj0iMi4xMC4zMiIKICAgdGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb29sPSJHSU1QIDIuMTAiCiAgIHhtcDpNZXRhZGF0YURhdGU9IjIwMjI6MTA6MDFUMTc6MTQ6NTktMDM6MDAiCiAgIHhtcDpNb2RpZnlEYXRlPSIyMDIyOjEwOjAxVDE3OjE0OjU5LTAzOjAwIj4KICAgPHhtcE1NOkhpc3Rvcnk+CiAgICA8cmRmOlNlcT4KICAgICA8cmRmOmx
pCiAgICAgIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiCiAgICAgIHN0RXZ0OmNoYW5nZWQ9Ii8iCiAgICAgIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6ZDFiNGUwMzUtYjkyZi00NDc0LWEzZmYtODc5YzFmNDc0ZTJhIgogICAgICBzdEV2dDpzb2Z0d2FyZUFnZW50PSJHaW1wIDIuMTAgKFdpbmRvd3MpIgogICAgICBzdEV2dDp3aGVuPSIyMDIyLTEwLTAxVDE3OjE1OjAxIi8+CiAgICA8L3JkZjpTZXE+CiAgIDwveG1wTU06SGlzdG9yeT4KICA8L3JkZjpEZXNjcmlwdGlvbj4KIDwvcmRmOlJERj4KPC94OnhtcG1ldGE+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAKPD94cGFja2V0IGVuZD0idyI/PrEq+WsAAAAGYktHRAD/AP8A/6C9p5MAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAHdElNRQfmCgEUDwEVdQoOAAAHM0lEQVRYw82YbUyb1xXHfwYSAikGbDDBENuxAzSE8FIIacZAK4ka2mofQlfSD9uHqVO2qZWmaZpUqS/avkzRNE1bt0ldVmmaNqka3dImi5Z0S0gWliYhgIlrMBhsg4HH8PgFUmOw8ds+uNh5YkOWbNpypCP5ufc+9/nfc+75n3Msi8fjxTwmkvMwi0VR9NltNpxOJ4Ig4PV68fv9yXmdTodarUaj0aA3GFCpVIqH2V/271jGarUO3hkZ0Y+OjqI3GNBqtajVapRKJXK5PLnO4XAgCAIzMzPYbTb2799PQ2Ojvbq6uuU/BuPxeHzXr1/HYbfT2NREXV3dpaWlpaOCICRAuvKZda0m1++t3AbA4YZSihX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<!plain_txt_msg>"""

error_icon = b"<plain_txt_msg:img>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<!plain_txt_msg>"

red_square_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAABwAAAAXCAYAAAAYyi9XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAMUSURBVEhLvVY9TFNRGD2lpQRoUmJIIylLCUUYdLGEOKCDVQMLhEDShKmLIhOjLgwsrExoXHCsCwYH8KcsLg1SY2IiIbSAiWkg1RhICtXSH7/zeBh8977CYDjJyX33u9/5Tu99P18de3t7FVwgaszxwnCuHZZKJeTzeRQKBRSLRZTLZdTU1MDlcsHtdqO+vh5Op9PMro6qhiy8v7+PjY0NLC0tYXV1FVtbW8jlcvB4PGhra0N3dzf6+vrQ0dEBr9dr/JBqsDXkbtLpNObm5vBxcRG+nR34KxV4hC5ZLwpzDgcywmxLC6739yMajaK9vd3YtR20hkdHR1hZWcHTmRn8jMcRlthNYVDYLKwT/hb+EKaE74Vx4aVwGGMTE+jp6UFtba1EVCiGPMb19XVMT06iKGYRid0RthireuwI3wljQpeYPp6aQmdnp/Z4lQjvD48xu7xsmPULq5kRXGce86mjnnV0UAzX1tbwSR6Q23KvuDMe4XnAPOZTRz3r6KAYLiwswLu7i1tyfdbOrGA+ddSzjg6KYSKRQLPcxyvm3IrXwoDJ5wxYQB31rKODYri5uYkGEdgdZVT41eRDBiygjnrW0UExPDg4MIK6N4m72z2+NPDLHE+DOupZRwfFsKmpyXip88fTf6DbkRXUUc86OiiGXV1dyMn7w51YvwgPzNEOzKeOetbRQTHs7e3Fd/kofzHnp/FIOH18aWDMHE+DOupZRwfFcHBwEPlAAG/lOi207pKmjJFPGDDBOfOpo551dFAMW1tbcXd4GB/q6vBK5t+EVlMruM485lNHPevooBg2NjZidHQUV0dG8FLELyTGDzQfhLLwxJwj54xznXnMp4561tFB2y3YcFOpFJ7NziIxP4/Q4SHuybt1TdYuC0+6BR+Qz8I38pAkGxpwY2gI98fHEQwGbRuybT+syDcxm80iFoshLp+pnDRet3R9p/RJh6xVpA+WpO8VpNt7pBGHBwYQiUTg8/ngkDU72BqegH8pMpkM4tKqkskktre3/3b8gDwcoVAIYWlJfr/f+MtxFs40/L8A/gB0ajveVmSMOQAAAABJRU5ErkJggg==<!plain_txt_msg>"
dark_purple_square_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV+/qEhF1A4iDhmqixZERRylikWwUNoKrTqYXPoFTRqSFBdHwbXg4Mdi1cHFWVcHV0EQ/ABxdHJSdJES/5cUWsR4cNyPd/ced+8Ab6PCFMM/ASiqqafiMSGbWxWCr/CjH30IYExkhpZIL2bgOr7u4eHrXZRnuZ/7c/TIeYMBHoF4jmm6SbxBPLNpapz3icOsJMrE58TjOl2Q+JHrksNvnIs2e3lmWM+k5onDxEKxg6UOZiVdIZ4mjsiKSvnerMMy5y3OSqXGWvfkLwzl1ZU012kOI44lJJCEAAk1lFGBiSitKikGUrQfc/EP2f4kuSRylcHIsYAqFIi2H/wPfndrFKYmnaRQDAi8WNbHCBDcBZp1y/o+tqzmCeB7Bq7Utr/aAGY/Sa+3tcgR0LsNXFy3NWkPuNwBBp80URdtyUfTWygA72f0TTlg4BboXnN6a+3j9AHIUFfLN8DBITBapOx1l3d3dfb275lWfz9ok3KjzjZLlwAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAAuIwAALiMBeKU/dgAAAAd0SU1FB+YEEhIIBNNPUuQAAAAZdEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAABvklEQVQ4y7XVv2tTURQH8E9f8hJLxJDK61DaIYNQB4dCh3Yyjh1cOroIQffWVUepm/4H3bpUELcOLl0E0dLq0NYtgZaCEqJSH8/0R+qSJ08R24b6hQP3Xs73y72Hc76Xv6OIOp6jgcNeNHpn9V7OmXAfmzg5JTZ7ub9hILMewiPMQ61UVy1NGCqMGMxdBsnxd+2DPY14w2q8mPKe4THafwo+xfx4WDNVmTU2eP2fz9hJtr358sLHw9VU9AHkMs9cGA9rbl69Y+TStVPrUg4jUWFM3NnX6jansYf1oFfcOZiqzBouVs9aa8PFqqnKbLqdQzGHu7hXK9XdKN9yXpTDSHAUah5uRGgEmIFqaUK/yHBnAkzCUGGkb8EMdzLAKH61Rj/IcEcDF4wAu2nT9osMdzfAGrQP9voWzHDXAqxAI97oWzDDXQmwhK3VeNFOsn1usZ1kO53rLSzlcNyzpts/DhJRYUwpXzmT2OdOw+v2sla3CQ/xNp3ldZRb3eZ03Nl3JR8ph9GpN3vdXs6aw5OsOcA7FFrd5vT7eEVwFMoNhPJBQT4IcSI53vep0/Dh2ysvvy6kN0vtK/kvBuuiv4CfS52pWj+J87cAAAAASUVORK5CYII=<!plain_txt_msg>"
green_square_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV+/qEhF1A4iDhmqixZERRylikWwUNoKrTqYXPoFTRqSFBdHwbXg4Mdi1cHFWVcHV0EQ/ABxdHJSdJES/5cUWsR4cNyPd/ced+8Ab6PCFMM/ASiqqafiMSGbWxWCr/CjH30IYExkhpZIL2bgOr7u4eHrXZRnuZ/7c/TIeYMBHoF4jmm6SbxBPLNpapz3icOsJMrE58TjOl2Q+JHrksNvnIs2e3lmWM+k5onDxEKxg6UOZiVdIZ4mjsiKSvnerMMy5y3OSqXGWvfkLwzl1ZU012kOI44lJJCEAAk1lFGBiSitKikGUrQfc/EP2f4kuSRylcHIsYAqFIi2H/wPfndrFKYmnaRQDAi8WNbHCBDcBZp1y/o+tqzmCeB7Bq7Utr/aAGY/Sa+3tcgR0LsNXFy3NWkPuNwBBp80URdtyUfTWygA72f0TTlg4BboXnN6a+3j9AHIUFfLN8DBITBapOx1l3d3dfb275lWfz9ok3KjzjZLlwAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAAuIwAALiMBeKU/dgAAAAd0SU1FB+YEEhILLiPZyPEAAAAZdEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAABtElEQVQ4y7XVQUtUURgG4GfOzNwraoZCjYsLIbioFi0iBP+BLvoFEoHkWm3TopZRu6J/IESrFm0C+wuZuAiMFgMGDlEQSYM1Ms690+ZO3kIaG+yFD845nPflfB/f9x6OR4xFPMcODvPYyc8W8zsnwhK20e0T2/nd31AqrCdwD6sQlidVZsaFZEgYq4Cs2ZE1DnQ29mRPPvV4j3EfX/8UfITV0tyo6kKicmXsr2l03jYdPmvovtrvid6GciHNB6W5UdHSBZVLZ/rWJdRiYWpY1mxRb8/iI7ZCXtwVqC4kytMjJ6218vSI6kLS264gLuMmboXlSdHcef+KUIulcar7ev8cdgLmoTIzblAUuPMB1yAkQwMLFrjXAhL8ao2BBI+4SXDKCGj0mnZQFLiNgE3IGgeDCx5xNwPWobOxN7Bggbteyht7C5ejpxf7jtxxI9i+8R7e4WoZaW5N17PWgTA1LExEJxJL698dru1Sb8NdbPRmeQtn1duzWbOlVIuFWtzfHNZ2i+bwsGgO8AaRens2ffFFGqdUA1FQigJdsm8daf2H9svPOnc+9F7Ws6/WfzFYp/0F/ATSPqGFspUBxQAAAABJRU5ErkJggg==<!plain_txt_msg>"

synchro_win_header = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAABMAAAAUCAYAAABvVQZ0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAABySURBVDhP7ZDtCsAgCEV9dB/NN2tzzLiWfSz6scEOXEq0Q0VpIx+QEVHOKl6mq+0X5F5m0RoDvR65a4Mi4g5f0T7MtKhkJaW8x1CGvFvGzHdV42QW/acIk1lKwuugGOUoixi/7QTFPaZks/yy52yUpXQA2zVZAPgs8KoAAAAASUVORK5CYII=<!plain_txt_msg>"
VK_DOWN = 0x28
VK_RETURN = 0x0D
VK_LEFT = 0x25

decoded_img_cache = {}


def decode_img(msg):
    msg = msg[
        msg.find(b"<plain_txt_msg:img>")
        + len(b"<plain_txt_msg:img>") : msg.find(b"<!plain_txt_msg>")
    ]
    msg = b64decode(msg)
    buf = io.BytesIO(msg)
    img = Image.open(buf)
    return img


def remove_stall_dialogs(sleep_default=0.1):
    loc_f = locate_element(decode_img(locate_warning_remove), grayscale=False)
    loc_g = locate_element(decode_img(error_icon), grayscale=False)
    if loc_f or loc_g:
        print("Stall dialog for g", loc_g)
        print("Stall dialog for f", loc_f)
        simulate_shortcut.single_Key(VK_RETURN)
        time.sleep(sleep_default)


def moving_into(element, pausefloat, keyrelease, clicks_in, x_offset=0):
    loc_f = locate_element(decode_img(element), grayscale=False)
    if not loc_f:
        print("Field not found")
        return False
    else:
        time.sleep(pausefloat)
        loc_f = (
            loc_f[0] - x_offset,
            loc_f[1],
        )  # Where the offset thing happens
        pg.click(
            loc_f, clicks=clicks_in
        )  # Changing contents do require mouse for now...
        grab_me = copy_clipboard()
        time.sleep(pausefloat)  # Though i could write a string to memory grabbing
        simulate_shortcut.get_key_comb(f"{keyrelease}")  # the contents on the field...
        time.sleep(pausefloat)  # It would've been neat
        return grab_me


# With cache handling(?)
""" def locate_img_new(img_gather, pausefloat: float, click_it=True, clicknum=1):
    # Decode the base64 string into bytes
    found_elem = False
    img_bytes = b64decode(img_gather)

    # Check if the decoded image is already in the cache
    if img_gather in decoded_img_cache:
        obj_search = decoded_img_cache[img_gather]
        
    else:
        # Decode the image from bytes to an Image object
        img = Image.open(io.BytesIO(img_bytes))
        # Add the decoded image to the cache
        decoded_img_cache[img_gather] = img

        # Search for the image on the screen
        obj_search = locate_element(img, grayscale=True, confidence=0.7)
        time.sleep(pausefloat)

        if not obj_search:
            print("Element not found")
            found_elem = False
        else:
            if click_it == True:
                pg.click(obj_search, clicks=clicknum)
                time.sleep(pausefloat)
            found_elem = True

    return found_elem, obj_search """


# Original without cache handling
def locate_img_new(img_gather, pausefloat: float, click_it=True, clicknum=1):
    found_elem = False
    obj_search = locate_element(decode_img(img_gather), grayscale=True, confidence=0.7)
    time.sleep(pausefloat)
    if not obj_search:
        print("Element not found")
        found_elem = False
    else:
        if click_it == True:
            pg.click(obj_search, clicks=clicknum)
            time.sleep(pausefloat)
        found_elem = True
    return found_elem, obj_search


def window_restore():  # helper...
    while True:
        win_identifier = get_win(f"Documentos Fiscais - Controle de ST")[0]
        if win_identifier:
            win_identifier.activate()
            win_identifier.restore()
            time.sleep(0.2)
            break
        else:
            print("No window was found")


def copy_clipboard():  # Make this a bool function?
    simulate_shortcut.get_key_comb("ctrl+c")
    time.sleep(0.01)
    return paste()


def update_coords():
    nav, coords = locate_img_new(
        img_gather=synchro_win_header, click_it=False, pausefloat=0.2
    )
    print(nav, coords)
    return nav, coords


# Read if actual note is selected
# get value from txt insert

# alterar_icms_saida


# evaluate if get!
# I wonder if this may stall when highlighting the next empty note or something
def number_get(coords):
    note_check = None
    while note_check is None:
        try:
            # x= 625, y=98
            obj_click = pg.moveTo(
                x=coords[0] + 305, y=coords[1] + 81, duration=0.1
            )  # Click NFE item
            time.sleep(0.2)
            pg.click(obj_click, clicks=2)
            note_check = copy_clipboard()
            if int(note_check):
                print("num is here", int(note_check))
        except ValueError:
            remove_stall_dialogs(0.01)
            pass  # Not working apparently

        return int(note_check)  # Ignoring exception at return because window delay


# Something faulty with this block (at least on the call_next_note bit)
def match_note(note_compare):
    check = True
    note_check, coords = number_get()
    print("Hey, it's match_note", note_check)
    if note_check != note_compare:
        check = False

    return check, coords


# Sometimes this doesn't work when annoying window
def merc_grab(coords):
    print("here it is", coords)
    merc_check = None
    while merc_check is None or str:
        try:  # i wonder if this is enough
            # x=532, y=342
            obj_click = pg.moveTo(
                x=coords[0] + 212, y=coords[1] + 299, duration=0.1
            )  # Merc coords
            time.sleep(0.2)
            pg.click(obj_click, clicks=2)
            merc_check = copy_clipboard()
            if int(merc_check):
                # print("Return int as Str later:", merc_check)
                break
        except ValueError:
            remove_stall_dialogs()
    return str(merc_check)


def update_clipboard(list_content):
    win32clipboard.OpenClipboard()
    time.sleep(0.2)
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(list_content)  # ICMS
    win32clipboard.CloseClipboard()


def clear_clipboard():
    win32clipboard.OpenClipboard()
    time.sleep(0.2)
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()


""" def check_if_merc_input():
    obj_click = pg.moveTo(x=537, y=321, duration=0.1)  # Merc coords
    time.sleep(0.2)
    pg.click(obj_click, clicks=2)
    try:
        merc_check = copy_clipboard()
        if int(merc_check):
            print("merc is here", merc_check)

    except ValueError:
        check_if_merc_input()

    return merc_check """


def call_next_note(coords):
    # obj_click = pg.moveTo(x=391, y=698, duration=0.1) #decrease coords
    # 362, 38
    # 540,705
    obj_click = pg.moveTo(x=coords[0] + 178, y=coords[1] + 667, duration=0.1)
    # Select Next Note on Synchro
    time.sleep(0.2)
    pg.click(obj_click)  # Calling next note on my application

    # this might be slowing things down!
    remove_stall_dialogs(0.01)


def call_next_merc(coords):
    # obj_click = pg.moveTo(x=coords[0] + 223, y=coords[1] + 542)
    obj_click = pg.moveTo(x=coords[0] + 173, y=coords[1] + 532, duration=0.1)
    time.sleep(0.1)
    pg.click(obj_click)
    remove_stall_dialogs(0.01)


def gravar_last_item():
    simulate_shortcut.get_key_comb("alt+g")


# This checks wether the selected merc on Synchro exists within the input list (json query)
def match_merc(input_list, coords):
    # this should've just eliminated comparissons, given it searches
    # input_list contains the current match_merc
    current_match = False
    selected_merc = merc_grab(coords)
    taxing_values = []
    for merc_v, icms, st in input_list:
        if merc_v == selected_merc:
            print(f"Merc from list: {merc_v} equals merc from Synchro: {selected_merc}")
            taxing_values.extend([icms, st])
            current_match = True

    return current_match, selected_merc, taxing_values


# This serves to validate merc field, if the caller return empty, this will handle it
# After all, Synchro is lovely with it`s delays right (irony)
def merc_catch_delay(check_value):
    condition_of = False
    try:
        if int(check_value):
            condition_of = True
    except ValueError:
        remove_stall_dialogs(0.01)
        pass
    # instead of repeating function call and destroying functionality, use pass
    return condition_of


def change_merc_items_unord(coords, merc_check, tax_values):
    print(coords, "Here it is")
    match_up = False
    print("Any sign of", merc_check)
    # Another source of slowdown
    if_merc_in = merc_catch_delay(merc_check)
    if if_merc_in == False:
        pass  # I believe this repeats until delay met
    else:
        if tax_values:  # if list empty, select next merc
            if tax_values[0] == "excluir" or tax_values[1] == "excluir":
                # Excluir BTN, x=750, y=539
                obj_click = pg.moveTo(
                    x=coords[0] + 430, y=coords[1] + 522, duration=0.1
                )
                time.sleep(0.1)
                pg.click(obj_click)
                time.sleep(0.2)
                # Excluir 684x441 (Sim); x= 775, y=441 (Não)
                simulate_shortcut.PressKey(VK_LEFT)
                """ obj_click = pg.moveTo(
                    x=coords[0] + 364, y=coords[1] + 424, duration=0.1
                ) """
                time.sleep(0.2)
                simulate_shortcut.PressKey(VK_RETURN)
                time.sleep(0.2)
                simulate_shortcut.PressKey(VK_RETURN)

            else:
                # Some trick to refresh values
                # x=795, y=457
                # ICMS Item
                obj_click = pg.moveTo(
                    x=coords[0] + 475, y=coords[1] + 440, duration=0.1
                )
                time.sleep(0.1)
                update_clipboard(tax_values[0])  # ICMS
                time.sleep(0.1)
                pg.tripleClick(obj_click)
                # Open clipboard and put here
                # synchro not supporting ctrl v
                simulate_shortcut.get_3key_comb("ctrl+shift+v")
                time.sleep(0.1)
                simulate_shortcut.PressKey(VK_DOWN)  # Down Key
                time.sleep(0.1)
                update_clipboard(tax_values[1])  # ST
                time.sleep(0.1)
                # synchro not supporting ctrl v
                simulate_shortcut.get_3key_comb("ctrl+shift+v")
                time.sleep(0.1)
                # x=602, y=549 # Next merc
                obj_click = pg.moveTo(
                    x=coords[0] + 176, y=coords[1] + 524, duration=0.1
                )
                # Going to next without resetting
                time.sleep(0.1)
                pg.click(obj_click)
                time.sleep(0.1)
                simulate_shortcut.single_Key(VK_RETURN)
                time.sleep(0.3)  # Because Synchro is slow.
            match_up = True
        else:  # this block needs proper fix
            match_up = False
            # Going to next without resetting
            # x=493, y=550
            obj_click = pg.moveTo(x=coords[0] + 173, y=coords[1] + 532, duration=0.1)
            # obj_click = pg.moveTo(x=coords[0] + 176, y=coords[1] + 524, duration=0.1)
            time.sleep(0.1)
            pg.click(obj_click)
            # This stalls the code significantly.
            # remove_stall_dialogs(0.01)

    return match_up


def change_merc_items(coords, tax_values, merc_compare):
    match_up = False
    merc_check = merc_grab(coords)
    if merc_check == merc_compare:  # TODO: try except error symbol.
        if tax_values[0] == "excluir" or tax_values[1] == "excluir":
            # Excluir BTN, x=750, y=539
            obj_click = pg.moveTo(x=coords[0] + 430, y=coords[1] + 522, duration=0.1)
            time.sleep(0.1)
            pg.click(obj_click)
            # Excluir 684x441 (Sim); x= 775, y=441 (Não)
            obj_click = pg.moveTo(x=coords[0] + 364, y=coords[1] + 424, duration=0.1)
            time.sleep(0.2)
            pg.click(obj_click)  # rightClick
            time.sleep(0.3)
            simulate_shortcut.PressKey(VK_RETURN)

        else:
            # Some trick to refresh values
            # x=795, y=457
            # ICMS Item
            obj_click = pg.moveTo(x=coords[0] + 475, y=coords[1] + 440, duration=0.1)
            time.sleep(0.1)
            update_clipboard(tax_values[0])  # ICMS
            time.sleep(0.1)
            pg.tripleClick(obj_click)
            # Open clipboard and put here
            # synchro not supporting ctrl v
            simulate_shortcut.get_3key_comb("ctrl+shift+v")
            time.sleep(0.1)
            simulate_shortcut.PressKey(VK_DOWN)  # Down Key
            time.sleep(0.1)
            update_clipboard(tax_values[1])  # ST
            time.sleep(0.1)
            # synchro not supporting ctrl v
            simulate_shortcut.get_3key_comb("ctrl+shift+v")
            time.sleep(0.1)
            # x=492, y=549 # Next merc item(?)
            obj_click = pg.moveTo(x=coords[0] + 172, y=coords[1] + 52, duration=0.1)
            # Going to next without resetting
            time.sleep(0.1)
            pg.click(obj_click)
            time.sleep(0.1)
            simulate_shortcut.single_Key(VK_RETURN)
            time.sleep(0.3)  # Because Synchro is slow.
        match_up = True
    else:
        match_up = False
        # Going to next without resetting
        # x=493, y=550
        obj_click = pg.moveTo(x=coords[0] + 173, y=coords[1] + 532, duration=0.1)
        time.sleep(0.1)
        pg.click(obj_click)
    return match_up


def update_coords():
    nav, coords = locate_img_new(
        img_gather=synchro_win_header, click_it=False, pausefloat=0.2
    )
    print(nav, coords)
    return nav, coords


""" window_restore()

_, coords = update_coords()
obj_click = pg.moveTo(x=coords[0] + 173, y=coords[1] + 532, duration=0.1)
time.sleep(0.1)
pg.click(obj_click)
time.sleep(0.2) """
# remove_stall_dialogs(0.01)

# the execute cce have a class for this initial compare
# Append from three fields on a list of three
