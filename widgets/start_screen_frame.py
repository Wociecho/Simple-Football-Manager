import tkinter as tk
from tkinter import font
import sqlite3

class StartScreenFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg=self.master.background)
        self.avoid_start = 0

        # Przycisk
        self.continue_button = tk.Button(self, text="Continue", command=self.continue_game, font=font.Font(size=25, weight='bold'), width=20, height=4, bg=self.master.button_bg, fg=self.master.highlights)
        self.continue_button.pack(pady=60)

        # Przycisk
        self.start_button = tk.Button(self, text="New game", command=self.new_game, font=font.Font(size=13, weight='bold'), width=20, height=2, bg=self.master.button_bg, fg=self.master.highlights)
        self.start_button.pack(pady=(60, 20))

        if not self.check_if_can_load():
            self.avoid_start = 1
            self.continue_button.pack_forget()
            self.start_button.configure(font=font.Font(size=25, weight='bold'), width=20, height=4)

    def check_if_can_load(self):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Pobieramy nazwy klubów z bazy danych
        cursor.execute("SELECT selected_club, league_level, gameweek FROM saved_game")
        data = cursor.fetchall()[0]

        # Zamykamy połączenie z bazą danych
        conn.close()

        return True if data[0] else False

    def new_game(self):
        self.avoid_start += 1
        if self.avoid_start > 1:
            self.master.switch_to_club_selection_interface()
        else:
            self.start_button.configure(text="Are you sure?")

    def continue_game(self):
        self.master.load_game()

    def hide(self):
        self.pack_forget()