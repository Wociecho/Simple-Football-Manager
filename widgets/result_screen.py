import tkinter as tk
import sqlite3
from tkinter import font
from data_managment import calendar

class ResultScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=self.master.background)

        for i in range(1):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.columnconfigure(i, weight=1, uniform="equal") #kolumny
        
        # Przycisk do przejścia do meczu
        self.match_button = tk.Button(self, text="Continue", font=font.Font(size=32, weight='bold'), command=self.back_to_main_screen, bg=self.master.button_bg, fg=self.master.highlights)
        self.match_button.grid(row=0, column=0, sticky="nsew")
        self.match_button.bind("<Enter>", self.master.on_enter)
        self.match_button.bind("<Leave>", self.master.on_leave)

        self.team_frame = tk.Frame(self, background=self.master.label_default)
        self.team_frame.grid(row=1, column=0, sticky="nsew")
        
        for i in range(2):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.team_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

        self.score_frame = tk.Frame(self, background=self.master.label_default)
        self.score_frame.grid(row=2, column=0, sticky="nsew")
        
        for i in range(2):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.score_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

        self.match_events_frame = tk.Frame(self, background=self.master.label_default)
        self.match_events_frame.grid(row=3, column=0, sticky="nsew")
        
        for i in range(3):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.match_events_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

        self.match_cards_frame = tk.Frame(self, background=self.master.label_default)
        self.match_cards_frame.grid(row=4, column=0, sticky="nsew")
        
        for i in range(3):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.match_cards_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

        self.match_details_frame = tk.Frame(self, background=self.master.label_default)
        self.match_details_frame.grid(row=5, column=0, sticky="nsew")
        
        for i in range(3):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.match_details_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny
        
        # self.match_details_label = tk.Label(self, text="")
        # self.match_details_label.grid(row=4, column=0, sticky="nsew")

    def show(self, wynik, rozgrywki):
        # Wywoływane przy przełączaniu na ekran z wynikiem
        karne = 0
        if rozgrywki == "EU" or rozgrywki == "league":
            karne = self.sprawdz_karne(wynik['gospodarze']['nazwa'], wynik['goscie']['nazwa'])
        # Nagłówek
        for widget in self.team_frame.winfo_children():
            widget.destroy()
        home_colors = self.get_colors(wynik['gospodarze']['nazwa'], rozgrywki)
        away_colors = self.get_colors(wynik['goscie']['nazwa'], rozgrywki)
        self.club_name_label = tk.Label(self.team_frame, text=f"{wynik['gospodarze']['nazwa']}", font=font.Font(size=32, weight='bold'), background=home_colors[0], fg=home_colors[1])
        self.club_name_label.grid(row=0, column=0, sticky='nswe')
        self.club_name_label = tk.Label(self.team_frame, text=f"{wynik['goscie']['nazwa']}", font=font.Font(size=32, weight='bold'), background=away_colors[0], fg=away_colors[1])
        self.club_name_label.grid(row=0, column=1, sticky='nswe')
        self.vs_label = tk.Label(self.team_frame, text="V", font=font.Font(size=23, weight='bold'), background=home_colors[0], fg=home_colors[1])
        self.vs_label.grid(row=0, column=0, sticky='e')
        self.vs_label = tk.Label(self.team_frame, text="S", font=font.Font(size=23, weight='bold'), background=away_colors[0], fg=away_colors[1])
        self.vs_label.grid(row=0, column=1, sticky='w')

        # Wynik
        for widget in self.score_frame.winfo_children():
            widget.destroy()
        self.club_name_label = tk.Label(self.score_frame, text=f"{'p.' if wynik['gospodarze']['karne'] or karne == 1 else ''}{wynik['gospodarze']['gole']}", font=font.Font(size=32, weight='bold'), background=home_colors[0], fg=home_colors[1])
        self.club_name_label.grid(row=0, column=0, sticky='nswe')
        self.club_name_label = tk.Label(self.score_frame, text=f"{wynik['goscie']['gole']}{'p.' if wynik['goscie']['karne'] or karne == 2 else ''}", font=font.Font(size=32, weight='bold'), background=away_colors[0], fg=away_colors[1])
        self.club_name_label.grid(row=0, column=1, sticky='nswe')

        # Przebieg
        for widget in self.match_events_frame.winfo_children():
            widget.destroy()
        if len(wynik['bramki']) > 0:
            for indeks, bramka in enumerate(wynik['bramki']):
                self.goal_label = tk.Label(self.match_events_frame, text=f"{bramka[2] if bramka[0] == 1 else ''}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
                self.goal_label.grid(row=indeks, column=0, sticky='nswe')
                self.min_label = tk.Label(self.match_events_frame, text=f"{bramka[1]}'", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
                self.min_label.grid(row=indeks, column=1, sticky='nswe')
                self.goal_label = tk.Label(self.match_events_frame, text=f"{bramka[2] if bramka[0] == 2 else ''}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
                self.goal_label.grid(row=indeks, column=2, sticky='nswe')

        self.fill_label = tk.Label(self.match_events_frame, text=" ", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.fill_label.grid(row=len(wynik['bramki']), column=0, sticky='nswe', pady=(5,0), columnspan=3)

        for widget in self.match_cards_frame.winfo_children():
            widget.destroy()
        if len(wynik['kartki']) > 0:
            for indeks, kartka in enumerate(wynik['kartki']):
                self.goal_label = tk.Label(self.match_cards_frame, text=f"{'▮' if kartka[0] == 1 else ''}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg='red')
                self.goal_label.grid(row=indeks, column=0, sticky='nswe')
                self.min_label = tk.Label(self.match_cards_frame, text=f"{kartka[1]}'", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
                self.min_label.grid(row=indeks, column=1, sticky='nswe')
                self.goal_label = tk.Label(self.match_cards_frame, text=f"{'▮' if kartka[0] == 2 else ''}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg='red')
                self.goal_label.grid(row=indeks, column=2, sticky='nswe')

        self.fill_label = tk.Label(self.match_cards_frame, text=" ", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.fill_label.grid(row=len(wynik['kartki']), column=0, sticky='nswe', pady=(5,0), columnspan=3)

        # Stats
        for widget in self.match_details_frame.winfo_children():
            widget.destroy()
        self.table_pos_label = tk.Label(self.match_details_frame, text=f"{wynik['gospodarze']['strzaly']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=0, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.match_details_frame, text="Shots", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=0, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.match_details_frame, text=f"{wynik['goscie']['strzaly']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=0, column=2, sticky='nswe')

        self.table_pos_label = tk.Label(self.match_details_frame, text=f"{wynik['gospodarze']['strzaly celne']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=1, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.match_details_frame, text="Shots on target", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=1, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.match_details_frame, text=f"{wynik['goscie']['strzaly celne']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=1, column=2, sticky='nswe')

        self.table_pos_label = tk.Label(self.match_details_frame, text=f"{wynik['gospodarze']['posiadanie']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=2, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.match_details_frame, text="Ball possession", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=2, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.match_details_frame, text=f"{wynik['goscie']['posiadanie']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=2, column=2, sticky='nswe')

        self.table_pos_label = tk.Label(self.match_details_frame, text=f"{wynik['gospodarze']['podania']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=3, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.match_details_frame, text="Passes", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=3, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.match_details_frame, text=f"{wynik['goscie']['podania']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=3, column=2, sticky='nswe')

        self.table_pos_label = tk.Label(self.match_details_frame, text=f"{wynik['gospodarze']['zolte']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=4, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.match_details_frame, text="Yellow cards", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=4, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.match_details_frame, text=f"{wynik['goscie']['zolte']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=4, column=2, sticky='nswe')

        self.table_pos_label = tk.Label(self.match_details_frame, text=f"{wynik['gospodarze']['czerwone']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=5, column=0, sticky='nswe')
        self.table_pos_label = tk.Label(self.match_details_frame, text="Red cards", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=5, column=1, sticky='nswe')
        self.table_pos_label = tk.Label(self.match_details_frame, text=f"{wynik['goscie']['czerwone']}", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.table_pos_label.grid(row=5, column=2, sticky='nswe')

        self.pack(expand=True, fill="both")

    def sprawdz_karne(self, t1, t2):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT wynik
            FROM mecze
            WHERE druzyna_gospodarza = ? AND druzyna_gosci = ? AND rozgrywki = ? AND kolejka = ?
        """, (t1, t2, calendar[self.master.gameweek - 1][0], calendar[self.master.gameweek-1][1],))

        data = cursor.fetchone()

        # Zamykamy połączenie z bazą danych
        conn.close()

        if data:
            wynik = data[0]
            parts = wynik.split()
            if 'p' in parts[1]:
                return 1
            elif 'p' in parts[len(parts) - 2]:
                return 2
            else:
                return 0
        else:
            return 0


    def get_colors(self, club_name, rozgrywki):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        if rozgrywki == 'EU':
            # Pobieramy statystyki
            cursor.execute("""
                SELECT bg_color, fg_color
                FROM eu_druzyny 
                WHERE nazwa = ?
            """, (club_name,))

            colors = cursor.fetchone()
        else:
            # Pobieramy statystyki
            cursor.execute("""
                SELECT bg_color, fg_color
                FROM druzyny
                WHERE nazwa = ?
            """, (club_name,))

            colors = cursor.fetchone()

        # Zamykamy połączenie z bazą danych
        conn.close()

        return colors

    def back_to_main_screen(self):
        self.master.switch_to_club_interface()

    def hide(self):
        self.pack_forget()
