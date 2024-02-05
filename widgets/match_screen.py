import tkinter as tk
import sqlite3
from tkinter import font
from data_managment import  calendar, save_game, budget_update, cup_advane, create_next_cup_round_schedule, create_next_eu_group_stage_fixture, create_next_eu_round_fixture, create_playoffs, create_playoffs_finals, promote_playoffs_winners
from simulator import rozegraj_mecz

class MatchScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=self.master.background)

        for i in range(1):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.columnconfigure(i, weight=1, uniform="equal") #kolumny
        
        # Przycisk do przejścia do meczu
        self.match_button = tk.Button(self, text="Simulate", font=font.Font(size=32, weight='bold'), command=self.simulate, bg=self.master.button_bg, fg=self.master.highlights)
        self.match_button.grid(row=0, column=0, sticky="nsew")
        self.match_button.bind("<Enter>", self.master.on_enter)
        self.match_button.bind("<Leave>", self.master.on_leave)
        
        self.compare_frame = tk.Frame(self, background=self.master.label_default)
        self.compare_frame.grid(row=1, column=0, sticky="nsew")
        
        for i in range(2):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.compare_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny
        
        self.data_frame = tk.Frame(self, background=self.master.label_default)
        self.data_frame.grid(row=2, column=0, sticky="nsew")
        
        for i in range(3):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.data_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

    def show(self):
        # Wywoływane przy przełączaniu na ekran z meczem
        self.selected_club = self.master.selected_club
        self.gameweek = self.get_gameweek()

        # Pobierz dane o zespołach
        self.clubs_names = self.get_clubs_names(self.selected_club)

        # Wyświetl dane o zespołach
        self.compare_teams(self.clubs_names)

        self.pack(expand=True, fill="both")

    def get_gameweek(self):
        rozgrywki = calendar[self.master.gameweek][0]
        if rozgrywki == "league":
            if self.master.league_level == 1:
                gameweek = calendar[self.master.gameweek][1]
            else:
                gameweek = calendar[self.master.gameweek][2]
        else:
            gameweek = calendar[self.master.gameweek][1]

        return gameweek

    def compare_teams(self, clubs_names):
        stats_home = self.get_stats(clubs_names['gospodarze'])
        stats_away = self.get_stats(clubs_names['goscie'])
        # Przebieg
        for widget in self.compare_frame.winfo_children():
            widget.destroy()
        # Nagłówek
        self.club_name_label = tk.Label(self.compare_frame, text=f"{clubs_names['gospodarze']}", font=font.Font(size=32, weight='bold'), background=stats_home['bg_color'], fg=stats_home['fg_color'])
        self.club_name_label.grid(row=0, column=0, sticky='nswe')
        self.club_name_label = tk.Label(self.compare_frame, text=f"{clubs_names['goscie']}", font=font.Font(size=32, weight='bold'), background=stats_away['bg_color'], fg=stats_away['fg_color'])
        self.club_name_label.grid(row=0, column=1, sticky='nswe')
        self.vs_label = tk.Label(self.compare_frame, text="V", font=font.Font(size=23, weight='bold'), background=stats_home['bg_color'], fg=stats_home['fg_color'])
        self.vs_label.grid(row=0, column=0, sticky='e')
        self.vs_label = tk.Label(self.compare_frame, text="S", font=font.Font(size=23, weight='bold'), background=stats_away['bg_color'], fg=stats_away['fg_color'])
        self.vs_label.grid(row=0, column=1, sticky='w')
        # Dane
        for widget in self.data_frame.winfo_children():
            widget.destroy()
        # Formacja
        self.table_pos_label = tk.Label(self.data_frame, text=f"{stats_home['formacja']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=0, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text="Formation", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=0, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text=f"{stats_away['formacja']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=0, column=2, sticky='nswe')
        # GK
        self.table_pos_label = tk.Label(self.data_frame, text=f"{stats_home['sila_bramkarza']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=1, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text="Goalkeeper", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=1, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text=f"{stats_away['sila_bramkarza']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=1, column=2, sticky='nswe')
        # DEF
        self.table_pos_label = tk.Label(self.data_frame, text=f"{stats_home['sila_obrony']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=2, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text="Defenders", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=2, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text=f"{stats_away['sila_obrony']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=2, column=2, sticky='nswe')
        # MID
        self.table_pos_label = tk.Label(self.data_frame, text=f"{stats_home['sila_pomocy']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=3, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text="Midfielders", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=3, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text=f"{stats_away['sila_pomocy']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=3, column=2, sticky='nswe')
        # ATT
        self.table_pos_label = tk.Label(self.data_frame, text=f"{stats_home['sila_napadu']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=4, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text="Attackers", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=4, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text=f"{stats_away['sila_napadu']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=4, column=2, sticky='nswe')
        # # Trener
        # self.table_pos_label = tk.Label(self.data_frame, text=f"{stats_home['sila_trenera']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        # self.table_pos_label.grid(row=5, column=0, sticky='nswe')
        # self.table_pos_label = tk.Label(self.data_frame, text="Coach", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        # self.table_pos_label.grid(row=5, column=1, sticky='nswe')
        # self.table_pos_label = tk.Label(self.data_frame, text=f"{stats_away['sila_trenera']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        # self.table_pos_label.grid(row=5, column=2, sticky='nswe')
        # Nastawienie
        self.table_pos_label = tk.Label(self.data_frame, text=f"{self.attitude_to_text(stats_home['nastawienie'])}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=5, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text="Attitude", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=5, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text=f"{self.attitude_to_text(stats_away['nastawienie'])}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=5, column=2, sticky='nswe')
        # Dlugosc podan
        self.table_pos_label = tk.Label(self.data_frame, text=f"{self.passing_to_text(stats_home['dlugosc_podan'])}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=6, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text="Passing", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=6, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text=f"{self.passing_to_text(stats_away['dlugosc_podan'])}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=6, column=2, sticky='nswe')
        # Pressing
        self.table_pos_label = tk.Label(self.data_frame, text=f"{self.pressing_to_text(stats_home['pressing'])}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=7, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text="Pressing", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=7, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text=f"{self.pressing_to_text(stats_away['pressing'])}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=7, column=2, sticky='nswe')
        # Wslizgi
        self.table_pos_label = tk.Label(self.data_frame, text=f"{self.tackles_to_text(stats_home['wslizgi'])}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=8, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text="Tackles", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=8, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text=f"{self.tackles_to_text(stats_away['wslizgi'])}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=8, column=2, sticky='nswe')
        # Krycie
        self.table_pos_label = tk.Label(self.data_frame, text=f"{self.cover_to_text(stats_home['krycie'])}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=9, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text="Cover", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=9, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text=f"{self.cover_to_text(stats_away['krycie'])}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=9, column=2, sticky='nswe')
        # Kontry
        self.table_pos_label = tk.Label(self.data_frame, text=f"{self.counter_to_text(stats_home['kontry'])}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=10, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text="Counterattacks", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=10, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text=f"{self.counter_to_text(stats_away['kontry'])}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=10, column=2, sticky='nswe')
        # Pulapki offsidowe
        self.table_pos_label = tk.Label(self.data_frame, text=f"{self.offside_to_text(stats_home['pulapki_offsidowe'])}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=11, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text="Offside trap", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=11, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.data_frame, text=f"{self.offside_to_text(stats_away['pulapki_offsidowe'])}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=11, column=2, sticky='nswe')

    def attitude_to_text(self, attitude):
        if attitude == 1:
            return 'All out'
        elif attitude == 2:
            return 'Offensive'
        elif attitude == 3:
            return 'Neutral'
        elif attitude == 4:
            return 'Defensive'
        elif attitude == 5:
            return 'Ultradefensive'
        
    def passing_to_text(self, passing):
        if passing == 1:
            return 'Long'
        elif passing == 2:
            return 'Mixed'
        elif passing == 3:
            return 'Short'
        
    def pressing_to_text(self, pressing):
        if pressing == 1:
            return 'High'
        elif pressing == 2:
            return 'Normal'
        elif pressing == 3:
            return 'Low'
        
    def tackles_to_text(self, tackles):
        if tackles == 1:
            return 'Hard'
        elif tackles == 2:
            return 'Normal'
        elif tackles == 3:
            return 'Easy'
        
    def cover_to_text(self, cover):
        if cover == 1:
            return 'Zonal'
        elif cover == 2:
            return 'Individual'
        
    def counter_to_text(self, counter):
        if counter == 1:
            return 'Yes'
        elif counter == 2:
            return 'No'
        
    def offside_to_text(self, offside):
        if offside == 1:
            return 'Yes'
        elif offside == 2:
            return 'No'

    def get_stats(self, club_name):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        if calendar[self.master.gameweek][0] == 'EU':
            # Pobieramy statystyki
            cursor.execute("""
                SELECT *
                FROM eu_druzyny 
                WHERE nazwa = ?
            """, (club_name,))

            results = cursor.fetchone()
            kolumny = [opis[0] for opis in cursor.description]  # Pobranie nazw kolumn
            stats = dict(zip(kolumny, results))
        else:
            # Pobieramy statystyki
            cursor.execute("""
                SELECT *
                FROM druzyny 
                WHERE nazwa = ?
            """, (club_name,))

            results = cursor.fetchone()
            kolumny = [opis[0] for opis in cursor.description]  # Pobranie nazw kolumn
            stats = dict(zip(kolumny, results))

        # Zamykamy połączenie z bazą danych
        conn.close()

        return stats

    def get_clubs_names(self, club_name):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Szukamy meczu drużyny club_name w zadanej kolejce gameweek
        cursor.execute("""
            SELECT druzyna_gospodarza, druzyna_gosci
            FROM mecze 
            WHERE (druzyna_gospodarza= ? OR druzyna_gosci= ?) AND (kolejka = ?) AND rozgrywki = ?
        """, (club_name, club_name, self.gameweek, calendar[self.master.gameweek][0],))

        names = cursor.fetchone()

        # Zamykamy połączenie z bazą danych
        conn.close()

        return {
            'gospodarze': names[0],
            'goscie': names[1],
        }

    def simulate(self):
        #typ rozgrywek
        rozgrywki = calendar[self.master.gameweek][0]
        druzyna_gospodarzy = self.get_club_info(self.clubs_names['gospodarze'], rozgrywki)
        druzyna_gosci = self.get_club_info(self.clubs_names['goscie'], rozgrywki)
        wynik = rozegraj_mecz(druzyna_gospodarzy, druzyna_gosci, calendar[self.master.gameweek][0])
        #zapisuje wynik w tabeli mecze
        self.save_result(self.gameweek, wynik['gospodarze']['nazwa'], wynik['goscie']['nazwa'], wynik['gospodarze']['gole'], wynik['goscie']['gole'], rozgrywki, wynik['gospodarze']['karne'], wynik['goscie']['karne'])
        #zapisuje statystyki dla rozgrywek ligowych
        #przyznaje nagrody za zwycięstwo
        self.update_budget(wynik, rozgrywki)
        if rozgrywki == "league" and calendar[self.master.gameweek][2] < 47:
            self.save_stats(wynik, rozgrywki)
        elif rozgrywki == 'EU' and calendar[self.master.gameweek][1] < 9:
            self.save_stats(wynik, rozgrywki)
        elif rozgrywki == 'cup':
            cup_advane(wynik)
        #symuluj pozostałe mecze w tygodniu
        self.simulate_pozostale_mecze(self.clubs_names['gospodarze'], self.clubs_names['goscie'], rozgrywki)
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
        self.master.switch_to_match_result_interface(wynik, rozgrywki)

    def simulate_pozostale_mecze(self, mecz_gracza_d1, mecz_gracza_d2, rozgrywki):
        pozostale_mecze = self.znajdz_pozostale_mecze(mecz_gracza_d1, mecz_gracza_d2, rozgrywki)
        for mecz in pozostale_mecze:
            druzyna_gospodarzy_bot = self.get_club_info(mecz[0], rozgrywki)
            druzyna_gosci_bot = self.get_club_info(mecz[1], rozgrywki)
            #poziom rozgrywkowy
            gameweek = calendar[self.master.gameweek][1]
            if rozgrywki == 'league' and mecz[2] > 1:
                gameweek = calendar[self.master.gameweek][2]
            wynik = rozegraj_mecz(druzyna_gospodarzy_bot, druzyna_gosci_bot, calendar[self.master.gameweek][0])
            self.save_result(gameweek, wynik['gospodarze']['nazwa'], wynik['goscie']['nazwa'], wynik['gospodarze']['gole'], wynik['goscie']['gole'], rozgrywki, wynik['gospodarze']['karne'], wynik['goscie']['karne'])
            self.update_budget(wynik, rozgrywki)
            if rozgrywki == "league" and calendar[self.master.gameweek][2] < 47:
                self.save_stats(wynik, rozgrywki)
            elif rozgrywki == 'EU' and calendar[self.master.gameweek][1] < 9:
                self.save_stats(wynik, rozgrywki)
            elif rozgrywki == 'cup':
                cup_advane(wynik)

    def znajdz_pozostale_mecze(self, mecz_gracza_d1, mecz_gracza_d2, rozgrywki):
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
                WHERE ((kolejka=? AND poziom_rozgrywkowy=1) OR (kolejka=? AND poziom_rozgrywkowy>1)) AND NOT (druzyna_gospodarza = ? OR druzyna_gosci = ?) AND rozgrywki = ?
                ORDER BY poziom_rozgrywkowy
            """, (kolejka_pierwsza_liga, kolejka_nizsze_ligi, mecz_gracza_d1, mecz_gracza_d2, rozgrywki,))
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

    
    def get_club_info(self, club_name, rozgrywki):
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

    def hide(self):
        self.pack_forget()
