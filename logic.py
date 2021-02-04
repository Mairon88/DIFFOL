from tkinter import *
from tkinter import ttk
from tkcalendar import *
from tkinter import filedialog
import datetime, os, stat

# KLASA ODPOWIADAJĄCA ZA WCZYTYWANIE ŚCIEŻEK ORAZ FORMATÓW, ZAPIS USTAWIEŃ DO PLIKU I ICH ODCZYT Z PLIKU


class MyPath(object):
    pos_col = 0
    pos_row = 0
    num_of_paths = 1

    def __init__(self, frame_paths):

        self.frame_path_formats = ttk.LabelFrame(frame_paths,
                                                 text=f"Ścieżki {MyPath.num_of_paths}A-{MyPath.num_of_paths}B")
        self.frame_path_formats.grid(column=0, row=MyPath.pos_row)

        self.my_entry1 = ttk.Entry(self.frame_path_formats, text="", width=20)
        self.my_entry1.grid(column=1, row=0, padx=20)
        self.my_entry2 = ttk.Entry(self.frame_path_formats, text="", width=20)
        self.my_entry2.grid(column=2, row=0, padx=20)
        self.my_entry3 = ttk.Entry(self.frame_path_formats, text="", width=20)
        self.my_entry3.grid(column=2, row=3, pady=10, padx=20)

        self.path_A = ""
        self.path_B = ""

        self.my_button1 = ttk.Button(self.frame_path_formats, text="Wskaż ścieżkę A",
                                     command=lambda: self.set_path("A"))
        self.my_button1.grid(column=1, row=1, padx=20)
        self.my_button2 = ttk.Button(self.frame_path_formats, text="Wskaż ścieżkę B",
                                     command=lambda: self.set_path("B"))
        self.my_button2.grid(column=2, row=1, padx=20)

        self.frame_formats = ttk.Frame(self.frame_path_formats)
        self.frame_formats.grid(column=0, row=2, columnspan=4)

        self.my_label = ttk.Label(self.frame_path_formats, text="Podaj rozszerzenia plków po przecinku, bez spacji i"
                                                                   " kropki. Np. txt,docx,pdf,xlsx -->", wraplength=300)
        self.my_label.grid(column=0, row=3, pady=10, padx=20, columnspan=2)

        MyPath.pos_row += 3
        MyPath.num_of_paths += 1

    # POZWALA NA WYBRANIE ŚCIEŻKI FOLDERU PRZY POMOCY PRZYCISKU "WSKAŻ ŚCIEŻKĘ"
    # USTAWIA NAZWĘ ŚCIEŻKI W POLU ENTRY
    def set_path(self, opt):
        path = filedialog.askdirectory()
        if opt == "A":
            self.my_entry1.delete(0, "end")
            self.my_entry1.insert(0, path)
            self.path_A = path

        else:
            self.my_entry2.delete(0,"end")
            self.my_entry2.insert(0, path)
            self.path_B = path

    # ZAPISUJE USTAWIENIA DO PLIKU TXT
    @staticmethod
    def save_settings(list_with_path):

        print("Zapisuje ustawienia")
        with open("setting_file.txt", 'w') as outfile:
            for obj in list_with_path:
                outfile.write(obj.my_entry1.get()+"\n")
                outfile.write(obj.my_entry2.get()+"\n")
                outfile.write(obj.my_entry3.get()+"\n")

    # WCZYTUJE USTAWIENIA
    @staticmethod
    def load_settings(list_with_path):
        number = 0
        print("Wczytuje ustawienia")

        try:
            with open("setting_file.txt", 'r') as infile:
                lines = infile.readlines()
            for obj in list_with_path:
                obj.my_entry1.delete(0, "end")
                obj.my_entry1.insert(0, lines[number].rstrip("\n"))
                obj.my_entry2.delete(0, "end")
                obj.my_entry2.insert(0, lines[number+1].rstrip("\n"))
                obj.my_entry3.delete(0, "end")
                obj.my_entry3.insert(0, lines[number+2].rstrip("\n"))
                number += 3
        except:
            print("Brak w folderze z programem pliku z ustawieniami setting_file.txt")


class CheckFile(object):
    def __init__(self, list_of_paths, start_date, end_date):
        self.list_of_paths = list_of_paths
        self.start_date = start_date
        self.end_date = end_date

    def differ(self):
        for path in self.list_of_paths:
            path_1 = path.my_entry1.get()
            path_2 = path.my_entry2.get()

            if (path_1 != "") & (path_2 != ""):
                try:
                    files_a = CheckFile.filtered_files(path_1, self.start_date, self.end_date)
                    files_b = CheckFile.filtered_files(path_2, self.start_date, self.end_date)

                except BaseException as e:
                    print("Błąd: ",e)


    @staticmethod
    def filtered_files(path, data_1, data_2):

        for file in os.listdir(path):
            file_date = str(datetime.datetime.fromtimestamp(os.stat(os.path.join(path, file))[stat.ST_MTIME]))
            if str(data_1) <= file_date[:10] <= str(data_2):
                yield (file, file_date)


class Raport():
    def __init__(self):
        pass

    @staticmethod
    def save_raport(path):
        pass