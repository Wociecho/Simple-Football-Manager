import tkinter as tk
from tkinter import font
from data_managment import calendar, save_game, budget_update, cup_advane, create_next_cup_round_schedule, create_next_eu_group_stage_fixture, create_next_eu_round_fixture, create_playoffs, create_playoffs_finals, promote_playoffs_winners
from simulator import rozegraj_mecz
import sqlite3

class ClubInterfaceFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=self.master.background)
        for i in range(10):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.columnconfigure(i, weight=1, uniform="equal") #kolumny
            # self.rowconfigure(i, weight=1, uniform="equal") #wiersze

        self.selected_club_label = tk.Label(self, text="", height=2, font=font.Font(size=26, weight='bold'))
        self.selected_club_label.grid(row=0, column=0, sticky="nsew", columnspan=10)

        # Etykiety do wyświetlania informacji o sile bramkarza, obrony, pomocy i ataku
        self.gkframe = tk.Frame(self, highlightbackground=self.master.highlights, highlightthickness=2, background=self.master.label_default)
        self.gkframe.grid(row=1, column=0, pady=10)
        self.goalkeeper_label = tk.Label(self.gkframe, text="", font=font.Font(size=26, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.goalkeeper_label.pack(anchor="center", expand=True)

        self.defframe = tk.Frame(self, highlightbackground=self.master.highlights, highlightthickness=2, background=self.master.label_default)
        self.defframe.grid(row=1, column=1, pady=10)
        self.defence_label = tk.Label(self.defframe, text="", font=font.Font(size=26, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.defence_label.pack(anchor="center", expand=True)

        self.midframe = tk.Frame(self, highlightbackground=self.master.highlights, highlightthickness=2, background=self.master.label_default)
        self.midframe.grid(row=1, column=2, pady=10)
        self.midfield_label = tk.Label(self.midframe, text="", font=font.Font(size=26, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.midfield_label.pack(anchor="center", expand=True)

        self.attframe = tk.Frame(self, highlightbackground=self.master.highlights, highlightthickness=2, background=self.master.label_default)
        self.attframe.grid(row=1, column=3, pady=10)
        self.attack_label = tk.Label(self.attframe, text="", font=font.Font(size=26, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.attack_label.pack(anchor="center", expand=True)

        # Budżet
        budframe = tk.Frame(self, highlightbackground=self.master.highlights, highlightthickness=2, background=self.master.label_default)
        budframe.grid(row=1, column=4, pady=10, columnspan=3)
        self.budget_label = tk.Label(budframe, text="Budget:", font=font.Font(size=26, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.budget_label.pack(anchor="center", expand=True)

        # Week
        gwframe = tk.Frame(self, highlightbackground=self.master.highlights, highlightthickness=2, background=self.master.label_default)
        gwframe.grid(row=1, column=7, pady=10, columnspan=3)
        self.gameweek_label = tk.Label(gwframe, text="", font=font.Font(size=26, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.gameweek_label.pack(anchor="center", expand=True)

        self.opponentframe = tk.Frame(self, highlightbackground=self.master.highlights, highlightthickness=2, background=self.master.label_default)
        self.opponentframe.grid(row=2, column=0, padx=20, pady=20, columnspan=5, sticky="nsew")
        for i in range(5):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.opponentframe.columnconfigure(i, weight=1, uniform="equal") #kolumny

        # Lista do wyświtlania ostatnich i następnych meczów
        self.curfixtureframe = tk.Frame(self, highlightbackground=self.master.highlights, highlightthickness=2, background=self.master.label_default)
        self.curfixtureframe.grid(row=2, column=5, padx=20, pady=20, columnspan=5, sticky="nsew")
        self.curfixtureframe.bind("<Button-1>", lambda e:self.show_fixture())
        # Zmiana kursora
        self.curfixtureframe.bind("<Enter>", self.master.on_enter)
        self.curfixtureframe.bind("<Leave>", self.master.on_leave)
        for i in range(5):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.curfixtureframe.columnconfigure(i, weight=1, uniform="equal") #kolumny
        
        # Tabela skrócona
        self.tableframe = tk.Frame(self, highlightbackground=self.master.highlights, highlightthickness=2, background=self.master.label_default)
        self.tableframe.grid(row=3, column=0, padx=20, pady=20, columnspan=5, rowspan=2, sticky="nsew")
        self.tableframe.bind("<Button-1>", lambda e:self.show_table())
        # Zmiana kursora
        self.tableframe.bind("<Enter>", self.master.on_enter)
        self.tableframe.bind("<Leave>", self.master.on_leave)
        for i in range(5):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.tableframe.columnconfigure(i, weight=1, uniform="equal") #kolumny

        # Przycisk do przejścia do taktyki
        tacframe = tk.Frame(self, highlightbackground=self.master.highlights, highlightthickness=2, background=self.master.label_default)
        tacframe.grid(row=3, column=5, padx=20, pady=20, sticky="nsew", columnspan=5)
        for i in range(1):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            tacframe.columnconfigure(i, weight=1, uniform="equal")
            tacframe.rowconfigure(i, weight=1, uniform="equal")
        self.tactic_button = tk.Button(tacframe, text="Tactic", command=self.show_tactic, font=font.Font(size=24, weight='bold'), bg=self.master.button_bg, fg=self.master.highlights)
        self.tactic_button.grid(row=0, column=0, sticky="nsew")
        
        self.tactic_button.bind("<Enter>", self.master.on_enter)
        self.tactic_button.bind("<Leave>", self.master.on_leave)
        
        # Przycisk do przejścia do transferów
        tmframe = tk.Frame(self, highlightbackground=self.master.highlights, highlightthickness=2, background=self.master.label_default)
        tmframe.grid(row=4, column=5, padx=20, pady=20, sticky="nsew", columnspan=5)
        for i in range(1):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            tmframe.columnconfigure(i, weight=1, uniform="equal")
            tmframe.rowconfigure(i, weight=1, uniform="equal")
        self.transfer_button = tk.Button(tmframe, text="Transfer market", command=self.show_transfer_market, font=font.Font(size=24, weight='bold'), bg=self.master.button_bg, fg=self.master.highlights)
        self.transfer_button.grid(row=0, column=0, sticky="nsew")
        
        self.transfer_button.bind("<Enter>", self.master.on_enter)
        self.transfer_button.bind("<Leave>", self.master.on_leave)

        # Przycisk do przejścia do meczu
        conframe = tk.Frame(self, highlightbackground=self.master.highlights, highlightthickness=2, background=self.master.label_default)
        conframe.grid(row=5, column=0, pady=20, sticky="nsew", columnspan=10, padx=20)
        for i in range(1):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            conframe.columnconfigure(i, weight=1, uniform="equal")
            conframe.rowconfigure(i, weight=1, uniform="equal")
        self.match_button = tk.Button(conframe, text="Pokaż Mecz", command=self.show_next_match, font=font.Font(size=32, weight='bold'), bg=self.master.button_bg, fg=self.master.highlights)
        self.match_button.grid(row=0, column=0, sticky="nsew")
        
        self.match_button.bind("<Enter>", self.master.on_enter)
        self.match_button.bind("<Leave>", self.master.on_leave)

    def show(self):
        self.selected_club = self.master.selected_club
        
        self.selected_club_label.config(background=self.master.colors[0])
        self.selected_club_label.config(foreground=self.master.colors[1])
        # Wywoływane przy przełączaniu na ekran z interfejsem klubu
        self.selected_club_label.config(text=f"{self.selected_club}")

        # Pobierz informacje o drużynie z bazy danych
        club_info = self.get_club_info(self.selected_club)
        # Wyświetl informacje na etykietach
        self.goalkeeper_label.config(text=f"G {club_info['sila_bramkarza']}")
        self.defence_label.config(text=f"D {club_info['sila_obrony']}")
        self.midfield_label.config(text=f"M {club_info['sila_pomocy']}")
        self.attack_label.config(text=f"A {club_info['sila_napadu']}")
        self.budget_label.config(text=f"Budget: {round(club_info['budget'], 2) if club_info['budget'] < 2000 else round(club_info['budget'] / 1000, 2)} {'M' if club_info['budget'] < 2000 else 'B'} €")
        self.gameweek_label.config(text=f"Gameweek: {self.master.gameweek}")

        self.gkframe.config(highlightbackground=self.master.highlights)
        self.defframe.config(highlightbackground=self.master.highlights)
        self.midframe.config(highlightbackground=self.master.highlights)
        self.attframe.config(highlightbackground=self.master.highlights)

        self.gkframe.unbind("<Enter>")
        self.gkframe.unbind("<Leave>")
        self.defframe.unbind("<Enter>")
        self.defframe.unbind("<Leave>")
        self.midframe.unbind("<Enter>")
        self.midframe.unbind("<Leave>")
        self.attframe.unbind("<Enter>")
        self.attframe.unbind("<Leave>")

        # Pobieramy informacje o przeciwniku
        opponent_data = self.get_opponent_info()
        # Wyczyść listę i dodaj mecze
        for widget in self.opponentframe.winfo_children():
            widget.destroy()
        # 0nazwa, 1sila_bramkarza, 2sila_obrony, 3sila_pomocy, 4sila_napadu, 5sila_trenera
        # 6formacja, 7nastawienie, 8forma, 9bg_color, 10fg_color, 11 pozycja     
        if opponent_data:
            #info o kartkach, jeżeli gra:
            if calendar[self.master.gameweek][0] == 'EU' or calendar[self.master.gameweek][0] == 'league':
                kartki = self.get_kartki(calendar[self.master.gameweek][0])

                if ((kartki[0] > 10 or kartki[1] > 0) and calendar[self.master.gameweek][0] == 'league') or ((kartki[0] > 3 or kartki[1] > 0) and (calendar[self.master.gameweek][0] == 'EU')) :
                    self.gkframe.config(highlightbackground="yellow")
                    self.defframe.config(highlightbackground="yellow")
                    self.midframe.config(highlightbackground="yellow")
                    self.attframe.config(highlightbackground="yellow")

                    tekst = 'One of your formation will be slightly weaker next game due to yellow/red cards\nPenalty for every:\n- 10 (3 in EU) yellow cards\n- 1 red card'

                    self.gkframe.bind("<Enter>", lambda event: self.show_tooltip(event, tekst))
                    self.gkframe.bind("<Leave>", lambda event: self.hide_tooltip())
                    self.defframe.bind("<Enter>", lambda event: self.show_tooltip(event, tekst))
                    self.defframe.bind("<Leave>", lambda event: self.hide_tooltip())
                    self.midframe.bind("<Enter>", lambda event: self.show_tooltip(event, tekst))
                    self.midframe.bind("<Leave>", lambda event: self.hide_tooltip())
                    self.attframe.bind("<Enter>", lambda event: self.show_tooltip(event, tekst))
                    self.attframe.bind("<Leave>", lambda event: self.hide_tooltip())
        
            index = int(opponent_data[7])
            nastawienie_tablica = ['All out', 'Offensive', 'Neutral', 'Defensive', 'Ultradefensive']
            nastawienie = nastawienie_tablica[index - 1]
            self.info_label = tk.Label(self.opponentframe, text=f"Next match:", font=font.Font(size=16, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.info_label.grid(row=0, column=0, pady=5, padx=10, columnspan=2)
            self.name_label = tk.Label(self.opponentframe, text=f"{opponent_data[0]}", font=font.Font(size=16, weight='bold'), background=f'{opponent_data[9]}', fg=f'{opponent_data[10]}')
            self.name_label.grid(row=0, column=2, pady=5, padx=10, columnspan=3, sticky="nsew")

            self.gk_label = tk.Label(self.opponentframe, text=f"{opponent_data[1]}", font=font.Font(size=20, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.gk_label.grid(row=1, column=0, pady=5, padx=10)
            self.d_label = tk.Label(self.opponentframe, text=f"{opponent_data[2]}", font=font.Font(size=20, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.d_label.grid(row=1, column=1, pady=5, padx=10)
            self.m_label = tk.Label(self.opponentframe, text=f"{opponent_data[3]}", font=font.Font(size=20, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.m_label.grid(row=1, column=2, pady=5, padx=10)
            self.a_label = tk.Label(self.opponentframe, text=f"{opponent_data[4]}", font=font.Font(size=20, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.a_label.grid(row=1, column=3, pady=5, padx=10)
            self.pos_label = tk.Label(self.opponentframe, text=f'{opponent_data[11]}{"st" if opponent_data[11] == 1 or opponent_data[11] == 21 else ("nd" if opponent_data[11] == 2 or opponent_data[11] == 22 else ("rd" if opponent_data[11] == 3 or opponent_data[11] == 23 else ("" if opponent_data[11] == "CUP" or opponent_data[11] == "EU" else "th")))}', font=font.Font(size=20, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.pos_label.grid(row=1, column=4, pady=5, padx=10)

            #Taktyka
            self.tactic_frame = tk.Frame(self.opponentframe, highlightbackground=self.master.highlights, highlightthickness=2, background=self.master.label_default)
            self.tactic_frame.grid(row=2, column=0, pady=5, padx=10, columnspan=5, sticky="nsew")
            for i in range(1):  # Wszystkie kolumny/wiersze mają tą samą szerokość
                self.tactic_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

            self.formation_label = tk.Label(self.tactic_frame, text=f"{opponent_data[6]}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.formation_label.grid(row=0, column=0, pady=5, padx=10, sticky="nsew", columnspan=5)
            self.attitude_label = tk.Label(self.tactic_frame, text=f"{nastawienie}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.attitude_label.grid(row=1, column=0, pady=5, padx=10,  sticky="nsew", columnspan=5)
            self.form_frame = tk.Frame(self.tactic_frame, background=self.master.label_default)
            self.form_frame.grid(row=2, column=0, pady=5, padx=10,  sticky="nsew")
            for i in range(5):  # Wszystkie kolumny/wiersze mają tą samą szerokość
                self.form_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny
                if len(opponent_data[8]) > i:
                    form = f'{opponent_data[8][i]}'
                else:
                    form = '-'
                self.form_label = tk.Label(self.form_frame, text=f"{form}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
                self.form_label.grid(row=0, column=i, pady=5, padx=10,  sticky="nsew")
        else:
            self.info_label = tk.Label(self.opponentframe, text=f"{'The league at lower levels is played this gameweek' if calendar[self.master.gameweek][0] == 'league' else ('European competitions are taking place this gameweek' if calendar[self.master.gameweek][0] == 'EU' else ('The cup is played this gameweek' if calendar[self.master.gameweek][0] == 'cup' else 'End of the season'))}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.info_label.grid(row=0, column=0, pady=5, padx=10, columnspan=5)

        # Dodaj 5 mecze drużyny gospodarz/gosc/wynik/kolejka
        current_gameweek = self.check_gameweek()
        latest_fixture = self.get_latest_fixture(self.selected_club, current_gameweek)

        # Wyczyść listę i dodaj mecze
        grid_index = 0
        for widget in self.curfixtureframe.winfo_children():
            widget.destroy()
        for fixture in latest_fixture:
            rywal = fixture[1] if fixture[0] == self.master.selected_club else fixture[0]
            miejsce = 'H' if fixture[0] == self.master.selected_club else 'A'
            wynik = fixture[2] if miejsce == 'H' else self.reverse_result(fixture[2])
            kolejka = fixture[3]
            rozgrywki = fixture[4]
            self.fix_gw_label = tk.Label(self.curfixtureframe, text=f"{'L' if  rozgrywki == 'league' else ''}{kolejka if rozgrywki == 'league' else rozgrywki.upper()}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.fix_gw_label.grid(row=grid_index, column=0, padx=10)
            self.fix_ha_label = tk.Label(self.curfixtureframe, text=f"{miejsce}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.fix_ha_label.grid(row=grid_index, column=1, padx=10)
            self.fix_vs_label = tk.Label(self.curfixtureframe, text=f"{rywal}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.fix_vs_label.grid(row=grid_index, column=2, columnspan=3)
            fix_res_label = tk.Label(self.curfixtureframe, text=f"{wynik}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            fix_res_label.grid(row=grid_index, column=5, padx=10)
            grid_index += 1

        # Wyczyść tabelę
        for widget in self.tableframe.winfo_children():
            widget.destroy()

        # Pobierz dane i dodaj tabelę
        teams = self.get_teams(self.master.league_level)

        first_index = self.club_index - 3 if self.club_index > 3 else 1
        last_index = self.club_index + 3 if self.club_index < len(teams) - 3 else len(teams)
        if self.club_index >= len(teams) - 2:
            first_index -= (3 - (len(teams) - self.club_index))
        if self.club_index < 4:
            last_index += (4 - self.club_index)
        grid_index = 0
        for index, team in enumerate(teams, start=1):
            if index >= first_index and index <= last_index:
                self.bar_frame = tk.Frame(self.tableframe, background=self.get_bg_color(self.master.league_level, index))
                self.bar_frame.grid(row=grid_index, column=0, sticky='nswe')

                self.table_pos_label = tk.Label(self.tableframe, text=f"{index}", font=font.Font(size=13, weight='bold'), background=self.get_bg_color(self.master.league_level, index), fg=self.master.highlights)
                self.table_pos_label.grid(row=grid_index, column=0, sticky='nswe')

                self.table_name_label = tk.Label(self.tableframe, text=f"{team[0]}", font=font.Font(size=13, weight='bold'), background=self.get_bg_color(self.master.league_level, index), fg=self.master.my_team_highlight if index == self.club_index else self.master.highlights)
                self.table_name_label.grid(row=grid_index, column=1, columnspan=3, sticky='nswe')

                self.table_points_label = tk.Label(self.tableframe, text=f"{team[1]}", font=font.Font(size=13, weight='bold'), background=self.get_bg_color(self.master.league_level, index), fg=self.master.highlights)
                self.table_points_label.grid(row=grid_index, column=4, sticky='nswe')

                grid_index += 1
        
        # Przypisz onclick do całości tabeli
        self.bind_recursive(self.tableframe, "<Button-1>", lambda e: self.show_table())
        self.bind_recursive(self.curfixtureframe, "<Button-1>", lambda e: self.show_fixture())

        # Zmiana tekstu i funkcji na przycisku jeżeli druzyna nie gra
        if self.master.gameweek == self.master.last_gameweek:
            self.match_button.config(text="Next season")
            self.match_button.config(command=self.start_new_season)
        elif not opponent_data:
            self.match_button.config(text="Next gameweek")
            self.match_button.config(command=self.simulate_other_matches)
        # Zmiana tekstu i funkcji na przycisku jeżeli ostatnia kolejka
        else:
            self.match_button.config(text="Show match")
            self.match_button.config(command=self.show_next_match)

        self.pack(expand=True, fill="both")

    def get_bg_color(self, league, index):
        winner_color = '#008a5e'
        promotion_color = '#35c191'
        playoff_color = '#0098fa'
        relegation_color = '#f37f7e'
        default_color = self.master.label_default
        if index == 1:
            return winner_color
        elif league == 1:
            if index > 1 and index < 5:
                return promotion_color
            elif index > 4 and index < 8:
                return playoff_color
            elif index > 17:
                return relegation_color
            else:
                return default_color
        elif league == 2:
            if index == 2:
                return promotion_color
            elif index > 2 and index < 7:
                return playoff_color
            elif index > 21:
                return relegation_color
            else:
                return default_color
        elif league == 3:
            if index == 2:
                return promotion_color
            elif index > 2 and index < 7:
                return playoff_color
            elif index > 20:
                return relegation_color
            else:
                return default_color
        elif league == 4:
            if index == 2 or index == 3:
                return promotion_color
            elif index > 3 and index < 8:
                return playoff_color
            else:
                return default_color

    def reverse_result(self, input_str):
        parts = input_str.split()
        reversed_array = parts[::-1]
        result_str = ' '.join(reversed_array)
        
        return result_str

    def check_gameweek(self):
        league = self.master.league_level
        check = self.master.gameweek
        if league == 1:
            while calendar[check][0] != "league" or calendar[check][1] == False:
                check -= 1
            return calendar[check][1]
        else:
            while calendar[check][0] != "league":
                check -= 1
            return calendar[check][2]

    def bind_recursive(self, widget, event, func):
        widget.bind(event, func)
        for child in widget.winfo_children():
            self.bind_recursive(child, event, func)

    def show_tooltip(self, event, text):
        x, y, _, _ = event.widget.bbox("insert")
        x += event.widget.winfo_rootx()
        y += event.widget.winfo_rooty() + event.widget.winfo_height() + 5

        self.tooltip = tk.Toplevel(event.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=text, justify='left', background="#ffffe0", relief='solid', borderwidth=1)
        label.pack(ipadx=1)

    def hide_tooltip(self):
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()

    def get_teams(self, league_level):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Pobieramy statystyki dla wybranej ligi
        cursor.execute("""
            SELECT nazwa, punkty
            FROM druzyny
            WHERE poziom_rozgrywkowy = ?
            ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC
        """, (league_level,))

        teams = cursor.fetchall()

        # Zamykamy połączenie z bazą danych
        conn.close()

        for index, team in enumerate(teams, start=1):
            if team[0] == self.master.selected_club:
                self.club_index = index
                break

        return teams
    
    def get_kartki(self, rozgrywki):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        if rozgrywki == 'league':
            # Pobieramy statystyki dla wybranej ligi
            cursor.execute("""
                SELECT zolte_kartki, czerwone_kartki
                FROM druzyny
                WHERE nazwa = ?
            """, (self.master.selected_club,))
            zolte = cursor.fetchone()
        elif rozgrywki == 'EU':
            cursor.execute("""
                SELECT zolte_kartki, czerwone_kartki
                FROM eu_druzyny
                WHERE nazwa = ?
            """, (self.master.selected_club,))
            zolte = cursor.fetchone()

        # Zamykamy połączenie z bazą danych
        conn.close()
        
        if not zolte:
            zolte = [0,0]

        return zolte

    def get_opponent_info(self):
        if self.master.league_level == 1:
            kolejka = calendar[self.master.gameweek][1]
        else:
            if(calendar[self.master.gameweek][0] == "league"):
                kolejka = calendar[self.master.gameweek][2]
            else:
                kolejka = calendar[self.master.gameweek][1]
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Pobieramy mecze dla wszystkich drużyn w następnej kolejce
        cursor.execute("""
            SELECT druzyna_gospodarza, druzyna_gosci
            FROM mecze
            WHERE kolejka=? AND (druzyna_gospodarza = ? OR druzyna_gosci = ?) AND rozgrywki = ?
        """, (kolejka, self.master.selected_club, self.master.selected_club, calendar[self.master.gameweek][0],))

        next_match = cursor.fetchone()

        if next_match:
            next_opponent = next_match[0] if next_match[1] == self.master.selected_club else next_match[1]
            if calendar[self.master.gameweek][0] == 'league':
                cursor.execute("""
                    SELECT nazwa, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, sila_trenera, formacja, nastawienie, forma, bg_color, fg_color, pozycja
                    FROM (
                        SELECT nazwa, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, sila_trenera, formacja, nastawienie, forma, bg_color, fg_color, ROW_NUMBER() OVER (ORDER BY punkty DESC, (bramki_strzelone - bramki_stracone) DESC, bramki_strzelone DESC, zwyciestwa DESC, (sila_bramkarza + sila_obrony + sila_pomocy + sila_napadu) DESC, nazwa ASC) as pozycja
                        FROM druzyny
                        WHERE poziom_rozgrywkowy = ?
                    )
                    WHERE nazwa=?
                """, (self.master.league_level, next_opponent,))

                next_opponent_data = cursor.fetchone()
            elif calendar[self.master.gameweek][0] == 'cup':
                cursor.execute("""
                    SELECT nazwa, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, sila_trenera, formacja, nastawienie, forma, bg_color, fg_color, "CUP" as pozycja
                    FROM druzyny
                    WHERE nazwa=?
                """, (next_opponent,))

                next_opponent_data = cursor.fetchone()

            elif calendar[self.master.gameweek][0] == 'EU':
                cursor.execute("""
                    SELECT nazwa, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, sila_trenera, formacja, nastawienie, forma, bg_color, fg_color, "EU" as pozycja
                    FROM eu_druzyny
                    WHERE nazwa=?
                """, (next_opponent,))

                next_opponent_data = cursor.fetchone()
        else:
            next_opponent_data = False

        # Zamykamy połączenie z bazą danych
        conn.close()

        return next_opponent_data

    def get_latest_fixture(self, club_name, num_rounds):
        curr_gameweek = self.master.gameweek - 1
        prev_games = 3
        next_games = 5
        prev_matches = []
        next_matches = []
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        while prev_games > 0:
            if curr_gameweek > 0:
                rozgrywki = calendar[curr_gameweek][0]
                if rozgrywki == 'league':
                    if self.master.league_level > 1:
                        kolejka = calendar[curr_gameweek][2]
                    else:
                        kolejka = calendar[curr_gameweek][1]
                else:
                    kolejka = calendar[curr_gameweek][1]
                # Pobieramy mecze dla wybranej drużyny
                cursor.execute("""
                    SELECT druzyna_gospodarza, druzyna_gosci, wynik, kolejka, rozgrywki
                    FROM mecze 
                    WHERE (druzyna_gospodarza= ? OR druzyna_gosci= ?) AND kolejka = ? AND rozgrywki = ?
                """, (club_name, club_name, kolejka, rozgrywki,))

                mecz = cursor.fetchone()

                if mecz:
                    prev_matches.insert(0, mecz)
                    prev_games -= 1
                curr_gameweek -= 1
            else:
                next_games += prev_games
                prev_games = 0

        curr_gameweek = self.master.gameweek

        while next_games > 0:
            if curr_gameweek < len(calendar):
                rozgrywki = calendar[curr_gameweek][0]
                if rozgrywki == 'league':
                    if self.master.league_level > 1:
                        kolejka = calendar[curr_gameweek][2]
                    else:
                        kolejka = calendar[curr_gameweek][1]
                else:
                    kolejka = calendar[curr_gameweek][1]
                # Pobieramy mecze dla wybranej drużyny
                cursor.execute("""
                    SELECT druzyna_gospodarza, druzyna_gosci, wynik, kolejka, rozgrywki
                    FROM mecze 
                    WHERE (druzyna_gospodarza= ? OR druzyna_gosci= ?) AND kolejka = ? AND rozgrywki = ?
                """, (club_name, club_name, kolejka, rozgrywki,))

                mecz = cursor.fetchone()

                if mecz:
                    next_matches.append(mecz)
                    next_games -= 1
                curr_gameweek += 1
            else:
                prev_games += next_games
                next_games = 0

        curr_gameweek = self.master.gameweek - 1
        
        if prev_games > 0:
            prev_games += len(prev_matches)
            prev_matches = []
            while prev_games > 0:
                if curr_gameweek > 0:
                    rozgrywki = calendar[curr_gameweek][0]
                    if rozgrywki == 'league':
                        if self.master.league_level > 1:
                            kolejka = calendar[curr_gameweek][2]
                        else:
                            kolejka = calendar[curr_gameweek][1]
                    else:
                        kolejka = calendar[curr_gameweek][1]
                    # Pobieramy mecze dla wybranej drużyny
                    cursor.execute("""
                        SELECT druzyna_gospodarza, druzyna_gosci, wynik, kolejka, rozgrywki
                        FROM mecze 
                        WHERE (druzyna_gospodarza= ? OR druzyna_gosci= ?) AND kolejka = ? AND rozgrywki = ?
                    """, (club_name, club_name, kolejka, rozgrywki,))

                    mecz = cursor.fetchone()

                    if mecz:
                        prev_matches.insert(0, mecz)
                        prev_games -= 1
                    curr_gameweek -= 1

        matches = prev_matches + next_matches

        # Zamykamy połączenie z bazą danych
        conn.close()

        return matches
    
    def get_matches_number(self):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Pobieramy mecze dla wybranej drużyny
        cursor.execute("""
            SELECT COUNT(*)
            FROM druzyny
            WHERE poziom_rozgrywkowy = ?
        """, (self.master.league_level,))

        team_number = cursor.fetchone()[0]

        # Zamykamy połączenie z bazą danych
        conn.close()

        matches_number = (team_number - 1) * 2

        return matches_number

    def hide(self):
        self.pack_forget()

    def get_club_info(self, selected_club):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Pobieramy informacje o drużynie z bazy danych
        cursor.execute("SELECT sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu, budget FROM druzyny WHERE nazwa=?", (selected_club,))
        club_info = cursor.fetchone()

        # Zamykamy połączenie z bazą danych
        conn.close()

        return {
            'sila_bramkarza': club_info[0],
            'sila_obrony': club_info[1],
            'sila_pomocy': club_info[2],
            'sila_napadu': club_info[3],
            'budget': club_info[4],
        }

    def show_next_match(self):
        self.master.switch_to_next_match_interface()

    def start_new_season(self):
        self.master.start_new_season()

    def show_table(self):
        self.master.switch_to_table_interface()

    def show_fixture(self):
        self.master.switch_to_fixture_interface()

    def show_tactic(self):
        self.master.switch_to_tactic_interface()

    def show_transfer_market(self):
        self.master.switch_to_transfer_market_interface()
    
    #symulacja jezeli druzyna nie gra
    def simulate_other_matches(self):
        rozgrywki = calendar[self.master.gameweek][0]
        self.simulate_pozostale_mecze(rozgrywki)
        if rozgrywki == 'league':
            if calendar[self.master.gameweek][2] == 46:
                create_playoffs()
            if calendar[self.master.gameweek][2] == 48:
                create_playoffs_finals()
            if calendar[self.master.gameweek][2] == 49:
                promote_playoffs_winners()
        if rozgrywki == 'cup':
            create_next_cup_round_schedule()
        if rozgrywki =='EU':
            kolejka = calendar[self.master.gameweek][1]
            if kolejka < 8:
                create_next_eu_group_stage_fixture(calendar[self.master.gameweek][1] + 1)
            elif kolejka == 8:
                create_next_eu_round_fixture(2)
            elif kolejka == 10:
                create_next_eu_round_fixture(3)
            elif kolejka == 12:
                create_next_eu_round_fixture(4)
            elif kolejka == 14:
                create_next_eu_round_fixture(5)
            elif kolejka == 16:
                create_next_eu_round_fixture(6)
            elif kolejka == 17:
                create_next_eu_round_fixture(7)
        self.master.next_gameweek()
        save_game(self.master.selected_club, self.master.league_level, self.master.gameweek, self.master.season)
        self.master.switch_to_club_interface()

    #symulacja jezeli druzyna gra + ogolna
    def simulate_pozostale_mecze(self, rozgrywki):
        pozostale_mecze = self.znajdz_pozostale_mecze(rozgrywki)
        if pozostale_mecze:
            for mecz in pozostale_mecze:
                druzyna_gospodarzy_bot = self.get_match_info(mecz[0], rozgrywki)
                druzyna_gosci_bot = self.get_match_info(mecz[1], rozgrywki)
                wynik = rozegraj_mecz(druzyna_gospodarzy_bot, druzyna_gosci_bot, calendar[self.master.gameweek][0])
                gameweek = calendar[self.master.gameweek][1]
                if rozgrywki == 'league' and mecz[2] > 1:
                    gameweek = calendar[self.master.gameweek][2]
                self.save_result(gameweek, wynik['gospodarze']['nazwa'], wynik['goscie']['nazwa'], wynik['gospodarze']['gole'], wynik['goscie']['gole'], rozgrywki, wynik['gospodarze']['karne'], wynik['goscie']['karne'])
                self.update_budget(wynik, rozgrywki)
                if rozgrywki == "league" and calendar[self.master.gameweek][2] < 47:
                    self.save_stats(wynik, rozgrywki)
                elif rozgrywki == 'EU' and calendar[self.master.gameweek][1] < 9:
                    self.save_stats(wynik, rozgrywki)
                elif rozgrywki == 'cup':
                    cup_advane(wynik)

    def znajdz_pozostale_mecze(self, rozgrywki):
        if rozgrywki == "league":
            kolejka_pierwsza_liga = calendar[self.master.gameweek][1]
            kolejka_nizsze_ligi = calendar[self.master.gameweek][2]
        elif rozgrywki == "EU":
            kolejka_pierwsza_liga = calendar[self.master.gameweek][1]
            kolejka_nizsze_ligi = calendar[self.master.gameweek][1]
        else:
            kolejka_pierwsza_liga = calendar[self.master.gameweek][1]
            kolejka_nizsze_ligi = False
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT druzyna_gospodarza, druzyna_gosci, poziom_rozgrywkowy
                FROM mecze
                WHERE ((kolejka=? AND poziom_rozgrywkowy=1) OR (kolejka=? AND poziom_rozgrywkowy>1)) AND rozgrywki = ?
                ORDER BY poziom_rozgrywkowy
            """, (kolejka_pierwsza_liga, kolejka_nizsze_ligi, rozgrywki,))
            mecze = cursor.fetchall()
        return mecze

    def update_budget(self, wynik, rozgrywki):
        if rozgrywki == 'league' or (rozgrywki == 'EU' and calendar[self.master.gameweek][1] < 9):
            if wynik['gospodarze']['gole'] > wynik['goscie']['gole']:
                budget_update(wynik['gospodarze']['nazwa'], 1, rozgrywki)
            if wynik['gospodarze']['gole'] == wynik['goscie']['gole']:
                budget_update(wynik['gospodarze']['nazwa'], 2, rozgrywki)
                budget_update(wynik['goscie']['nazwa'], 2, rozgrywki)
            else:
                budget_update(wynik['goscie']['nazwa'], 1, rozgrywki)
        elif rozgrywki == 'cup' or (rozgrywki == "EU" and calendar[self.master.gameweek][1] >= 9):
            budget_update(wynik['gospodarze']['nazwa'], 1, rozgrywki)
            budget_update(wynik['goscie']['nazwa'], 1, rozgrywki)
    
    def get_match_info(self, club_name, rozgrywki):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            if rozgrywki == "EU":
                cursor.execute("""
                    SELECT *
                    FROM eu_druzyny 
                    WHERE nazwa = ?
                """, (club_name,))
                club = cursor.fetchone()
            else:
                cursor.execute("""
                    SELECT *
                    FROM druzyny 
                    WHERE nazwa = ?
                """, (club_name,))
                club = cursor.fetchone()
        return club

    def save_result(self, kolejka, gospodarze, goscie, wynik_gospodarze, wynik_goscie, rozgrywki, karne_gosp, karne_gosc):
        if rozgrywki == 'league':
            wynik_meczu = f"{wynik_gospodarze} - {wynik_goscie}"
        elif rozgrywki == 'cup':
            if wynik_gospodarze == wynik_goscie:
                wynik_meczu = f"{'p.' if karne_gosp else ''} {wynik_gospodarze} - {wynik_goscie} {'p.' if karne_gosc else ''}"
            else:
                wynik_meczu = f"{wynik_gospodarze} - {wynik_goscie}"
        elif rozgrywki == 'EU':
            wynik_meczu = f"{wynik_gospodarze} - {wynik_goscie}"


        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE mecze
                SET wynik = ?
                WHERE kolejka = ? AND druzyna_gospodarza = ? AND druzyna_gosci = ? AND rozgrywki = ?
            """, (wynik_meczu, kolejka, gospodarze, goscie, rozgrywki,))
            conn.commit()

    def save_stats(self, stats, rozgrywki):
        team_name_gosp = stats['gospodarze']['nazwa']
        team_name_gosc = stats['goscie']['nazwa']
        br_strz_gosp = stats['gospodarze']['gole']
        br_strz_gosc = stats['goscie']['gole']
        zol_gosp = stats['gospodarze']['zolte']
        czerw_gosp = stats['gospodarze']['czerwone']
        zol_gosc = stats['goscie']['zolte']
        czerw_gosc = stats['goscie']['czerwone']

        if br_strz_gosp > br_strz_gosc:
            pkt_gosp, zw_gosp, rem_gosp, prz_gosp = 3, 1, 0, 0
            pkt_gosc, zw_gosc, rem_gosc, prz_gosc = 0, 0, 0, 1
            forma_gosp, forma_gosc = 'W', 'L'
        elif br_strz_gosp == br_strz_gosc:
            pkt_gosp, zw_gosp, rem_gosp, prz_gosp = 1, 0, 1, 0
            pkt_gosc, zw_gosc, rem_gosc, prz_gosc = 1, 0, 1, 0
            forma_gosp, forma_gosc = 'D', 'D'
        else:
            pkt_gosp, zw_gosp, rem_gosp, prz_gosp = 0, 0, 0, 1
            pkt_gosc, zw_gosc, rem_gosc, prz_gosc = 3, 1, 0, 0
            forma_gosp, forma_gosc = 'L', 'W'

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()

            if rozgrywki == 'EU':
                # Update statistics for the home team
                cursor.execute("""
                    UPDATE eu_druzyny
                    SET punkty = punkty + ?,
                        zwyciestwa = zwyciestwa + ?,
                        remisy = remisy + ?,
                        porazki = porazki + ?,
                        bramki_strzelone = bramki_strzelone + ?,
                        bramki_stracone = bramki_stracone + ?,
                        zolte_kartki = zolte_kartki + ?,
                        czerwone_kartki = czerwone_kartki + ?,
                        forma = CASE 
                        WHEN LENGTH(forma) < 5 THEN ? || forma
                        ELSE ? || SUBSTR(forma, 1, LENGTH(forma) - 1)
                        END
                    WHERE nazwa = ?
                """, (pkt_gosp, zw_gosp, rem_gosp, prz_gosp, br_strz_gosp, br_strz_gosc, zol_gosp, czerw_gosp, forma_gosp, forma_gosp, team_name_gosp))

                # Update statistics for the away team
                cursor.execute("""
                    UPDATE eu_druzyny
                    SET punkty = punkty + ?,
                        zwyciestwa = zwyciestwa + ?,
                        remisy = remisy + ?,
                        porazki = porazki + ?,
                        bramki_strzelone = bramki_strzelone + ?,
                        bramki_stracone = bramki_stracone + ?,
                        zolte_kartki = zolte_kartki + ?,
                        czerwone_kartki = czerwone_kartki + ?,
                        forma = CASE 
                        WHEN LENGTH(forma) < 5 THEN ? || forma
                        ELSE ? || SUBSTR(forma, 1, LENGTH(forma) - 1)
                        END
                    WHERE nazwa = ?
                """, (pkt_gosc, zw_gosc, rem_gosc, prz_gosc, br_strz_gosc, br_strz_gosp, zol_gosc, czerw_gosc, forma_gosc, forma_gosc, team_name_gosc))

            else:
                # Update statistics for the home team
                cursor.execute("""
                    UPDATE druzyny
                    SET punkty = punkty + ?,
                        zwyciestwa = zwyciestwa + ?,
                        remisy = remisy + ?,
                        porazki = porazki + ?,
                        bramki_strzelone = bramki_strzelone + ?,
                        bramki_stracone = bramki_stracone + ?,
                        zolte_kartki = zolte_kartki + ?,
                        czerwone_kartki = czerwone_kartki + ?,
                        forma = CASE 
                        WHEN LENGTH(forma) < 5 THEN ? || forma
                        ELSE ? || SUBSTR(forma, 1, LENGTH(forma) - 1)
                        END
                    WHERE nazwa = ?
                """, (pkt_gosp, zw_gosp, rem_gosp, prz_gosp, br_strz_gosp, br_strz_gosc, zol_gosp, czerw_gosp, forma_gosp, forma_gosp, team_name_gosp))

                # Update statistics for the away team
                cursor.execute("""
                    UPDATE druzyny
                    SET punkty = punkty + ?,
                        zwyciestwa = zwyciestwa + ?,
                        remisy = remisy + ?,
                        porazki = porazki + ?,
                        bramki_strzelone = bramki_strzelone + ?,
                        bramki_stracone = bramki_stracone + ?,
                        zolte_kartki = zolte_kartki + ?,
                        czerwone_kartki = czerwone_kartki + ?,
                        forma = CASE 
                        WHEN LENGTH(forma) < 5 THEN ? || forma
                        ELSE ? || SUBSTR(forma, 1, LENGTH(forma) - 1)
                        END
                    WHERE nazwa = ?
                """, (pkt_gosc, zw_gosc, rem_gosc, prz_gosc, br_strz_gosc, br_strz_gosp, zol_gosc, czerw_gosc, forma_gosc, forma_gosc, team_name_gosc))

            # Commit changes
            conn.commit()
