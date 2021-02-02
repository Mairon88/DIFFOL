#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkcalendar import *
import logic


# TWORZENIE GŁOWNEGO OKNA

root = Tk()
root.title(">>> DIFFOL <<<")
height = 600
width = 545
notebook = ttk.Notebook(root)
notebook.grid(column=0, row=0)

# TWORZENIE ZAKŁADEK
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text='GŁÓWNE OKNO', )
frame2 = ttk.Frame(notebook)
notebook.add(frame2, text='USTAWIENIA')
frame3 = ttk.Frame(notebook)
notebook.add(frame3, text='POMOC')

# ZDEFINIOWANIE PARAMETRÓW OKNA PROGRAMU
root.geometry(f"{width}x{height}")
root.minsize(width, height)
root.maxsize(width, height)
root.option_add('*tearOff', False)

# RAMKA DLA KALENDARZA
frame_calendars = ttk.LabelFrame(frame1, text="Wybierz zakres dat w jakim chcesz porównać foldery")
frame_calendars.grid(column=0, row=0, pady=10, padx=10)
frame_calendars.config(height=100, width=525)

# TWORZENIE DWÓCH KALENDARZY DO WYBORU DATY POCZATKOWEJ I KONCOWEJ
# USTAWIANIE DATY POCZĄTKOWEJ
text_cal_1 = Label(frame_calendars, text="DATA POCZĄTKOWA")
text_cal_1.grid(column=0, row=0, pady=10, padx=35)
cal_1 = DateEntry(frame_calendars, width=12, background='darkblue', foreground='white', borderwidth=2,
                  date_pattern='y-mm-dd')
cal_1.grid(column=1, row=0, pady=10, padx=10)

# USTAWIANIE DATY KOŃCOWEJ
text_cal_2 = Label(frame_calendars, text="DATA KOŃCOWA")
text_cal_2.grid(column=0, row=1, pady=10, padx=35)
cal_2 = DateEntry(frame_calendars, width=12, background='darkblue', foreground='white', borderwidth=2,
                  date_pattern='y-mm-dd')
cal_2.grid(column=1, row=1, pady=10, padx=10)
3
# RAMKA DLA PRZYCISKÓW
frame_buttons = ttk.LabelFrame(frame1, text="Sprawdź różnice w folderach, zapisz raport z wynikami "
                                            "lub wyjdź z programu")
frame_buttons.grid(column=0, row=1, pady=10, padx=10)
frame_buttons.config(height=100, width=525)

# UTWORZENIE GŁÓWNYCH PRZYCISKÓW
main_batton_start = ttk.Button(frame_buttons, text="PORÓWNAJ FOLDERY")
# command=lambda : dif.CheckFile.checking_file(list_of_paths, frame_infos))
main_batton_start.grid(column=0, row=0, padx=18, pady=10)
main_batton_raport = ttk.Button(frame_buttons, text="ZAPISZ RAPORT")
# command=lambda : dif.CheckFile.print_raport(list_of_paths))
main_batton_raport.grid(column=1, row=0, padx=18, pady=10)
main_batton_exit = ttk.Button(frame_buttons, text="WYJDŹ Z PROGRAMU", command=root.quit)
main_batton_exit.grid(column=2, row=0, padx=18, pady=10)
# main_batton_save = ttk.Button(frame_paths, text="ZAPISZ USTAWIENIA",
# command=lambda : dif.MyPath.save_settings(list_of_paths))
# main_batton_save.grid(column = 0, row= 14)

# RAMKA DLA WYŚWIETLANIA INFORMACJI O SPÓJNOŚCI FOLDEÓRW
frame_infos = ttk.LabelFrame(frame1, text="Status spójności folderów")
frame_infos.grid(column=0, row=2, pady=10, padx=10)
frame_infos.config(height=200, width=525)

# UTWORZENIE SPISU PAR FOLDERÓW
# LISTY PRZECHOWUJĄCE ETYKIETY DLA PAR FOLDERÓW I STATUSY

pair_of_paths = []
dif_status = []

for i in range(4):
    pair_of_paths.append(Label(frame_infos, text=f"FOLDERY {i+1}A-{i+1}B"))
    pair_of_paths[i].grid(column=0, row=i, pady=10, padx=10)
    dif_status.append(Label(frame_infos, text="-"))
    dif_status[i].grid(column=1, row=i, pady=10, padx=10)

# RAMKA DLA WYŚWIETLANIA INFORMACJI O RAPORCIE
frame_raport = ttk.LabelFrame(frame1, text="Informacja o raporcie")
frame_raport.grid(column=0, row=3,  pady=10, padx=10)
frame_raport.config(height=120, width=525)

# WYDRUK INFORMACJI O PLIKU RAPORTU I ŚCIEŻCE W KTÓREJ ZOSTAŁ UTWORZONY
raport_info_1 = Label(frame_raport, text="Nazwa pliku: raport_file_01-02-2021_12-47-39.txt")
raport_info_1.grid(column=0, row=0)
raport_info_2 = Label(frame_raport, text="Ścieżka: /home/mariusz/PycharmProjects/DIFFOL/venv/bin/python "
                                         "/home/mariusz/PycharmProjects/DIFFOL/main.py", wraplength=500)
raport_info_2.grid(column=0, row=1)







root.mainloop()
