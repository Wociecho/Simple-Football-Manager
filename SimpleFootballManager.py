import tkinter as tk
from tkinter import *
import sqlite3
from data_managment import calendar, initiate, save_game, reset_schedule, update_teams_for_new_season, season_end_update_eu_teams, add_winners, update_eu_cups, fill_transfer_market, create_transfer_list, load_game, season_end_update_teams
from widgets import start_screen_frame, scrollable_frame, club_selection_frame, club_interface_frame, match_screen, result_screen, table_screen, eu_table_screen, tactic_screen, transfer_market_screen, fixture_screen, eu_fixture_screen, cup_screen, cup_winners_screen, winners_screen, eu_winners_screen

class FootballManagerGame(tk.Tk):
    def __init__(self):
        super().__init__()
        # '#525CEB'
        self.background = '#525CEB'
        self.highlights = '#aFeFf8'
        self.label_default = '#9DADC5'
        self.my_team_highlight = '#fffedc'
        self.button_bg = '#3d4756'
        self.configure(bg=self.background)

        initiate()

        self.gameweek = 1
        self.last_gameweek = len(calendar) - 1
        self.season = 1

        self.scrollable_frame = scrollable_frame.ScrollableFrame

        # Ekran startowy
        self.start_screen_frame = start_screen_frame.StartScreenFrame(self)
        self.start_screen_frame.pack(expand=True, fill="both")

        # Ekran wyboru klubu
        self.club_selection_frame = club_selection_frame.ClubSelectionFrame(self)
        self.club_selection_frame.pack(expand=True, fill="both")
        self.club_selection_frame.hide()

        # Ukrywamy ekran z interfejsem klubu na początku
        self.club_interface_frame = club_interface_frame.ClubInterfaceFrame(self)
        self.club_interface_frame.pack(expand=True, fill="both")
        self.club_interface_frame.hide()

        # Interface meczu
        self.match_screen = match_screen.MatchScreen(self)
        self.match_screen.pack(expand=True, fill="both")
        self.match_screen.hide()

        # Interface wynik
        self.result_screen = result_screen.ResultScreen(self)
        self.result_screen.pack(expand=True, fill="both")
        self.result_screen.hide()

        # Tabela
        self.table_screen = table_screen.TableScreen(self)
        self.table_screen.pack(expand=True, fill="both")
        self.table_screen.hide()

        # Tabela EU
        self.eu_table_screen = eu_table_screen.EuTableScreen(self)
        self.eu_table_screen.pack(expand=True, fill="both")
        self.eu_table_screen.hide()

        # Terminarz
        self.fixture_screen = fixture_screen.FixtureScreen(self)
        self.fixture_screen.pack(expand=True, fill="both")
        self.fixture_screen.hide()

        # Terminarz EU
        self.eu_fixture_screen = eu_fixture_screen.EuFixtureScreen(self)
        self.eu_fixture_screen.pack(expand=True, fill="both")
        self.eu_fixture_screen.hide()

        # Puchar
        self.cup_screen = cup_screen.CupScreen(self)
        self.cup_screen.pack(expand=True, fill="both")
        self.cup_screen.hide()

        self.cup_winners_screen = cup_winners_screen.CupWinnersScreen(self)
        self.cup_winners_screen.pack(expand=True, fill="both")
        self.cup_winners_screen.hide()

        # Zwycięzcy
        self.winners_screen = winners_screen.WinnersScreen(self)
        self.winners_screen.pack(expand=True, fill="both")
        self.winners_screen.hide()

        # Zwycięzcy EU
        self.eu_winners_screen = eu_winners_screen.EuWinnersScreen(self)
        self.eu_winners_screen.pack(expand=True, fill="both")
        self.eu_winners_screen.hide()

        # Taktyka
        self.tactic_screen = tactic_screen.TacticScreen(self)
        self.tactic_screen.pack(expand=True, fill="both")
        self.tactic_screen.hide()

        # Transfer market
        self.transfer_market_screen = transfer_market_screen.TransferMarketScreen(self)
        self.transfer_market_screen.pack(expand=True, fill="both")
        self.transfer_market_screen.hide()
        
    def load_game(self):
        data = load_game()
        self.selected_club = data[0]
        self.colors = self.get_colors()
        self.league_level = data[1]
        self.gameweek = data[2]
        self.season = data[3]
        self.switch_to_club_interface()

    def switch_to_club_interface(self):
        self.current_selected_league = self.league_level
        self.current_selected_league_eu = 2
        # Wywołaj tę funkcję, aby przełączyć się na ekran z interfejsem klubu
        self.start_screen_frame.hide()
        self.club_selection_frame.hide()
        self.fixture_screen.hide()
        self.eu_fixture_screen.hide()
        self.cup_screen.hide()
        self.cup_winners_screen.hide()
        self.winners_screen.hide()
        self.eu_winners_screen.hide()
        self.result_screen.hide()
        self.table_screen.hide()
        self.eu_table_screen.hide()
        self.tactic_screen.hide()
        self.transfer_market_screen.hide()
        self.club_interface_frame.show()

    def switch_to_next_match_interface(self):
        # Przełącz na interface następnego meczu
        self.club_interface_frame.hide()
        self.match_screen.show()

    def switch_to_match_result_interface(self, results, competition):
        self.match_screen.hide()
        self.result_screen.show(results, competition)

    def switch_to_table_interface(self):
        self.club_interface_frame.hide()
        self.cup_screen.hide()
        self.fixture_screen.hide()
        self.winners_screen.hide()
        self.table_screen.show()

    def switch_to_eu_table_interface(self):
        self.club_interface_frame.hide()
        self.cup_screen.hide()
        self.fixture_screen.hide()
        self.winners_screen.hide()
        self.eu_fixture_screen.hide()
        self.eu_winners_screen.hide()
        self.eu_table_screen.show()

    def switch_to_fixture_interface(self):
        self.table_screen.hide()
        self.club_interface_frame.hide()
        self.winners_screen.hide()
        self.fixture_screen.show()

    def switch_to_eu_fixture_interface(self):
        self.eu_table_screen.hide()
        self.eu_winners_screen.hide()
        self.club_interface_frame.hide()
        self.eu_fixture_screen.show()

    def switch_to_cup_interface(self):
        self.table_screen.hide()
        self.eu_table_screen.hide()
        self.cup_winners_screen.hide()
        self.club_interface_frame.hide()
        self.winners_screen.hide()
        self.cup_screen.show()

    def switch_to_cup_winners_interface(self):
        self.winners_screen.hide()
        self.eu_winners_screen.hide()
        self.cup_screen.hide()
        self.table_screen.hide()
        self.club_interface_frame.hide()
        self.cup_winners_screen.show()

    def switch_to_winners_interface(self):
        self.table_screen.hide()
        self.cup_screen.hide()
        self.cup_winners_screen.hide()
        self.fixture_screen.hide()
        self.club_interface_frame.hide()
        self.winners_screen.show()

    def switch_to_eu_winners_interface(self):
        self.eu_table_screen.hide()
        self.cup_screen.hide()
        self.cup_winners_screen.hide()
        self.eu_fixture_screen.hide()
        self.club_interface_frame.hide()
        self.eu_winners_screen.show()

    def switch_to_tactic_interface(self):
        self.club_interface_frame.hide()
        self.tactic_screen.show()

    def switch_to_transfer_market_interface(self):
        self.club_interface_frame.hide()
        self.transfer_market_screen.show()

    def set_user_club(self, club_name, league_level):
        reset_schedule()
        self.selected_club = club_name
        self.league_level = league_level
        self.season = 1
        self.colors = self.get_colors()
        create_transfer_list(self.selected_club)
        save_game(self.selected_club, self.league_level, self.gameweek, self.season)

    def next_gameweek(self):
        fill_transfer_market(self.selected_club)
        self.gameweek += 1

    def start_new_season(self):
        sezon = self.season
        season_end_update_teams(self.selected_club)
        season_end_update_eu_teams()
        add_winners(sezon)
        update_eu_cups()
        status_zespolu = update_teams_for_new_season(self.selected_club)
        if status_zespolu == 0:
            self.league_level -= 1
        elif status_zespolu == 2:
            self.league_level += 1
        reset_schedule()
        self.gameweek = 1
        self.season += 1
        save_game(self.selected_club, self.league_level, self.gameweek, self.season)
        self.club_interface_frame.show()
        self.current_selected_league = self.league_level

    def switch_to_club_selection_interface(self):
        self.start_screen_frame.hide()
        self.club_selection_frame.show()
    
    def on_enter(self, event):
        self.config(cursor="hand2")

    def on_leave(self, event):
        self.config(cursor="")

    def get_colors(self):
        # Łączymy się z bazą danych
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Pobieramy statystyki dla wybranej ligi
        cursor.execute("""
            SELECT bg_color, fg_color
            FROM druzyny
            WHERE nazwa = ?
        """, (self.selected_club,))

        colors = cursor.fetchone()

        # Zamykamy połączenie z bazą danych
        conn.close()

        return colors

if __name__ == "__main__":
    app = FootballManagerGame()
    app.title("Simple Football Manager")
    app.geometry("1000x850")
    app.mainloop()