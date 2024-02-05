import tkinter as tk
import sqlite3
from data_managment import calendar
from tkinter import font

class CupScreen(tk.Frame):
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
        self.higher_button = tk.Button(self.buttons_frame, text="<", command=self.master.switch_to_eu_table_interface, bg=self.master.button_bg, fg=self.master.highlights)
        self.higher_button.grid(row=0, column=0, pady=20, sticky="nsew", padx=20)

        # Zmień na niższą ligę
        self.lower_button = tk.Button(self.buttons_frame, text=">", command=self.master.switch_to_table_interface, bg=self.master.button_bg, fg=self.master.highlights)
        self.lower_button.grid(row=0, column=4, pady=20, sticky="nsew", padx=20)
        # Poprzednia runda
        self.prev_button = tk.Button(self.buttons_frame, text="< Previous round", command=self.show_prev_round, bg=self.master.button_bg, fg=self.master.highlights)
        self.prev_button.grid(row=0, column=1, pady=20, sticky="nsew", padx=20)
        # Następna runda
        self.next_button = tk.Button(self.buttons_frame, text="Next round >", command=self.show_next_round, bg=self.master.button_bg, fg=self.master.highlights)
        self.next_button.grid(row=0, column=2, pady=20, sticky="nsew", padx=20)
        # Zmień na historię
        self.history_button = tk.Button(self.buttons_frame, text="Winners", command=self.master.switch_to_cup_winners_interface, bg=self.master.button_bg, fg=self.master.highlights)
        self.history_button.grid(row=0, column=3, pady=20, sticky="nsew", padx=20)

    def show(self):
        self.selected_club_label.config(text=f"{self.master.selected_club}")
        self.selected_club_label.config(background=self.master.colors[0])
        self.selected_club_label.config(foreground=self.master.colors[1])

        self.gameweek_to_show = self.check_gameweek()
        self.last_gameweek_to_show = self.gameweek_to_show

        self.create_widgets()

        self.pack(expand=True, fill="both")

    def create_widgets(self):
        self.fixture_frame = self.master.scrollable_frame(self, background=self.master.label_default)
        self.fixture_frame.grid(row=3, column=0, sticky="nsew")

        self.display_fixture()

    def check_gameweek(self):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        # Wykonanie zapytania SQL, aby znaleźć największą wartość w kolumnie
        cursor.execute("SELECT MAX(cup_round) FROM druzyny")

        # Pobranie wyniku zapytania
        curr_cup_round = cursor.fetchone()[0]

        conn.close()

        if curr_cup_round > 7:
            curr_cup_round = 7
        elif curr_cup_round == 2:
            if self.master.gameweek <= 5:
                curr_cup_round = 1

        return curr_cup_round

    def show_next_round(self):
        if self.gameweek_to_show < self.last_gameweek_to_show:
            self.gameweek_to_show += 1
            self.display_fixture()
            if self.gameweek_to_show == self.last_gameweek_to_show:
                self.next_button.config(state=tk.DISABLED)

    def show_prev_round(self):
        if self.gameweek_to_show > 1:
            self.gameweek_to_show -= 1
            self.display_fixture()
            if self.gameweek_to_show == 1:
                self.prev_button.config(state=tk.DISABLED)

    def display_fixture(self):
        if self.gameweek_to_show > self.last_gameweek_to_show:
            self.gameweek_to_show = self.last_gameweek_to_show

        if self.gameweek_to_show == 1:
            self.prev_button.config(state=tk.DISABLED)
            if self.last_gameweek_to_show == 1:
                self.next_button.config(state=tk.DISABLED)
            else:
                self.next_button.config(state=tk.NORMAL)
        elif self.gameweek_to_show == self.last_gameweek_to_show:
            self.next_button.config(state=tk.DISABLED)
            self.prev_button.config(state=tk.NORMAL)
        else:
            self.prev_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.NORMAL)


        fixture = self.get_matches()
        grid_index = 1

        self.fixture_no_label = tk.Label(self, text=f"{'Final' if self.gameweek_to_show == 7 else 'Round '}{self.gameweek_to_show if self.gameweek_to_show < 7 else ''}", font=font.Font(size=21, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.fixture_no_label.grid(row=2, column=0, sticky='nswe')

        # Wyczyść listę i dodaj druzyny do tabeli
        for widget in self.fixture_frame.scrollable_frame.winfo_children():
            widget.destroy()

        for match in fixture:
            home_label = tk.Label(self.fixture_frame.scrollable_frame, text=f"{match[0]}", font=("Helvetica", 13), background=self.master.label_default, fg=self.master.my_team_highlight if match[0] == self.master.selected_club else self.master.highlights)
            home_label.grid(row=grid_index, column=0, sticky='nswe', pady=(5, 5))
            
            score_label = tk.Label(self.fixture_frame.scrollable_frame, text=f"{match[2]}", font=("Helvetica", 13), background=self.master.label_default, fg=self.master.highlights)
            score_label.grid(row=grid_index, column=1, sticky='nswe', pady=(5, 5))
            
            away_label = tk.Label(self.fixture_frame.scrollable_frame, text=f"{match[1]}", font=("Helvetica", 13), background=self.master.label_default, fg=self.master.my_team_highlight if match[1] == self.master.selected_club else self.master.highlights)
            away_label.grid(row=grid_index, column=2, sticky='nswe', pady=(5, 5))
            
            grid_index += 1
        
        for i in range(3):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.fixture_frame.scrollable_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

        # Aktualizuj widok przewijalny
        self.fixture_frame.update_scrollable_frame()

        for i in range(1):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.fixture_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

    def get_matches(self):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Wykonujemy zapytanie, aby wyświetlić dane z konkretnej tabeli (np. druzyny)
        cursor.execute("""
            SELECT druzyna_gospodarza, druzyna_gosci, wynik
            FROM mecze
            WHERE kolejka = ? and rozgrywki = 'cup'
        """, (self.gameweek_to_show,))

        fixture = cursor.fetchall()

        # Zamykamy połączenie
        conn.close()

        return fixture

    def hide(self):
        self.pack_forget()