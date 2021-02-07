from tkinter import ttk
from tkinter import filedialog
import datetime
import os
import stat
from anything import Anything as any


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
                                                                "kropki. Np. txt,docx,pdf,xlsx -->", wraplength=300)
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
            self.my_entry2.delete(0, "end")
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
    data_for_report = {}

    def __init__(self, list_of_paths, start_date, end_date):
        self.list_of_paths = list_of_paths
        self.start_date = start_date
        self.end_date = end_date
        CheckFile.data_for_report = {}

    def differ(self, dif_status):
        # DLA KAŻDEGO OBIEKTU Z ŚCIEŻKAMI POBIERA ŚCIEZKI I FORMATY
        number = 0

        for path in self.list_of_paths:
            path_1 = path.my_entry1.get()
            path_2 = path.my_entry2.get()
            format_set = path.my_entry3.get()

            if (path_1 != "") & (path_2 != ""):
                try:
                    # NA PODSTAWIE DAT, SCIEZEK I FORMATOW FILTRUJE PLIKI DLA SANYCH SCIEZEK I PRZECHOWUJE JAKO ZBIÓR
                    # TUPLI
                    files_a = set(CheckFile.filtered_files(path_1, self.start_date, self.end_date, format_set))
                    files_b = set(CheckFile.filtered_files(path_2, self.start_date, self.end_date, format_set))

                    # ROZNICA ZBIOROW ZWRACA ZBIOR PLIKOW Z PIERWSZEGO FOLDERU KTORE ROZNIA W DRUGIM FOLDERZE
                    files_dif_a_b = list(files_a-files_b)
                    files_dif_b_a = list(files_b-files_a)

                    if set(files_dif_a_b) != set() or set(files_dif_b_a) != set():
                        dif_status[number].config(text='X')

                    else:
                        dif_status[number].config(text='V')

                    # LISTY POMOCNOCZE DO SPRAWDZENIA CZY ELEMENT Z ROZNICY WYNIKA Z BRAKU PLIKU CZY Z MODYFIKACJI
                    # SPRAWDZENIE ODBYWA SIE NA PODSTAWIE PIERWSZEGO ELEMENTU Z TUPLI CZYLI PO NAZWIE
                    exist_check_list_a = [file[0] for file in files_a]
                    exist_check_list_b = [file[0] for file in files_b]

                    CheckFile.prepare_to_raport(number, path_1, path_2, files_b, files_dif_a_b, exist_check_list_b, 1)
                    CheckFile.prepare_to_raport(number, path_2, path_1, files_a, files_dif_b_a, exist_check_list_a, 2)

                except BaseException as e:
                    print("Błąd: ", e)
            else:
                dif_status[number].config(text='-')

            number += 1

    @staticmethod
    def filtered_files(path, data_1, data_2, format_set):
        # DLA KAŻDEGO PLIKU SPRADZA JEGO FORMAT I DATE UTWORZENIA
        for file in os.listdir(path):
            file_format = file[str(file).index(".")+1:]
            file_date = str(datetime.datetime.fromtimestamp(os.stat(os.path.join(path, file))[stat.ST_MTIME]))

            # SRPAWDZENIE CZY PLIK ZNAJDUJE SIE W ZAKRESIE DAT I CZY MA ODPOWIEDNIE ROZSZERZENIE
            if format_set.split(",") != ['']:
                if (str(data_1) <= file_date[:10] <= str(data_2)) and file_format in format_set:
                    yield file, file_date
            # SPRAWDZA TYLKO ZAKRES DAT
            else:
                if str(data_1) <= file_date[:10] <= str(data_2):
                    yield file, file_date

    @staticmethod
    def prepare_to_raport(number, path_1, path_2, files, files_dif, check_list, num_of_path):
        # SPRAWDZANIE CZY PLIK Z ZBIORU ROZNIC ZNAJDUJE SIE W PLIKACH DRUGIEGO FOLDERU
        # JEŚLI TAK TO ZNACZY ZE ROZNIA SIE DATA A JESLI GO NIE MA TO ZNACZY ZE BRAKUJE TAKIEGO PLIKU
        # WYKORZYSTANO MODUL ANYTHING DO SPRAWDZENIA INDEKSU TUPLI ZNAJAC TYLKO NAZWĘ DZIEKI CZEMU MOZNA UZySKAC PEŁNE
        # DANE O NAZWIE I DACIE

        lista_of_file_pairs = []

        for file_dif in files_dif:

            if file_dif[0] in check_list:
                if num_of_path == 1:
                    files = list(files)
                    # SPRAWDZENIE INDEKSU TUPLI W LIŚCIE ZNAJAC TYLKO PIERWSZY ELEMENT TUPLI
                    # W DRUGĄ STRONE NIE ROBIMY TEGO SPRAWDZENIA BO BY SIĘ DUBLOWAŁ WYNIK
                    index = files.index((file_dif[0], any))
                    lista_of_file_pairs.append((file_dif, files[index]))

            else:
                if num_of_path == 1:
                    lista_of_file_pairs.append((file_dif, ('-', '-')))
                else:
                    lista_of_file_pairs.append((('-', '-'), file_dif))

        CheckFile.data_for_report.setdefault((number, path_1, path_2), lista_of_file_pairs)


class Report(object):
    def __init__(self):
        pass

    @staticmethod
    def save_raport(data, start_date, end_date):

        now = datetime.datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
        report_name = "report_file_"+str(dt_string)+".txt"

        def comment(file_name):
            if file_name == '-':
                return "BRAK PLIKU W TEJ ŚCIEŻCE"
            else:
                return ""

        def string_cut(file_name):
            if len(file_name) > 40:
                return file_name[:15] + "..." + file_name[-18:]
            else:
                return file_name

        with open(report_name, 'w', encoding="utf-8") as outfile:
            outfile.write("ZAKRES DAT: ")
            outfile.write((str(start_date)+" --> "+str(end_date)))

            num = 1
            for k, v in data.items():

                file_name_a = v[0][0][0]
                date_file_a = v[0][0][1]

                file_name_b = v[0][1][0]
                date_file_b = v[0][1][1]

                if num % 2 != 0:

                    outfile.write("\n\nŚCIEŻKA {}A {}".format(k[0] + 1, k[1]))
                    outfile.write("\nŚCIEŻKA {}B {}\n".format(k[0] + 1, k[2]))
                    outfile.write('\n\n{:^5} {:^40} {:^30} {:^30}\n'.format('LP.', 'NAZWA PLIKU', 'DATA PLIKU',
                                                                            'UWAGA'))
                    outfile.write("-" * 108)
                    num = 1

                if file_name_a != '-' and file_name_b != '-':
                    comment_1 = "RÓŻNICA W DATACH ZAPISU PLIKU"
                    comment_2 = ""
                else:
                    comment_1 = comment(file_name_a)
                    comment_2 = comment(file_name_b)

                outfile.write('\n{:^5} {:^40} {:^30} {:^30}'.format(num, string_cut(file_name_a), date_file_a,
                                                                    comment_1))
                outfile.write('\n{:^5} {:^40} {:^30} {:^30}\n'.format('', string_cut(file_name_b), date_file_b,
                                                                      comment_2))
                outfile.write("-" * 108)

                num += 1
