import tkinter as tk
import sqlite3
from data_managment import calendar
from tkinter import font

class EuFixtureScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=self.master.background)
        for i in range(1):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.columnconfigure(i, weight=1, uniform="equal") #kolumny

        self.selected_club_label = tk.Label(self, text="", height=2, font=font.Font(size=26, weight='bold'))
        self.selected_club_label.grid(row=0, column=0, sticky="nsew")
        self.selected_club_label.bind("<Button-1>", lambda e:self.master.switch_to_club_interface())
        # Zmiana kursora
        self.selected_club_label.bind("<Enter>", self.master.on_enter)
        self.selected_club_label.bind("<Leave>", self.master.on_leave)
        self.buttons_frame = tk.Frame(self, background=self.master.label_default)
        self.buttons_frame.grid(row=1, column=0, sticky="nsew")
        for i in range(5):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.buttons_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny
        # Zmień na wyższą ligę
        self.higher_button = tk.Button(self.buttons_frame, text="< Previous gameweek", command=self.show_prev_gameweek, bg=self.master.button_bg, fg=self.master.highlights)
        self.higher_button.grid(row=0, column=0, pady=20, sticky="nsew", padx=20)

        # Zmień na niższą ligę
        self.lower_button = tk.Button(self.buttons_frame, text="Next gameweek >", command=self.show_next_gameweek, bg=self.master.button_bg, fg=self.master.highlights)
        self.lower_button.grid(row=0, column=4, pady=20, sticky="nsew", padx=20)
        # Zmień na tabelę
        self.table_button = tk.Button(self.buttons_frame, text="Table", command=self.master.switch_to_eu_table_interface, bg=self.master.button_bg, fg=self.master.highlights)
        self.table_button.grid(row=0, column=1, pady=20, sticky="nsew", padx=20)
        # Zmień na terminarz
        self.fixture_button = tk.Button(self.buttons_frame, text="Fixture", bg=self.master.button_bg, fg=self.master.highlights)
        self.fixture_button.grid(row=0, column=2, pady=20, sticky="nsew", padx=20)
        # Zmień na historię
        self.history_button = tk.Button(self.buttons_frame, text="Winners", command=self.master.switch_to_eu_winners_interface, bg=self.master.button_bg, fg=self.master.highlights)
        self.history_button.grid(row=0, column=3, pady=20, sticky="nsew", padx=20)

        # Wyświetl terminarz
        self.fixture_frame = tk.Frame(self, background=self.master.label_default)
        self.fixture_frame.grid(row=2, column=0, sticky="nsew")

    def show(self):
        self.selected_club_label.config(text=f"{self.master.selected_club}")
        self.selected_club_label.config(background=self.master.colors[0])
        self.selected_club_label.config(foreground=self.master.colors[1])

        self.gameweek_to_show = self.check_gameweek()
        self.last_gameweek_to_show = self.get_no_of_games()

        self.display_fixture()

        self.pack(expand=True, fill="both")

    def check_gameweek(self):
        check = self.master.gameweek
        while check > 0 and calendar[check][0] != "EU":
            check -= 1
        if check == 0:
            return 1
        else:
            return calendar[check][1]

    def show_next_gameweek(self):
        if self.gameweek_to_show < self.last_gameweek_to_show:
            self.gameweek_to_show += 1
            self.display_fixture()
            if self.gameweek_to_show == self.last_gameweek_to_show:
                self.lower_button.config(state=tk.DISABLED)

    def show_prev_gameweek(self):
        if self.gameweek_to_show > 1:
            self.gameweek_to_show -= 1
            self.display_fixture()
            if self.gameweek_to_show == 1:
                self.higher_button.config(state=tk.DISABLED)

    def display_fixture(self):
        if self.gameweek_to_show > self.last_gameweek_to_show:
            self.gameweek_to_show = self.last_gameweek_to_show

        if self.last_gameweek_to_show == 1:
            self.higher_button.config(state=tk.DISABLED)
            self.lower_button.config(state=tk.DISABLED)
        elif self.gameweek_to_show == 1:
            self.higher_button.config(state=tk.DISABLED)
            self.lower_button.config(state=tk.NORMAL)
        elif self.gameweek_to_show == self.last_gameweek_to_show:
            self.lower_button.config(state=tk.DISABLED)
            self.higher_button.config(state=tk.NORMAL)
        else:
            self.lower_button.config(state=tk.NORMAL)
            self.higher_button.config(state=tk.NORMAL)


        fixture = self.get_matches()
        grid_index = 1
        # Wyczyść listę i dodaj druzyny do tabeli
        for widget in self.fixture_frame.winfo_children():
            widget.destroy()
        self.fixture_no_label = tk.Label(self.fixture_frame, text=f"Gameweek {self.gameweek_to_show}", font=font.Font(size=18, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.fixture_no_label.grid(row=0, column=0, sticky='nswe', pady=(5, 20), columnspan=8)

        for match in fixture:
            self.home_label = tk.Label(self.fixture_frame, text=f"{match[0]}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.my_team_highlight if match[0] == self.master.selected_club else self.master.highlights)
            self.home_label.grid(row=grid_index, column=0, sticky='nswe')
            self.score_label = tk.Label(self.fixture_frame, text=f"{match[2]}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.score_label.grid(row=grid_index, column=1, sticky='nswe')
            self.away_label = tk.Label(self.fixture_frame, text=f"{match[1]}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.my_team_highlight if match[1] == self.master.selected_club else self.master.highlights)
            self.away_label.grid(row=grid_index, column=2, sticky='nswe')
            grid_index += 1
        for i in range(3):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.fixture_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

    def get_no_of_games(self):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Wykonujemy zapytanie, aby wyświetlić dane z konkretnej tabeli (np. druzyny)
        cursor.execute("""
            SELECT MAX(kolejka) FROM mecze WHERE poziom_rozgrywkowy = ? AND rozgrywki = 'EU'
        """, (self.master.current_selected_league_eu,))

        games = cursor.fetchone()[0]

        # Zamykamy połączenie
        conn.close()

        return games

    def get_matches(self):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Wykonujemy zapytanie, aby wyświetlić dane z konkretnej tabeli (np. druzyny)
        cursor.execute("""
            SELECT druzyna_gospodarza, druzyna_gosci, wynik
            FROM mecze
            WHERE kolejka = ? and poziom_rozgrywkowy = ? and rozgrywki = 'EU'
        """, (self.gameweek_to_show, self.master.current_selected_league_eu,))

        fixture = cursor.fetchall()

        # Zamykamy połączenie
        conn.close()

        return fixture

    def hide(self):
        self.pack_forget()