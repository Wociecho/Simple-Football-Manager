import tkinter as tk
import random
import sqlite3
from tkinter import font
from data_managment import change_strength

class TransferMarketScreen(tk.Frame):
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
        
        # Budżet
        self.budget_label = tk.Label(self, text="", font=font.Font(size=20, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
        self.budget_label.grid(row=1, column=0, sticky="nsew")

        # Dostępni zawodnicy
        self.buy_frame = tk.Frame(self, background=self.master.label_default)
        self.buy_frame.grid(row=2, column=0, sticky="nsew")
        for i in range(5):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.buy_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

        self.sell_frame = tk.Frame(self, background=self.master.label_default)
        self.sell_frame.grid(row=3, column=0, sticky="nsew")
        for i in range(5):  # Wszystkie kolumny/wiersze mają tą samą szerokość
            self.sell_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny

        # Przycisk do powrotu do głównego ekranu
        self.back_button = tk.Button(self, text="Back", command=self.back_to_main_screen, font=font.Font(size=24, weight='bold'), bg=self.master.button_bg, fg=self.master.highlights)
        self.back_button.grid(row=4, column=0, sticky="nsew")

    def show(self):
        self.selected_club_label.config(text=f"{self.master.selected_club}")
        self.selected_club_label.config(background=self.master.colors[0])
        self.selected_club_label.config(foreground=self.master.colors[1])

        self.budget_label.configure(text=f"Budget: {self.get_budget()} M €")
        transfer_list = self.get_transfer_list()
        for widget in self.buy_frame.winfo_children():
            widget.destroy()

        # Wyświetl informacje o każdym zawodniku w panelu
        for index, player_info in enumerate(transfer_list):
            self.player_frame = tk.Label(self.buy_frame, background=self.master.label_default, highlightbackground=self.master.highlights, highlightthickness=2, )
            self.player_frame.grid(row=(index // 5), column=(index - 5 * (index // 5)), sticky='nswe', pady=5, padx=5)
            for i in range(1):  # Wszystkie kolumny/wiersze mają tą samą szerokość
                self.player_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny
            self.transfer_info_label = tk.Label(self.player_frame, text=f"Position: {self.get_position_name(player_info[1])}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.transfer_info_label.grid(row=0, column=0, sticky='nswe')
            self.transfer_info_label = tk.Label(self.player_frame, text=f"{player_info[6]} M €", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.transfer_info_label.grid(row=1, column=0, sticky='nswe')
            self.transfer_info_label = tk.Label(self.player_frame, text=f"Upgrade: {player_info[2]}%", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.transfer_info_label.grid(row=2, column=0, sticky='nswe')
            self.transfer_info_label = tk.Label(self.player_frame, text=f"No change: {player_info[3]}%", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.transfer_info_label.grid(row=3, column=0, sticky='nswe')
            self.transfer_info_label = tk.Label(self.player_frame, text=f"Downgrade: {player_info[4]}%", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.transfer_info_label.grid(row=4, column=0, sticky='nswe')
            self.transfer_info_label = tk.Label(self.player_frame, text=f"Expire time: {player_info[5]} weeks", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.transfer_info_label.grid(row=5, column=0, sticky='nswe')

            # Przycisk Zakup z dodatkowym atrybutem player_info
            self.button_purchase = tk.Button(self.player_frame, text="Buy", command=lambda player_info=player_info: self.purchase_player(player_info), font=font.Font(size=10, weight='bold'), bg=self.master.button_bg, fg=self.master.highlights)
            self.button_purchase.player_info = player_info
            self.button_purchase.player_id = player_info[0]
            self.button_purchase.grid(row=6, column=0, sticky='nswe')

        # Lista do sprzedaży
        sell_list = self.get_sell_list()
        for widget in self.sell_frame.winfo_children():
            widget.destroy()

        # Wyświetl informacje o każdym zawodniku w panelu
        for index, player_info in enumerate(sell_list):
            self.player_frame = tk.Label(self.sell_frame, background=self.master.label_default, highlightbackground=self.master.highlights, highlightthickness=2, )
            self.player_frame.grid(row=0, column=index+1, sticky='nswe', pady=5, padx=5)
            for i in range(1):  # Wszystkie kolumny/wiersze mają tą samą szerokość
                self.player_frame.columnconfigure(i, weight=1, uniform="equal") #kolumny
            self.transfer_info_label = tk.Label(self.player_frame, text=f"Position: {self.get_position_name(player_info[1])}", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.transfer_info_label.grid(row=0, column=0, sticky='nswe')
            self.transfer_info_label = tk.Label(self.player_frame, text=f"{player_info[5]} M €", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.transfer_info_label.grid(row=1, column=0, sticky='nswe')
            self.transfer_info_label = tk.Label(self.player_frame, text=f"No change: {player_info[2]}%", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.transfer_info_label.grid(row=2, column=0, sticky='nswe')
            self.transfer_info_label = tk.Label(self.player_frame, text=f"Downgrade: {player_info[3]}%", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.transfer_info_label.grid(row=3, column=0, sticky='nswe')
            self.transfer_info_label = tk.Label(self.player_frame, text=f"Expire time: {player_info[4]} weeks", font=font.Font(size=13, weight='bold'), background=self.master.label_default, fg=self.master.highlights)
            self.transfer_info_label.grid(row=4, column=0, sticky='nswe')

            # Przycisk Sprzedaj z dodatkowym atrybutem player_info
            self.button_sell = tk.Button(self.player_frame, text="Sell", command=lambda player_info=player_info: self.sell_player(player_info), font=font.Font(size=10, weight='bold'), bg=self.master.button_bg, fg=self.master.highlights)
            self.button_sell.player_info = player_info
            self.button_sell.player_id = player_info[0]
            self.button_sell.grid(row=5, column=0, sticky='nswe')

        self.pack(expand=True, fill="both")
    
    def get_position_name(self, position):
        # Mapuj numer pozycji na odpowiadającą mu nazwę
        position_mapping = {1: "Goalkeeper", 2: "Defender", 3: "Midfielder", 4: "Attacker"}
        return position_mapping.get(position, "Unknown")
    
    def purchase_player(self, player):
        price = player[6]
        # Kod obsługujący zakup zawodnika
        output = random.choices(
            [1,2,3],
            [player[2], player[3], player[4]]
        )[0]

        # button_purchase = self.get_button_purchase(player)
        for player_frame in self.buy_frame.winfo_children():
            if isinstance(player_frame, tk.Label):
                for button in player_frame.winfo_children():
                    if isinstance(button, tk.Button) and hasattr(button, 'player_id') and button.player_id == player[0]:
                        # Znaleziono odpowiedni przycisk, zmień jego tekst
                        if self.get_budget() > player[6]:
                            change_strength(self.master.selected_club, player[1], output, price, button.player_id, 'buy')
                            button.configure(text="Bought")
                            button.config(state="disabled")
                            self.budget_label.configure(text=f"Budget: {self.get_budget()} M €")
                        else:
                            button.configure(text="No money!")
                            button.config(state="disabled")
                        break  # Przerwij pętlę, gdy przycisk zostanie znaleziony

    def sell_player(self, player):
        price = player[5]
        # Kod obsługujący zakup zawodnika
        output = random.choices(
            [2,3],
            [player[2], player[3]]
        )[0]

        # button_purchase = self.get_button_purchase(player)
        for player_frame in self.sell_frame.winfo_children():
            if isinstance(player_frame, tk.Label):
                for button in player_frame.winfo_children():
                    if isinstance(button, tk.Button) and hasattr(button, 'player_id') and button.player_id == player[0]:
                        # Znaleziono odpowiedni przycisk, zmień jego tekst
                        change_strength(self.master.selected_club, player[1], output, price, button.player_id, 'sell')
                        button.configure(text="Sold")
                        button.config(state="disabled")
                        self.budget_label.configure(text=f"Budget: {self.get_budget()} M €")
                        break  # Przerwij pętlę, gdy przycisk zostanie znaleziony
    
    def get_transfer_list(self):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT *
            FROM transfer_market
        """)

        zawodnicy = cursor.fetchall()

        # Zamykamy połączenie z bazą danych
        conn.close()

        return zawodnicy
    
    def get_sell_list(self):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT *
            FROM transfer_market_sell
        """)

        zawodnicy = cursor.fetchall()

        # Zamykamy połączenie z bazą danych
        conn.close()

        return zawodnicy
    
    def get_budget(self):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Pobieramy informacje o drużynie z bazy danych
        cursor.execute("SELECT budget FROM druzyny WHERE nazwa=?", (self.master.selected_club,))
        budget = cursor.fetchone()

        # Zamykamy połączenie z bazą danych
        conn.close()

        return round(budget[0], 2)
    def hide(self):
        self.pack_forget()

    def back_to_main_screen(self):
        self.master.switch_to_club_interface()
