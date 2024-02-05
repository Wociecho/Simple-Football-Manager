import tkinter as tk
import sqlite3
from tkinter import font

class EuWinnersScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=self.master.background)
        for i in range(1):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.columnconfigure(i, weight=1, uniform="equal") #kolumny

        self.selected_club_label = tk.Label(self, text="", height=2, font=font.Font(size=26, weight='bold'))
        self.selected_club_label.grid(row=0, column=0, sticky="nsew", columnspan=10)
        self.selected_club_label.bind("<Button-1>", lambda e:self.master.switch_to_club_interface())
        # Zmiana kursora
        self.selected_club_label.bind("<Enter>", self.master.on_enter)
        self.selected_club_label.bind("<Leave>", self.master.on_leave)
        self.buttons_frame = tk.Frame(self, background=self.master.label_default)
        self.buttons_frame.grid(row=1, column=0, sticky="nsew")
        for i in range(5):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.buttons_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

        self.table_frame = tk.Frame(self, background=self.master.label_default)
        self.table_frame.grid(row=2, column=0, sticky="nsew")
        for i in range(3):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.table_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

        # Zmień na wyższą ligę
        self.higher_button = tk.Button(self.buttons_frame, text="<", command=self.change_league_up, bg=self.master.button_bg, fg=self.master.highlights)
        self.higher_button.grid(row=0, column=0, pady=20, sticky="nsew", padx=20)

        # Zmień na niższą ligę
        self.lower_button = tk.Button(self.buttons_frame, text=">", command=self.change_league_down, bg=self.master.button_bg, fg=self.master.highlights)
        self.lower_button.grid(row=0, column=4, pady=20, sticky="nsew", padx=20)
        # Zmień na tabelę
        self.table_button = tk.Button(self.buttons_frame, text="Table", command=self.master.switch_to_eu_table_interface, bg=self.master.button_bg, fg=self.master.highlights)
        self.table_button.grid(row=0, column=1, pady=20, sticky="nsew", padx=20)
        # Zmień na terminarz
        self.fixture_button = tk.Button(self.buttons_frame, text="Fixture", command=self.master.switch_to_eu_fixture_interface, bg=self.master.button_bg, fg=self.master.highlights)
        self.fixture_button.grid(row=0, column=2, pady=20, sticky="nsew", padx=20)
        # Zmień na historię
        self.history_button = tk.Button(self.buttons_frame, text="Winners", bg=self.master.button_bg, fg=self.master.highlights)
        self.history_button.grid(row=0, column=3, pady=20, sticky="nsew", padx=20)
    
    def show(self):
        self.selected_club_label.config(text=f"{self.master.selected_club}")
        self.selected_club_label.config(background=self.master.colors[0])
        self.selected_club_label.config(foreground=self.master.colors[1])
        self.max_leagues = self.get_leagues_levels()

        self.fill_table()
        
        self.pack(expand=True, fill="both")

    def fill_table(self):
        if self.max_leagues == 1:
            self.higher_button.config(state=tk.DISABLED)
            self.lower_button.config(command=self.master.switch_to_cup_winners_interface)
        elif self.master.current_selected_league_eu == 1:
            self.higher_button.config(state=tk.DISABLED)
            self.lower_button.config(command=self.change_league_down)
            self.lower_button.config(state=tk.NORMAL)
        elif self.master.current_selected_league_eu == self.max_leagues:
            self.lower_button.config(command=self.master.switch_to_cup_winners_interface)
            self.higher_button.config(state=tk.NORMAL)
        else:
            self.lower_button.config(command=self.change_league_down)
            self.lower_button.config(state=tk.NORMAL)
            self.higher_button.config(state=tk.NORMAL)

        for widget in self.table_frame.winfo_children():
            widget.destroy()
        # Pobierz statystyki do tabeli
        teams = self.get_teams()

        grid_index = 1
        # Nagłówki tabeli
        self.table_season_label = tk.Label(self.table_frame, text="Season", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_season_label.grid(row=0, column=0, sticky='nswe', pady=(5, 20))
        self.table_first_label = tk.Label(self.table_frame, text="Winner", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_first_label.grid(row=0, column=1, sticky='nswe', pady=(5, 20))
        self.table_second_label = tk.Label(self.table_frame, text="Runner-up", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_second_label.grid(row=0, column=2, sticky='nswe', pady=(5, 20))
        # Dane tabeli
        for team in teams:
            self.table_pos_label = tk.Label(self.table_frame, text=f"Season {team[3]}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.table_pos_label.grid(row=grid_index, column=0, sticky='nswe')
            self.table_name_label = tk.Label(self.table_frame, text=f"{team[0]}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.my_team_highlight if team[0] == self.master.selected_club else self.master.highlights)
            self.table_name_label.grid(row=grid_index, column=1, sticky='nswe')
            self.table_pts_label = tk.Label(self.table_frame, text=f"{team[1]}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.my_team_highlight if team[1] == self.master.selected_club else self.master.highlights)
            self.table_pts_label.grid(row=grid_index, column=2, sticky='nswe')
            grid_index += 1

    def get_leagues_levels(self):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Pobieramy statystyki dla wybranej ligi
        cursor.execute("""
            SELECT MAX(poziom_rozgrywkowy)
            FROM eu_druzyny
        """)

        poziomy_rozgrywkowe = int(cursor.fetchone()[0])

        # Zamykamy połączenie z bazą danych
        conn.close()

        return poziomy_rozgrywkowe

    def change_league_up(self):
        self.master.current_selected_league_eu -= 1
        
        self.fill_table()

    def change_league_down(self):
        self.master.current_selected_league_eu += 1
            
        self.fill_table()

    def get_teams(self):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Pobieramy statystyki dla wybranej ligi
        cursor.execute("""
            SELECT first, second, third, season
            FROM winners
            WHERE league_level = ? AND competition = 'EU'
            ORDER BY season DESC
        """, (self.master.current_selected_league_eu,))

        teams = cursor.fetchall()

        # Zamykamy połączenie z bazą danych
        conn.close()

        return teams

    def back_to_main_screen(self):
        self.master.switch_to_club_interface()

    def hide(self):
        self.pack_forget()
