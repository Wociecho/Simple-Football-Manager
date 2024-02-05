import tkinter as tk
import sqlite3
from tkinter import font

class EuTableScreen(tk.Frame):
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

        # Zmień na wyższą ligę
        self.higher_button = tk.Button(self.buttons_frame, text="<", command=self.change_league_up, bg=self.master.button_bg, fg=self.master.highlights)
        self.higher_button.grid(row=0, column=0, pady=20, sticky="nsew", padx=20)

        # Zmień na niższą ligę
        self.lower_button = tk.Button(self.buttons_frame, text=">", command=self.change_league_down, bg=self.master.button_bg, fg=self.master.highlights)
        self.lower_button.grid(row=0, column=4, pady=20, sticky="nsew", padx=20)
        # Zmień na tabelę
        self.table_button = tk.Button(self.buttons_frame, text="Table", bg=self.master.button_bg, fg=self.master.highlights)
        self.table_button.grid(row=0, column=1, pady=20, sticky="nsew", padx=20)
        # Zmień na terminarz
        self.fixture_button = tk.Button(self.buttons_frame, text="Fixture", command=self.master.switch_to_eu_fixture_interface, bg=self.master.button_bg, fg=self.master.highlights)
        self.fixture_button.grid(row=0, column=2, pady=20, sticky="nsew", padx=20)
        # Zmień na historię
        self.history_button = tk.Button(self.buttons_frame, text="Winners", command=self.master.switch_to_eu_winners_interface, bg=self.master.button_bg, fg=self.master.highlights)
        self.history_button.grid(row=0, column=3, pady=20, sticky="nsew", padx=20)

        self.table_frame_headers = tk.Frame(self, background=self.master.label_default)
        self.table_frame_headers.grid(row=2, column=0, sticky="nsew")
    
    def show(self):
        self.selected_club_label.config(text=f"{self.master.selected_club}")
        self.selected_club_label.config(background=self.master.colors[0])
        self.selected_club_label.config(foreground=self.master.colors[1])
        self.max_leagues = self.get_leagues_levels()

        self.create_widgets()

        self.pack(expand=True, fill="both")

    def create_widgets(self):
        self.table_frame = self.master.scrollable_frame(self, background=self.master.label_default)
        self.table_frame.grid(row=3, column=0, sticky="nsew")

        self.fill_table()

    def fill_table(self):
        if self.max_leagues == 1:
            self.higher_button.config(state=tk.DISABLED)
            self.lower_button.config(command=self.master.switch_to_cup_interface)
        elif self.master.current_selected_league_eu == 1:
            self.higher_button.config(state=tk.DISABLED)
            self.lower_button.config(command=self.change_league_down)
            self.lower_button.config(state=tk.NORMAL)
        elif self.master.current_selected_league_eu == self.max_leagues:
            self.lower_button.config(command=self.master.switch_to_cup_interface)
            self.higher_button.config(state=tk.NORMAL)
        else:
            self.lower_button.config(command=self.change_league_down)
            self.lower_button.config(state=tk.NORMAL)
            self.higher_button.config(state=tk.NORMAL)

        # Pobierz statystyki do tabeli
        teams = self.get_teams(self.master.current_selected_league_eu)

        grid_index = 1
        # Nagłówki tabeli
        self.table_pos_label = tk.Label(self.table_frame_headers, text=f"Pos", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=0, column=0, sticky='nswe', pady=(5, 20))
        self.table_name_label = tk.Label(self.table_frame_headers, text=f"Name", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_name_label.grid(row=0, column=1, sticky='nswe', columnspan=5, pady=(5, 20))
        self.table_pts_label = tk.Label(self.table_frame_headers, text=f"Pts", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pts_label.grid(row=0, column=6, sticky='nswe', pady=(5, 20))
        self.table_w_label = tk.Label(self.table_frame_headers, text=f"W", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_w_label.grid(row=0, column=7, sticky='nswe', pady=(5, 20))
        self.table_d_label = tk.Label(self.table_frame_headers, text=f"D", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_d_label.grid(row=0, column=8, sticky='nswe', pady=(5, 20))
        self.table_l_label = tk.Label(self.table_frame_headers, text=f"L", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_l_label.grid(row=0, column=9, sticky='nswe', pady=(5, 20))
        self.table_gf_label = tk.Label(self.table_frame_headers, text=f"GF", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_gf_label.grid(row=0, column=10, sticky='nswe', pady=(5, 20))
        self.table_ga_label = tk.Label(self.table_frame_headers, text=f"GA", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_ga_label.grid(row=0, column=11, sticky='nswe', pady=(5, 20))
        self.table_form_label = tk.Label(self.table_frame_headers, text=f"Form", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_form_label.grid(row=0, column=12, sticky='nswe', columnspan=2, pady=(5, 20))
        
        for i in range(14):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.table_frame_headers.columnconfigure(i, weight=1, uniform="equal") #kolumny
        
        # Wyczyść listę i dodaj druzyny do tabeli
        for widget in self.table_frame.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Dane tabeli
        for index, team in enumerate(teams, start=1):
            self.table_pos_label = tk.Label(self.table_frame.scrollable_frame, text=f"{index}", font=font.Font(size=13, weight='bold'), background=self.get_bg_color(index), fg=self.master.highlights)
            self.table_pos_label.grid(row=grid_index, column=0, sticky='nswe')
            self.table_name_label = tk.Label(self.table_frame.scrollable_frame, text=f"{team[0]}", font=font.Font(size=13, weight='bold'), background=self.get_bg_color(index), fg=self.master.my_team_highlight if team[0] == self.master.selected_club else self.master.highlights)
            self.table_name_label.grid(row=grid_index, column=1, sticky='nswe', columnspan=5)
            self.table_pts_label = tk.Label(self.table_frame.scrollable_frame, text=f"{team[1]}", font=font.Font(size=13, weight='bold'), background=self.get_bg_color(index), fg=self.master.highlights)
            self.table_pts_label.grid(row=grid_index, column=6, sticky='nswe')
            self.table_w_label = tk.Label(self.table_frame.scrollable_frame, text=f"{team[2]}", font=font.Font(size=13, weight='bold'), background=self.get_bg_color(index), fg=self.master.highlights)
            self.table_w_label.grid(row=grid_index, column=7, sticky='nswe')
            self.table_d_label = tk.Label(self.table_frame.scrollable_frame, text=f"{team[3]}", font=font.Font(size=13, weight='bold'), background=self.get_bg_color(index), fg=self.master.highlights)
            self.table_d_label.grid(row=grid_index, column=8, sticky='nswe')
            self.table_l_label = tk.Label(self.table_frame.scrollable_frame, text=f"{team[4]}", font=font.Font(size=13, weight='bold'), background=self.get_bg_color(index), fg=self.master.highlights)
            self.table_l_label.grid(row=grid_index, column=9, sticky='nswe')
            self.table_gf_label = tk.Label(self.table_frame.scrollable_frame, text=f"{team[5]}", font=font.Font(size=13, weight='bold'), background=self.get_bg_color(index), fg=self.master.highlights)
            self.table_gf_label.grid(row=grid_index, column=10, sticky='nswe')
            self.table_ga_label = tk.Label(self.table_frame.scrollable_frame, text=f"{team[6]}", font=font.Font(size=13, weight='bold'), background=self.get_bg_color(index), fg=self.master.highlights)
            self.table_ga_label.grid(row=grid_index, column=11, sticky='nswe')
            self.table_form_label = tk.Label(self.table_frame.scrollable_frame, text=f"{team[7]}", font=font.Font(size=13, weight='bold'), background=self.get_bg_color(index), fg=self.master.highlights)
            self.table_form_label.grid(row=grid_index, column=12, sticky='nswe', columnspan=2)
            grid_index += 1
        
        for i in range(14):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.table_frame.scrollable_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

        # Aktualizuj widok przewijalny
        self.table_frame.update_scrollable_frame()

        for i in range(1):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.table_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

    def get_bg_color(self, index):
        promotion_color = '#35c191'
        playoff_color = '#0098fa'
        default_color = self.master.label_default
        if index < 9:
            return promotion_color
        elif index > 8 and index < 25:
            return playoff_color
        else:
            return default_color

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

    def get_teams(self, league_level):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Pobieramy statystyki dla wybranej ligi
        cursor.execute("""
            SELECT nazwa, punkty, zwyciestwa, remisy, porazki, bramki_strzelone, bramki_stracone, forma
            FROM eu_druzyny
            WHERE poziom_rozgrywkowy = ?
            ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC
        """, (league_level,))

        teams = cursor.fetchall()

        # Zamykamy połączenie z bazą danych
        conn.close()

        return teams

    def back_to_main_screen(self):
        self.master.switch_to_club_interface()

    def hide(self):
        self.pack_forget()
