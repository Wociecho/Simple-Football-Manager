import tkinter as tk
from tkinter import ttk, font
import sqlite3
from data_managment import start_new_game

class ClubSelectionFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=self.master.background)
        self.data_loaded = False
        for i in range(1):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.columnconfigure(i, weight=1, uniform="equal") #kolumny

        self.data_frame = tk.Frame(self, background=self.master.label_default, highlightbackground=self.master.highlights, highlightthickness=2)
        self.data_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20,)

        for i in range(2):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.data_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

        # Wybór kraju
        # Pobieramy ilość poziomów rozgrywek z bazy danych
        self.available_nations = self.get_nations()

        # Zmienna do przechowywania wybranego klubu
        self.selected_nation = tk.StringVar()

        # Etykieta informacyjna
        label_kraj = tk.Label(self.data_frame, text="Pick country:", font=font.Font(size=20, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        label_kraj.grid(row=0, column=0, sticky="nsew", pady=20, padx=20)

        # Menu rozwijane z ligami
        self.nation_menu = ttk.Combobox(self.data_frame, textvariable=self.selected_nation, values=self.available_nations, state="readonly", font=font.Font(size=20))
        self.nation_menu.grid(row=0, column=1, sticky="nsew", pady=20, padx=20)

        self.nation_menu.bind("<<ComboboxSelected>>", self.on_nation_selected)

        # Wybór ligi
        # Pobieramy ilość poziomów rozgrywek z bazy danych
        self.available_leagues = ""

        # Zmienna do przechowywania wybranego klubu
        self.selected_league = tk.StringVar()

        # Etykieta informacyjna
        label_liga = tk.Label(self.data_frame, text="Pick league level:", font=font.Font(size=20, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        label_liga.grid(row=1, column=0, sticky="nsew", pady=20, padx=20)

        # Menu rozwijane z ligami
        self.league_menu = ttk.Combobox(self.data_frame, textvariable=self.selected_league, values=self.available_leagues, state="readonly", font=font.Font(size=20))
        self.league_menu.grid(row=1, column=1, sticky="nsew", pady=20, padx=20)

        self.league_menu.bind("<<ComboboxSelected>>", self.on_league_selected)

        # Wybór klubu
        # Pobieramy nazwy klubów z bazy danych
        self.available_clubs = ""

        # Zmienna do przechowywania wybranego klubu
        self.selected_club = tk.StringVar()

        # Etykieta informacyjna
        label = tk.Label(self.data_frame, text="Pick club:", font=font.Font(size=20, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        label.grid(row=2, column=0, sticky="nsew", pady=20, padx=20)

        # Menu rozwijane z klubami
        self.club_menu = ttk.Combobox(self.data_frame, textvariable=self.selected_club, values=self.available_clubs, state="readonly", font=font.Font(size=20))
        self.club_menu.grid(row=2, column=1, sticky="nsew", pady=20, padx=20)

        self.club_menu.bind("<<ComboboxSelected>>", self.on_club_selected)

        # Przycisk do potwierdzenia wyboru klubu
        confirm_button = tk.Button(self.data_frame, text="Confirm", command=self.confirm_selection, font=font.Font(size=20, weight='bold'))
        confirm_button.grid(row=3, column=0, sticky="nsew", columnspan=2, pady=20, padx=20)

        self.clubframe = tk.Frame(self, highlightbackground=self.master.highlights, highlightthickness=2, background=self.master.label_default)
        self.clubframe.grid(row=4, column=0, padx=20, pady=20, columnspan=2, sticky="nsew")
        for i in range(4):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.clubframe.columnconfigure(i, weight=1, uniform="equal") #kolumny

    def confirm_selection(self):
        selected_league = self.selected_league.get()
        selected_club = self.selected_club.get()
        if selected_club and selected_league:
            selected_league = int(selected_league)
            self.master.set_user_club(selected_club, selected_league)
            # Przełącz na ekran z interfejsem klubu
            self.master.switch_to_club_interface()

    def show(self):
        start_new_game()
        self.available_nations = self.get_nations()
        self.nation_menu["values"] = self.available_nations
        self.pack(expand=True, fill="both")

    def hide(self):
        self.pack_forget()

    def get_club_names(self, poziom_rozgrywkowy):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Pobieramy nazwy klubów z bazy danych
        cursor.execute("SELECT nazwa FROM druzyny WHERE poziom_rozgrywkowy = ? ORDER BY nazwa ASC", (poziom_rozgrywkowy,))
        clubs = cursor.fetchall()

        # Zamykamy połączenie z bazą danych
        conn.close()

        return [club[0] for club in clubs]
    
    def get_leagues(self, nation):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Pobieramy nazwy klubów z bazy danych
        cursor.execute("SELECT DISTINCT poziom_rozgrywkowy FROM druzyny WHERE kraj = ? ORDER BY poziom_rozgrywkowy ASC", (nation,))
        leagues = cursor.fetchall()

        # Zamykamy połączenie z bazą danych
        conn.close()

        return [league[0] for league in leagues]
    
    def get_nations(self):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Pobieramy nazwy krajów z tabeli ligi
        cursor.execute("SELECT DISTINCT kraj FROM ligi ORDER BY kraj ASC")
        nations = cursor.fetchall()

        # Zamykamy połączenie z bazą danych
        conn.close()

        return [nation[0] for nation in nations]
    
    def on_league_selected(self, event):
        selected_league = self.selected_league.get()
        self.available_clubs = self.get_club_names(selected_league)
        self.club_menu["values"] = self.available_clubs

    def on_nation_selected(self, event):
        selected_nation = self.selected_nation.get()
        self.available_leagues = self.get_leagues(selected_nation)
        self.league_menu["values"] = self.available_leagues

    def on_club_selected(self, event):
        selected_club = self.selected_club.get()
        if selected_club:
            self.fill_club_info()

    def fill_club_info(self):
        # Pobieramy informacje o przeciwniku
        data = self.get_club_info(self.selected_club.get())
        # Wyczyść listę i dodaj mecze
        for widget in self.clubframe.winfo_children():
            widget.destroy()
        # 0nazwa, 1sila_bramkarza, 2sila_obrony, 3sila_pomocy, 4sila_napadu, 5bg_color, 6fg_color     
        if data:
            self.name_label = tk.Label(self.clubframe, text=f"{data[0]}", font=font.Font(size=13, weight='bold'), background=f'{data[5]}', fg=f'{data[6]}')
            self.name_label.grid(row=0, column=0, pady=5, padx=10, columnspan=4, sticky="nsew")

            self.gk_label = tk.Label(self.clubframe, text=f"GK", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.gk_label.grid(row=1, column=0, pady=5, padx=10)
            self.d_label = tk.Label(self.clubframe, text=f"DEF", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.d_label.grid(row=1, column=1, pady=5, padx=10)
            self.m_label = tk.Label(self.clubframe, text=f"MID", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.m_label.grid(row=1, column=2, pady=5, padx=10)
            self.a_label = tk.Label(self.clubframe, text=f"ATT", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.a_label.grid(row=1, column=3, pady=5, padx=10)
            self.gk_label = tk.Label(self.clubframe, text=f"{data[1]}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.gk_label.grid(row=2, column=0, pady=5, padx=10)
            self.d_label = tk.Label(self.clubframe, text=f"{data[2]}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.d_label.grid(row=2, column=1, pady=5, padx=10)
            self.m_label = tk.Label(self.clubframe, text=f"{data[3]}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.m_label.grid(row=2, column=2, pady=5, padx=10)
            self.a_label = tk.Label(self.clubframe, text=f"{data[4]}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.a_label.grid(row=2, column=3, pady=5, padx=10)

    def get_club_info(self, club_name):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nazwa, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, bg_color, fg_color
            FROM druzyny
            WHERE nazwa=?
        """, (club_name,))

        data = cursor.fetchone()

        # Zamykamy połączenie z bazą danych
        conn.close()

        return data