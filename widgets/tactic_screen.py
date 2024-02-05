import tkinter as tk
import sqlite3
from tkinter import ttk, font

class TacticScreen(tk.Frame):
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

        self.formations = ["3-5-2", "3-4-3", "3-3-4", "4-5-1", "4-4-2", "4-3-3", "4-2-4", "5-4-1", "5-3-2", "5-2-3"]
        self.nastawienie = ["All out", "Offensive", "Neutral", "Deffensive", "Ultradeffensive"]
        self.passing = ["Long", "Mixed", "Short"]
        self.pressing = ["High", "Normal", "Low"]
        self.tackle = ["Hard", "Normal", "Easy"]
        self.cover = ["Zonal", "Individual"]
        self.counters_offside = [True, False]


        # Zmienne do przechowywania wybranych opcji
        self.selected_formation = tk.StringVar()
        self.selected_nastawienie = tk.StringVar()
        self.selected_passing = tk.StringVar()
        self.selected_pressing = tk.StringVar()
        self.selected_tackle = tk.StringVar()
        self.selected_cover = tk.StringVar()
        self.selected_counters = tk.BooleanVar()
        self.selected_offside_trap = tk.BooleanVar()

        self.tactic_frame = tk.Frame(self, background=self.master.label_default)
        self.tactic_frame.grid(row=1, column=0, sticky="nsew")
        

        for i in range(2):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.tactic_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

        # Etykieta
        label_formation = tk.Label(self.tactic_frame, text="Team formation:", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        label_formation.grid(row=0, column=0, sticky="nsew", pady=5)

        # Wybór formacji
        self.formation_menu = ttk.Combobox(self.tactic_frame, textvariable=self.selected_formation, values=self.formations, state="readonly", font=font.Font(size=23))
        self.formation_menu.grid(row=0, column=1, sticky="nsew", pady=5)

        # Etykieta
        label_attitude = tk.Label(self.tactic_frame, text="Mentality:", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        label_attitude.grid(row=1, column=0, sticky="nsew", pady=5)

        # Wybór nastawienia
        self.nastawienie_menu = ttk.Combobox(self.tactic_frame, textvariable=self.selected_nastawienie, values=self.nastawienie, state="readonly", font=font.Font(size=23))
        self.nastawienie_menu.grid(row=1, column=1, sticky="nsew", pady=5)

        # Etykieta
        label_passing = tk.Label(self.tactic_frame, text="Passes:", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        label_passing.grid(row=2, column=0, sticky="nsew", pady=5)

        # Wybór rodzaju podań
        self.passing_menu = ttk.Combobox(self.tactic_frame, textvariable=self.selected_passing, values=self.passing, state="readonly", font=font.Font(size=23))
        self.passing_menu.grid(row=2, column=1, sticky="nsew", pady=5)

        # Etykieta
        label_pressing = tk.Label(self.tactic_frame, text="Pressing:", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        label_pressing.grid(row=3, column=0, sticky="nsew", pady=5)
        
        # Wybór rodzaju pressingu
        self.pressing_menu = ttk.Combobox(self.tactic_frame, textvariable=self.selected_pressing, values=self.pressing, state="readonly", font=font.Font(size=23))
        self.pressing_menu.grid(row=3, column=1, sticky="nsew", pady=5)

        # Etykieta
        label_tackle = tk.Label(self.tactic_frame, text="Tackles:", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        label_tackle.grid(row=4, column=0, sticky="nsew", pady=5)

        # Wybór rodzaju wslizgow
        self.tackle_menu = ttk.Combobox(self.tactic_frame, textvariable=self.selected_tackle, values=self.tackle, state="readonly", font=font.Font(size=23))
        self.tackle_menu.grid(row=4, column=1, sticky="nsew", pady=5)

        # Etykieta
        label_cover = tk.Label(self.tactic_frame, text="Cover type:", font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        label_cover.grid(row=5, column=0, sticky="nsew", pady=5)

        # Wybór rodzaju krycia
        self.cover_menu = ttk.Combobox(self.tactic_frame, textvariable=self.selected_cover, values=self.cover, state="readonly", font=font.Font(size=23))
        self.cover_menu.grid(row=5, column=1, sticky="nsew", pady=5)

        # Wybierz czy kontrować
        self.counters = tk.Checkbutton(self.tactic_frame, text="Counterattacks", variable=self.selected_counters, font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights, indicatoron=False, command=self.toggle_color)
        self.counters.grid(row=6, column=0, sticky="nsew", pady=5)

        # Wybierz czy pulapki offsidowe
        self.offside_trap = tk.Checkbutton(self.tactic_frame, text="Offside traps", variable=self.selected_offside_trap, font=font.Font(size=23, weight='bold'), background=self.master.label_default, fg=self.master.highlights, indicatoron=False, command=self.toggle_color)
        self.offside_trap.grid(row=6, column=1, sticky="nsew", pady=5)

        # Przycisk do powrotu do głównego ekranu
        self.back_button = tk.Button(self.tactic_frame, text="Back", command=self.back_to_main_screen, font=font.Font(size=25, weight='bold'), bg=self.master.button_bg, fg=self.master.highlights)
        self.back_button.grid(row=7, column=0, sticky="nsew", pady=5)
        
        # Zmiana kursora
        self.back_button.bind("<Enter>", self.master.on_enter)
        self.back_button.bind("<Leave>", self.master.on_leave)

        # Przycisk do zapisu
        self.save_button = tk.Button(self.tactic_frame, text="Save", command=self.save_tactic, font=font.Font(size=25, weight='bold'), bg=self.master.button_bg, fg=self.master.highlights)
        self.save_button.grid(row=7, column=1, sticky="nsew", pady=5)

        # Zmiana kursora
        self.save_button.bind("<Enter>", self.master.on_enter)
        self.save_button.bind("<Leave>", self.master.on_leave)

    def show(self):
        self.selected_club_label.config(text=f"{self.master.selected_club}")
        self.selected_club_label.config(background=self.master.colors[0])
        self.selected_club_label.config(foreground=self.master.colors[1])

        taktyka = self.get_team_tactic()
        self.formation_menu.set(taktyka[0])
        self.nastawienie_menu.set(self.nastawienie[taktyka[1]-1])
        self.passing_menu.set(self.passing[taktyka[2]-1])
        self.pressing_menu.set(self.pressing[taktyka[3]-1])
        self.tackle_menu.set(self.tackle[taktyka[4]-1])
        self.cover_menu.set(self.cover[taktyka[5]-1])
        self.selected_counters.set(self.counters_offside[taktyka[6]-1])
        self.selected_offside_trap.set(self.counters_offside[taktyka[7]-1])
        self.pack(expand=True, fill="both")
        self.toggle_color()

    def toggle_color(self):
        if self.selected_counters.get():
            self.counters.config(background=self.master.label_default)
        else:
            self.counters.config(background='#f37f7e')

        if self.selected_offside_trap.get():
            self.offside_trap.config(background=self.master.label_default)
        else:
            self.offside_trap.config(background='#f37f7e')

    def get_team_tactic(self):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Pobieramy statystyki dla wybranej ligi
        cursor.execute("""
            SELECT formacja, nastawienie, dlugosc_podan, pressing, wslizgi, krycie, kontry, pulapki_offsidowe
            FROM druzyny
            WHERE nazwa = ?
        """, (self.master.selected_club,))

        taktyka = cursor.fetchone()

        # Zamykamy połączenie z bazą danych
        conn.close()
        return taktyka
    
    def save_tactic(self):
        formation = self.selected_formation.get()
        attitude = int(self.nastawienie.index(self.selected_nastawienie.get()) + 1)
        passing = int(self.passing.index(self.selected_passing.get()) + 1)
        pressing = int(self.pressing.index(self.selected_pressing.get()) + 1)
        tackle = int(self.tackle.index(self.selected_tackle.get()) + 1)
        cover = int(self.cover.index(self.selected_cover.get()) + 1)
        counter = 1 if self.selected_counters.get() else 2
        offside_trap = 1 if self.selected_offside_trap.get() else 2
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        # Zaktualizuj taktykę
        cursor.execute("""
            UPDATE druzyny
            SET formacja = ?, nastawienie = ?, dlugosc_podan = ?, pressing = ?, wslizgi = ?, krycie = ?, kontry = ?, pulapki_offsidowe = ?
            WHERE nazwa = ?
        """, (formation, attitude, passing, pressing, tackle, cover, counter, offside_trap, self.master.selected_club,))
        # Zatwierdź zmiany
        conn.commit()
        # Zamykamy połączenie z bazą danych
        conn.close()

    def back_to_main_screen(self):
        self.master.switch_to_club_interface()

    def hide(self):
        self.pack_forget()
