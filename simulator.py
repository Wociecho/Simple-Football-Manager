import random
import math
from data_managment import clear_cards

class Druzyna:
    def __init__(self, druzyna):
        # 1nazwa, 2formacja, 3sila_bramkarza, 4sila_obrony, 5sila_pomocy, 6sila_napadu, 7zaangazowanie_druzyny, 8sila_trenera, 9nastawienie,
        # 10dlugosc_podan, 11pressing, 12wslizgi, 13krycie, 14kontry, 15pulapki_offsidowe, 16premia_domowa
        self.nazwa = druzyna[1]
        self.formacja = druzyna[2]
        self.liczba_obroncow, self.liczba_pomocnikow, self.liczba_napastnikow = map(int, druzyna[2].split('-'))
        self.wsp_zaangazowania = (100 - druzyna[7]) * 0.4
        self.sila_bramkarza = max(1, druzyna[3] * druzyna[16] - self.wsp_zaangazowania)
        self.sila_obrony = max(1, druzyna[4] * druzyna[16] - self.wsp_zaangazowania)
        self.sila_pomocy = max(1, druzyna[5]  * druzyna[16] - self.wsp_zaangazowania)
        self.sila_napadu = max(1, druzyna[6]  * druzyna[16] - self.wsp_zaangazowania)
        self.poczatkowa_sila_bramkarza = druzyna[3] * druzyna[16]
        self.poczatkowa_sila_obrony = druzyna[4] * druzyna[16]
        self.poczatkowa_sila_pomocy = druzyna[5] * druzyna[16]
        self.poczatkowa_sila_napadu = druzyna[6] * druzyna[16]
        self.kondycja_bramkarza = 100
        self.kondycja_obrony = 100
        self.kondycja_pomocy = 100
        self.kondycja_napadu = 100
        self.zaangazowanie_druzyny = druzyna[7]
        self.sila_trenera = druzyna[8]
        self.nastawienie = druzyna[9]
        self.dlugosc_podan = druzyna[10]
        self.pressing = druzyna[11]
        self.wslizgi = druzyna[12]
        self.krycie = druzyna[13]
        self.kontry = druzyna[14]
        self.pulapki_offsidowe = druzyna[15]

    def __str__(self):
        return f"Druzyna:\nFormacja: {self.formacja}\n" \
               f"Liczba obroncow: {self.liczba_obroncow}\n" \
               f"Liczba pomocnikow: {self.liczba_pomocnikow}\n" \
               f"Liczba napastnikow: {self.liczba_napastnikow}\n" \
               f"Sila bramkarza: {self.sila_bramkarza}\n" \
               f"Sila obrony: {self.sila_obrony}\n" \
               f"Sila pomocy: {self.sila_pomocy}\n" \
               f"Sila napadu: {self.sila_napadu}\n" \
               f"Poczatkowa sila bramkarza: {self.poczatkowa_sila_bramkarza}\n" \
               f"Poczatkowa sila obrony: {self.poczatkowa_sila_obrony}\n" \
               f"Poczatkowa sila pomocy: {self.poczatkowa_sila_pomocy}\n" \
               f"Poczatkowa sila napadu: {self.poczatkowa_sila_napadu}\n" \
               f"Kondycja bramkarza: {self.kondycja_bramkarza}\n" \
               f"Kondycja obrony: {self.kondycja_obrony}\n" \
               f"Kondycja pomocy: {self.kondycja_pomocy}\n" \
               f"Kondycja napadu: {self.kondycja_napadu}\n" \
               f"Zaangazowanie druzyny: {self.zaangazowanie_druzyny}\n" \
               f"Sila trenera: {self.sila_trenera}"



class Mecz:
    def __init__(self, druzyna_A, druzyna_B):
        self.druzyna_A = druzyna_A
        self.druzyna_B = druzyna_B
        self.czas_meczu = 0
        self.czas_doliczony = 0
        self.polowa = 1
        self.posiadanie_pilki = random.choice([True, False])  # Losowe przyznanie posiadania piłki jednej z drużyn
        self.strefa_aktywna = 4 if self.posiadanie_pilki else 3  # Określenie strefy startowej
        self.druzyna_zaczyna = True
        self.formacja_przy_pilce = 2
        self.wynik_A = 0
        self.wynik_B = 0
        self.strzaly_A = 0
        self.strzaly_B = 0
        self.strzalyc_A = 0
        self.strzalyc_B = 0
        self.posiadanie_druzyna_A = 0
        self.posiadanie_druzyna_B = 0
        self.z_kartki_A = 0
        self.cz_kartki_A = 0
        self.z_kartki_B = 0
        self.cz_kartki_B = 0
        self.podania_A = 0
        self.podania_B = 0
        self.d_podania_A = 0
        self.d_podania_B = 0
        self.kontra_A = 0
        self.kontra_B = 0
        self.bramki = []
        self.kartki = []
        
    def oblicz_szanse(self, pozycja, strefa):
        # Dla zadanej pozycji i strefy zwraca szanse na dane zagranie
        # w kolejności [2 do przodu, 1 do przodu, bez zmian, 1 do tyłu
        nastawienie = self.sprawdz_nastawienie(1 if self.posiadanie_pilki else 2)
        nastawienie_przeciwnej = self.sprawdz_nastawienie(2 if self.posiadanie_pilki else 1)
        podania = self.sprawdz_podania(1 if self.posiadanie_pilki else 2)
        def zmien_tablice(tablica1, tablica2):
            return [a + b for a, b in zip(tablica1, tablica2)]
        tablica_szans = [
            # 1	2	3	4	5	6
            [ [30,40,30,0], None, None, None, None, None ],  # B
            [ [25,45,30,0], [25,45,25,5], [10,50,30,10], [0,20,60,20], None, None ],  # O
            [ [30,50,20,0], [30,50,15,5], [25,50,15,10], [25,55,10,10], [20,50,15,15], [0,40,30,30] ],  # P
            [ None, None, [25,55,15,5], [30,55,10,5], [45,25,20,10], [0,80,15,5] ]  # N
        ]

        if nastawienie == 1:
            # Hurraofensywne
            #zwieksz szanse na szybkie wyjscie z obrony
            tablica_szans[0][0] = zmien_tablice(tablica_szans[0][0], [10,10,-20,0])
            tablica_szans[1][0] = zmien_tablice(tablica_szans[1][0], [6,6,-12,0])
            tablica_szans[2][0] = zmien_tablice(tablica_szans[2][0], [5,5,-10,0])
            #zwieksz szanse na strzał pomocnicy
            tablica_szans[2][4] = zmien_tablice(tablica_szans[2][4], [3,0,-1,-2])
            tablica_szans[2][5] = zmien_tablice(tablica_szans[2][5], [0,3,-1,-2])
            #napastnicy
            tablica_szans[3][4] = zmien_tablice(tablica_szans[3][4], [4,0,-2,-2])
            tablica_szans[3][5] = zmien_tablice(tablica_szans[3][5], [0,3,-1,-2])
        elif nastawienie == 2:
            # Ofensywne
            #zwieksz szanse na szybkie wyjscie z obrony
            tablica_szans[0][0] = zmien_tablice(tablica_szans[0][0], [5,5,-10,0])
            tablica_szans[1][0] = zmien_tablice(tablica_szans[1][0], [3,3,-6,0])
            tablica_szans[2][0] = zmien_tablice(tablica_szans[2][0], [2,3,-5,0])
            #zwieksz szanse na strzał pomocnicy
            tablica_szans[2][4] = zmien_tablice(tablica_szans[2][4], [1,0,0,-1])
            tablica_szans[2][5] = zmien_tablice(tablica_szans[2][5], [0,1,0,-1])
            #napastnicy
            tablica_szans[3][4] = zmien_tablice(tablica_szans[3][4], [2,0,-1,-1])
            tablica_szans[3][5] = zmien_tablice(tablica_szans[3][5], [0,1,0,-1])
        elif nastawienie == 4:
            # Zmniejsz szanse na strzał jeżeli gra defensywnie
            tablica_szans[2][4] = zmien_tablice(tablica_szans[2][4], [-4,1,2,1])
            tablica_szans[2][5] = zmien_tablice(tablica_szans[2][5], [0,-4,2,2])
            tablica_szans[3][4] = zmien_tablice(tablica_szans[3][4], [-6,2,2,2])
            tablica_szans[3][5] = zmien_tablice(tablica_szans[3][5], [0,-6,3,3])
            # Zmniejsz szanse na długie piłki
            tablica_szans[2][2] = zmien_tablice(tablica_szans[2][2], [-3,1,1,1])
            tablica_szans[2][3] = zmien_tablice(tablica_szans[2][3], [-3,1,1,1])
            tablica_szans[3][2] = zmien_tablice(tablica_szans[3][2], [-5,2,2,1])
            tablica_szans[3][3] = zmien_tablice(tablica_szans[3][3], [-5,2,2,1])
        elif nastawienie == 5:
            # Zmniejsz szanse na strzał jeżeli gra defensywnie
            tablica_szans[2][4] = zmien_tablice(tablica_szans[2][4], [-8,2,3,3])
            tablica_szans[2][5] = zmien_tablice(tablica_szans[2][5], [0,-8,4,4])
            tablica_szans[3][4] = zmien_tablice(tablica_szans[3][4], [-12,4,4,4])
            tablica_szans[3][5] = zmien_tablice(tablica_szans[3][5], [0,-12,6,6])
            # Zmniejsz szanse na długie piłki
            tablica_szans[2][2] = zmien_tablice(tablica_szans[2][2], [-5,2,2,1])
            tablica_szans[2][3] = zmien_tablice(tablica_szans[2][3], [-5,2,2,1])
            tablica_szans[3][2] = zmien_tablice(tablica_szans[3][2], [-10,4,3,3])
            tablica_szans[3][3] = zmien_tablice(tablica_szans[3][3], [-10,4,3,3])

        if nastawienie_przeciwnej == 5:
            # Zmniejsz szanse na strzał jeżeli przeciwnik ultradef
            tablica_szans[2][4] = zmien_tablice(tablica_szans[2][4], [-10,3,4,3])
            tablica_szans[2][5] = zmien_tablice(tablica_szans[2][5], [0,-10,5,5])
            tablica_szans[3][4] = zmien_tablice(tablica_szans[3][4], [-15,5,5,5])
            tablica_szans[3][5] = zmien_tablice(tablica_szans[3][5], [0,-15,8,7])
        elif nastawienie_przeciwnej == 4:
            # Zmniejsz szanse na strzał jeżeli przeciwnik def
            tablica_szans[2][4] = zmien_tablice(tablica_szans[2][4], [-5,1,2,2])
            tablica_szans[2][5] = zmien_tablice(tablica_szans[2][5], [0,-5,2,3])
            tablica_szans[3][4] = zmien_tablice(tablica_szans[3][4], [-8,2,3,3])
            tablica_szans[3][5] = zmien_tablice(tablica_szans[3][5], [0,-8,4,4])

        szanse = tablica_szans[pozycja][strefa]

        # Zmień szanse na długie/krotkie zagranie
        #długie
        if podania == 1:
            if self.posiadanie_pilki and self.strefa_aktywna < 5:
                zmien_tablice(szanse, [5,-3,-1,-1])
            elif not self.posiadanie_pilki and self.strefa_aktywna > 2:
                zmien_tablice(szanse, [5,-3,-1,-1])
        #krótkie
        elif podania == 3:
            if self.posiadanie_pilki and self.strefa_aktywna < 5:
                zmien_tablice(szanse, [-10,8,1,1])
            elif not self.posiadanie_pilki and self.strefa_aktywna > 2:
                zmien_tablice(szanse, [-10,8,1,1])

        # Kontra
        if self.posiadanie_pilki and self.kontra_A > self.czas_meczu:
            if self.strefa_aktywna < 6:
                zmien_tablice(szanse, [szanse[3] + szanse[2] , 0, -szanse[2], -szanse[3]]) 
        elif not self.posiadanie_pilki and self.kontra_B > self.czas_meczu:
            if self.strefa_aktywna > 1:
                zmien_tablice(szanse, [szanse[3] + szanse[2] , 0, -szanse[2], -szanse[3]])

        return szanse
        
    def transformuj_liczbe(self, liczba):
        calkowita = liczba // 10
        reszta = liczba % 10
    
        if reszta == 0:
            wynik = calkowita + 1
        else:
            wynik = calkowita + 1 + reszta / 10
        return wynik
        
    def aktualizuj_sile(self, czas_akcji):
        wslizgi = self.sprawdz_wslizgi(2 if self.posiadanie_pilki else 1)
        krycie = self.sprawdz_krycie(2 if self.posiadanie_pilki else 1)
        # tablica_udzialow = [
        #     [0.4, 0.5, 0.1, 0], [0, 0.8, 0.2, 0], [0, 0.3, 0.6, 0.1], [0, 0.1, 0.7, 0.2], [0, 0, 0.5, 0.5], [0, 0, 0.2, 0.8]
        # ]
        # udzialy_druzyna_A = tablica_udzialow[self.strefa_aktywna - 1]
        # udzialy_druzyna_B = tablica_udzialow[ 7 - self.strefa_aktywna - 1]
        self.druzyna_A.kondycja_bramkarza -= ((0.05 * czas_akcji * self.transformuj_liczbe(math.ceil(self.czas_meczu))) + 0.1 * czas_akcji if not self.posiadanie_pilki else 0 + 0.1 * czas_akcji if self.posiadanie_pilki and self.formacja_przy_pilce == 0 else 0 + round(random.uniform(0.01, 0.06), 2) * czas_akcji) / 2 
        self.druzyna_A.sila_bramkarza = max(1, (self.druzyna_A.poczatkowa_sila_bramkarza * self.druzyna_A.kondycja_bramkarza / 100) - self.druzyna_A.wsp_zaangazowania)
        self.druzyna_A.kondycja_obrony -= (0.05 * czas_akcji * self.transformuj_liczbe(math.ceil(self.czas_meczu))) + 0.05 * czas_akcji if not self.posiadanie_pilki and krycie == 2 else 0 + 0.03 * czas_akcji if not self.posiadanie_pilki and wslizgi == 1 else 0 + 0.14 * czas_akcji if not self.posiadanie_pilki and self.druzyna_A.nastawienie == 1 else (0.12 * czas_akcji if not self.posiadanie_pilki and self.druzyna_A.nastawienie == 2 else (0.1 * czas_akcji if not self.posiadanie_pilki else 0)) + 0.1 * czas_akcji if self.posiadanie_pilki and self.formacja_przy_pilce == 1 else 0 + round(random.uniform(0.01, 0.06), 2) * czas_akcji * (1 if self.druzyna_A.liczba_obroncow == 5 else (2 if self.druzyna_A.liczba_obroncow == 4 else 3))
        self.druzyna_A.sila_obrony = max(1, (self.druzyna_A.poczatkowa_sila_obrony * self.druzyna_A.kondycja_obrony / 100) - self.druzyna_A.wsp_zaangazowania)
        self.druzyna_A.kondycja_pomocy -= (0.05 * czas_akcji * self.transformuj_liczbe(math.ceil(self.czas_meczu))) + 0.05 * czas_akcji if not self.posiadanie_pilki and krycie == 2 else 0 + 0.03 * czas_akcji if not self.posiadanie_pilki and wslizgi == 1 else 0 + 0.12 * czas_akcji if not self.posiadanie_pilki and self.druzyna_A.nastawienie == 1 else (0.11 * czas_akcji if not self.posiadanie_pilki and self.druzyna_A.nastawienie == 2 else (0.1 * czas_akcji if not self.posiadanie_pilki else 0)) + 0.1 * czas_akcji if self.posiadanie_pilki and self.formacja_przy_pilce == 2 else 0 + round(random.uniform(0.01, 0.06), 2) * czas_akcji * (1 if self.druzyna_A.liczba_pomocnikow == 5 else (1.5 if self.druzyna_A.liczba_pomocnikow == 4 else (2.5 if self.druzyna_A.liczba_pomocnikow == 3 else 4)))
        self.druzyna_A.sila_pomocy = max(1, (self.druzyna_A.poczatkowa_sila_pomocy * self.druzyna_A.kondycja_pomocy / 100) - self.druzyna_A.wsp_zaangazowania)
        self.druzyna_A.kondycja_napadu -= (0.05 * czas_akcji * self.transformuj_liczbe(math.ceil(self.czas_meczu))) + 0.03 * czas_akcji if not self.posiadanie_pilki and wslizgi == 1 else 0 + 0.1 * czas_akcji if not self.posiadanie_pilki else 0 + (0.2 if self.druzyna_A.nastawienie == 5 else (0.15 if self.druzyna_A.nastawienie == 4 else 0.1)) * czas_akcji if self.posiadanie_pilki and self.formacja_przy_pilce == 3 else 0 + round(random.uniform(0.01, 0.06), 2) * czas_akcji * (1 if self.druzyna_A.liczba_napastnikow == 4 else (2 if self.druzyna_A.liczba_napastnikow == 3 else (2.5 if self.druzyna_A.liczba_napastnikow == 2 else 3)))
        self.druzyna_A.sila_napadu = max(1, (self.druzyna_A.poczatkowa_sila_napadu * self.druzyna_A.kondycja_napadu / 100) - self.druzyna_A.wsp_zaangazowania)
        
        
        self.druzyna_B.kondycja_bramkarza -= ((0.05 * czas_akcji * self.transformuj_liczbe(math.ceil(self.czas_meczu))) + 0.1 * czas_akcji if self.posiadanie_pilki else 0 + 0.1 * czas_akcji if not self.posiadanie_pilki and self.formacja_przy_pilce == 0 else 0 + round(random.uniform(0.01, 0.06), 2) * czas_akcji) / 2
        self.druzyna_B.sila_bramkarza = max(1, (self.druzyna_B.poczatkowa_sila_bramkarza * self.druzyna_B.kondycja_bramkarza / 100) - self.druzyna_B.wsp_zaangazowania)
        self.druzyna_B.kondycja_obrony -= (0.05 * czas_akcji * self.transformuj_liczbe(math.ceil(self.czas_meczu))) + 0.05 * czas_akcji if self.posiadanie_pilki and krycie == 2 else 0 + 0.03 * czas_akcji if self.posiadanie_pilki and wslizgi == 1 else 0 + 0.14 * czas_akcji if self.posiadanie_pilki and self.druzyna_B.nastawienie == 1 else (0.12 * czas_akcji if self.posiadanie_pilki and self.druzyna_B.nastawienie == 2 else (0.1 * czas_akcji if self.posiadanie_pilki else 0)) + 0.1 * czas_akcji if not self.posiadanie_pilki and self.formacja_przy_pilce == 1 else 0 + round(random.uniform(0.01, 0.06), 2) * czas_akcji * (1 if self.druzyna_B.liczba_obroncow == 5 else (2 if self.druzyna_B.liczba_obroncow == 4 else 3))
        self.druzyna_B.sila_obrony = max(1, (self.druzyna_B.poczatkowa_sila_obrony * self.druzyna_B.kondycja_obrony / 100) - self.druzyna_B.wsp_zaangazowania)
        self.druzyna_B.kondycja_pomocy -= (0.05 * czas_akcji * self.transformuj_liczbe(math.ceil(self.czas_meczu))) + 0.05 * czas_akcji if self.posiadanie_pilki and krycie == 2 else 0 + 0.03 * czas_akcji if self.posiadanie_pilki and wslizgi == 1 else 0 + 0.12 * czas_akcji if self.posiadanie_pilki and self.druzyna_B.nastawienie == 1 else (0.11 * czas_akcji if self.posiadanie_pilki and self.druzyna_B.nastawienie == 2 else (0.1 * czas_akcji if self.posiadanie_pilki else 0)) + 0.1 * czas_akcji if not self.posiadanie_pilki and self.formacja_przy_pilce == 2 else 0 + round(random.uniform(0.01, 0.06), 2) * czas_akcji * (1 if self.druzyna_B.liczba_pomocnikow == 5 else (1.5 if self.druzyna_B.liczba_pomocnikow == 4 else (2.5 if self.druzyna_B.liczba_pomocnikow == 3 else 4)))
        self.druzyna_B.sila_pomocy = max(1, (self.druzyna_B.poczatkowa_sila_pomocy * self.druzyna_B.kondycja_pomocy / 100) - self.druzyna_B.wsp_zaangazowania)
        self.druzyna_B.kondycja_napadu -= (0.05 * czas_akcji * self.transformuj_liczbe(math.ceil(self.czas_meczu))) + 0.03 * czas_akcji if self.posiadanie_pilki and wslizgi == 1 else 0 + 0.1 * czas_akcji if self.posiadanie_pilki else 0 + (0.2 if self.druzyna_B.nastawienie == 5 else (0.15 if self.druzyna_B.nastawienie == 4 else 0.1)) * czas_akcji if not self.posiadanie_pilki and self.formacja_przy_pilce == 3 else 0 + round(random.uniform(0.01, 0.06), 2) * czas_akcji * (1 if self.druzyna_B.liczba_napastnikow == 4 else (2 if self.druzyna_B.liczba_napastnikow == 3 else (2.5 if self.druzyna_B.liczba_napastnikow == 2 else 3)))
        self.druzyna_B.sila_napadu = max(1, (self.druzyna_B.poczatkowa_sila_napadu * self.druzyna_B.kondycja_napadu / 100) - self.druzyna_B.wsp_zaangazowania)
        # #print(0.1 * czas_akcji if not self.posiadanie_pilki else 0)
        # #print(self.druzyna_A.kondycja_obrony)
        # #print(czas_akcji/3)
        
    def sprawdz_czy_udany_odbior(self):
        wslizgi_przeciwnika = self.sprawdz_wslizgi(2 if self.posiadanie_pilki else 1)
        kontra = self.sprawdz_kontre(2 if self.posiadanie_pilki else 1)
        if self.posiadanie_pilki:
            if self.formacja_przy_pilce == 0:
                sila_formacji_tracacej = self.druzyna_A.sila_bramkarza
            elif self.formacja_przy_pilce == 1:
                sila_formacji_tracacej = self.druzyna_A.sila_obrony
            elif self.formacja_przy_pilce == 2:
                sila_formacji_tracacej = self.druzyna_A.sila_pomocy
            elif self.formacja_przy_pilce == 3:
                sila_formacji_tracacej = self.druzyna_A.sila_napadu

            szansa_na_strate = max(0, min(100, 100 - 0.4 * (sila_formacji_tracacej - 50)))
            
            odbior = random.choices(
                [True, False],
                [szansa_na_strate, 100 - szansa_na_strate]
            )[0]
            
            if odbior:
                self.zmien_posiadanie()
                # Aktywuj kontratak
                if kontra == 1:
                    if (self.posiadanie_pilki and self.strefa_aktywna < 3) or (not self.posiadanie_pilki and self.strefa_aktywna > 4):
                        if self.posiadanie_pilki:
                            self.kontra_A = self.czas_meczu + 3
                        else:
                            self.kontra_B = self.czas_meczu + 3

            else:
                podwojna_kara = 1
                if self.strefa_aktywna == 6:
                    szansa_na_karny = random.choices(
                        [True, False],
                        [100 - self.druzyna_B.sila_obrony, self.druzyna_B.sila_obrony]
                    )[0]
                    if szansa_na_karny:
                        self.czas_doliczony += 0.5
                        podwojna_kara = 0
                        strzel_karnego = random.choices(
                            [True, False],
                            [50 + self.druzyna_A.sila_napadu / 2 - self.druzyna_B.sila_bramkarza * 0.1, 100 - (50 + self.druzyna_A.sila_napadu / 2 - self.druzyna_B.sila_bramkarza * 0.1)]
                        )[0]
                        # print(f"RZUT KARNY w {round(self.czas_meczu)}")
                        if strzel_karnego:
                            self.strzaly_A += 1
                            self.strzalyc_A += 1
                            self.wynik_A += 1
                            # print(f"GOOOOL z karnego w {round(self.czas_meczu)} min dla A")
                            self.dodaj_bramke(1)
                            self.strefa_aktywna = 3
                            self.posiadanie_pilki = False
                        else:
                            self.strzaly_A += 1
                            self.posiadanie_pilki = random.choice([True, False])
                            # print(f"karny nie trafiony w {round(self.czas_meczu)} min dla A")
                    # else:
                        # print(f"NIE MA KARNEGO w {round(self.czas_meczu)}")
                        
                szansa_kartka = max(10, min(100, 60 + sila_formacji_tracacej / 2 - (90 - round(self.czas_meczu)) / 2))
                if wslizgi_przeciwnika == 1:
                    szansa_kartka = min(100, szansa_kartka + 10)
                elif wslizgi_przeciwnika == 3:
                    szansa_kartka = max(0, szansa_kartka - 10)
                szansa_na_kartke = random.choices(
                    [True, False],
                    [szansa_kartka, 100 - szansa_kartka]
                )[0]
                if szansa_na_kartke:
                    szansa_na_czerwona = max(1, min(100, (sila_formacji_tracacej / 2 - (90 - round(self.czas_meczu)) / 2 + self.z_kartki_B * 5) / 3)) * podwojna_kara if self.z_kartki_B < 11 else 100
                    czerwona_kartka = random.choices(
                        [True, False],
                        [szansa_na_czerwona, 100 - szansa_na_czerwona]
                    )[0]
                    if czerwona_kartka:
                        self.czas_doliczony += 0.5
                        self.cz_kartki_B += 1
                        self.dodaj_kartke(2)
                        self.druzyna_B.poczatkowa_sila_obrony *= 0.87
                        self.druzyna_B.sila_obrony = max(1, (self.druzyna_B.poczatkowa_sila_obrony * self.druzyna_B.kondycja_obrony / 100) - self.druzyna_B.wsp_zaangazowania)
                        self.druzyna_B.poczatkowa_sila_pomocy *= 0.87
                        self.druzyna_B.sila_pomocy = max(1, (self.druzyna_B.poczatkowa_sila_pomocy * self.druzyna_B.kondycja_pomocy / 100) - self.druzyna_B.wsp_zaangazowania)
                        self.druzyna_B.poczatkowa_sila_napadu *= 0.87
                        self.druzyna_B.sila_napadu = max(1, (self.druzyna_B.poczatkowa_sila_napadu * self.druzyna_B.kondycja_napadu / 100) - self.druzyna_B.wsp_zaangazowania)
                        if self.druzyna_B.liczba_napastnikow > 1:
                            self.druzyna_B.liczba_napastnikow -= 1
                        elif self.druzyna_B.liczba_pomocnikow > 2:
                            self.druzyna_B.liczba_pomocnikow -= 1
                        elif self.druzyna_B.liczba_obroncow > 3:
                            self.druzyna_B.liczba_obroncow -= 1
                        # print(f"CZERWONA dla B w {round(self.czas_meczu)}")
                    else:
                        self.czas_doliczony += 0.2
                        # print(f"zolta dla B w {round(self.czas_meczu)}")
                        self.z_kartki_B += 1
                # else:
                    # print(f"NIEudany przechwyt przez B w {round(self.czas_meczu)}")
        else:
            if self.formacja_przy_pilce == 0:
                sila_formacji_tracacej = self.druzyna_B.sila_bramkarza
            elif self.formacja_przy_pilce == 1:
                sila_formacji_tracacej = self.druzyna_B.sila_obrony
            elif self.formacja_przy_pilce == 2:
                sila_formacji_tracacej = self.druzyna_B.sila_pomocy
            elif self.formacja_przy_pilce == 3:
                sila_formacji_tracacej = self.druzyna_B.sila_napadu
            
            szansa_na_strate = max(0, min(100, 100 - 0.4 * (sila_formacji_tracacej - 50)))

            odbior = random.choices(
                [True, False],
                [szansa_na_strate, 100 - szansa_na_strate]
            )[0]
            if odbior:
                self.zmien_posiadanie()

                # Aktywuj kontratak
                if kontra == 1:
                    if (self.posiadanie_pilki and self.strefa_aktywna < 3) or (not self.posiadanie_pilki and self.strefa_aktywna > 4):
                        if self.posiadanie_pilki:
                            self.kontra_A = self.czas_meczu + 3
                        else:
                            self.kontra_B = self.czas_meczu + 3
            else:
                podwojna_kara = 1
                if self.strefa_aktywna == 1:
                    szansa_na_karny = random.choices(
                        [True, False],
                        [100 - self.druzyna_A.sila_obrony, self.druzyna_A.sila_obrony]
                    )[0]
                    if szansa_na_karny:
                        self.czas_doliczony += 0.5
                        podwojna_kara = 0
                        strzel_karnego = random.choices(
                            [True, False],
                            [50 + self.druzyna_B.sila_napadu / 2 - self.druzyna_A.sila_bramkarza * 0.1, 100 - (50 + self.druzyna_B.sila_napadu / 2 - self.druzyna_A.sila_bramkarza * 0.1)]
                        )[0]
                        # print(f"RZUT KARNY w {round(self.czas_meczu)}")
                        if strzel_karnego:
                            self.strzaly_B += 1
                            self.strzalyc_B += 1
                            self.wynik_B += 1
                            self.dodaj_bramke(2)
                            # print(f"GOOOOL z karnego w {round(self.czas_meczu)} min dla B")
                            self.strefa_aktywna = 4
                            self.posiadanie_pilki = True
                        else:
                            self.strzaly_B += 1
                            self.posiadanie_pilki = random.choice([True, False])
                            # print(f"karny nie trafiony w {round(self.czas_meczu)} min dla B")
                    # else:
                        # print(f"NIE MA KARNEGO w {round(self.czas_meczu)}")
                        
                szansa_kartka = max(10, min(100, 60 + sila_formacji_tracacej / 2 - (90 - round(self.czas_meczu)) / 2))
                
                if wslizgi_przeciwnika == 1:
                    szansa_kartka = min(100, szansa_kartka + 10)
                elif wslizgi_przeciwnika == 3:
                    szansa_kartka = max(0, szansa_kartka - 10)

                szansa_na_kartke = random.choices(
                    [True, False],
                    [szansa_kartka, 100 - szansa_kartka]
                )[0]
                if szansa_na_kartke:
                    szansa_na_czerwona = max(1, min(100, (sila_formacji_tracacej / 2 - (90 - round(self.czas_meczu)) / 2 + self.z_kartki_A * 5) / 3)) * podwojna_kara if self.z_kartki_A < 11 else 100
                    czerwona_kartka = random.choices(
                        [True, False],
                        [szansa_na_czerwona, 100 - szansa_na_czerwona]
                    )[0]
                    if czerwona_kartka:
                        self.czas_doliczony += 0.5
                        self.cz_kartki_A += 1
                        self.dodaj_kartke(1)
                        self.druzyna_A.poczatkowa_sila_obrony *= 0.87
                        self.druzyna_A.sila_obrony = max(1, (self.druzyna_A.poczatkowa_sila_obrony * self.druzyna_A.kondycja_obrony / 100) - self.druzyna_A.wsp_zaangazowania)
                        self.druzyna_A.poczatkowa_sila_pomocy *= 0.87
                        self.druzyna_A.sila_pomocy = max(1, (self.druzyna_A.poczatkowa_sila_pomocy * self.druzyna_A.kondycja_pomocy / 100) - self.druzyna_A.wsp_zaangazowania)
                        self.druzyna_A.poczatkowa_sila_napadu *= 0.87
                        self.druzyna_A.sila_napadu = max(1, (self.druzyna_A.poczatkowa_sila_napadu * self.druzyna_A.kondycja_napadu / 100) - self.druzyna_A.wsp_zaangazowania)
                        if self.druzyna_A.liczba_napastnikow > 1:
                            self.druzyna_A.liczba_napastnikow -= 1
                        elif self.druzyna_A.liczba_pomocnikow > 2:
                            self.druzyna_A.liczba_pomocnikow -= 1
                        elif self.druzyna_A.liczba_obroncow > 3:
                            self.druzyna_A.liczba_obroncow -= 1
                        # print(f"CZERWONA dla A w {round(self.czas_meczu)}")
                    else:
                        self.czas_doliczony += 0.2
                        self.z_kartki_A += 1
                        # print(f"zolta dla A w {round(self.czas_meczu)}")
                # else:
                    # print(f"NIEudany przechwyt przez A w {round(self.czas_meczu)}")
                

    def przenies_akcje(self, strefa, posiadanie_pilki):
        druzyna = "pierwsza" if posiadanie_pilki else "druga"
        nastawienie = self.sprawdz_nastawienie(1 if posiadanie_pilki else 2)
        nastawienie_przeciwnej = self.sprawdz_nastawienie(2 if posiadanie_pilki else 1)
        pressing_przeciwnika = self.sprawdz_pressing(2 if posiadanie_pilki else 1)
        wslizgi_przeciwnika = self.sprawdz_wslizgi(2 if posiadanie_pilki else 1)
        krycie_przeciwnika = self.sprawdz_krycie(2 if posiadanie_pilki else 1)
        if strefa == 1:
            um_druzyna_A = round(0.4 * self.druzyna_A.sila_bramkarza + 0.5 * self.druzyna_A.sila_obrony + 0.1 * self.druzyna_A.sila_pomocy)
            um_druzyna_B = round(0.2 * self.druzyna_B.sila_pomocy + 0.8 * self.druzyna_B.sila_napadu)
            szanse_formacji_dA_na_posiadanie = random.choices(
                [0,1,2,3],
                [40, 50 * self.druzyna_A.liczba_obroncow, 10 * self.druzyna_A.liczba_pomocnikow, 0]
            )[0] 
            szanse_formacji_dB_na_posiadanie = random.choices(
                [0,1,2,3],
                [0, 0, 20 * self.druzyna_B.liczba_pomocnikow, 80 * self.druzyna_B.liczba_napastnikow]
            )[0]
        elif strefa == 2:
            um_druzyna_A = round(0.8 * self.druzyna_A.sila_obrony + 0.2 * self.druzyna_A.sila_pomocy)
            um_druzyna_B = round(0.5 * self.druzyna_B.sila_pomocy + 0.5 * self.druzyna_B.sila_napadu)
            szanse_formacji_dA_na_posiadanie = random.choices(
                [0,1,2,3],
                [0, 80 * self.druzyna_A.liczba_obroncow, 20 * self.druzyna_A.liczba_pomocnikow, 0]
            )[0] 
            szanse_formacji_dB_na_posiadanie = random.choices(
                [0,1,2,3],
                [0, 0, 50 * self.druzyna_B.liczba_pomocnikow, 50 * self.druzyna_B.liczba_napastnikow]
            )[0]
        elif strefa == 3:
            um_druzyna_A = round(0.3 * self.druzyna_A.sila_obrony + 0.6 * self.druzyna_A.sila_pomocy + 0.1 * self.druzyna_A.sila_napadu)
            um_druzyna_B = round(0.1 * self.druzyna_B.sila_obrony + 0.7 * self.druzyna_B.sila_pomocy + 0.2 * self.druzyna_B.sila_napadu)
            szanse_formacji_dA_na_posiadanie = random.choices(
                [0,1,2,3],
                [0, 30 * self.druzyna_A.liczba_obroncow, 60 * self.druzyna_A.liczba_pomocnikow, 10 * self.druzyna_A.liczba_napastnikow]
            )[0] 
            szanse_formacji_dB_na_posiadanie = random.choices(
                [0,1,2,3],
                [0, 10 * self.druzyna_B.liczba_obroncow, 70 * self.druzyna_B.liczba_pomocnikow, 20 * self.druzyna_B.liczba_napastnikow]
            )[0]
        elif strefa == 4:
            um_druzyna_A = round(0.1 * self.druzyna_A.sila_obrony + 0.7 * self.druzyna_A.sila_pomocy + 0.2 * self.druzyna_A.sila_napadu)
            um_druzyna_B = round(0.3 * self.druzyna_B.sila_obrony + 0.6 * self.druzyna_B.sila_pomocy + 0.1 * self.druzyna_B.sila_napadu)
            szanse_formacji_dA_na_posiadanie = random.choices(
                [0,1,2,3],
                [0, 10 * self.druzyna_A.liczba_obroncow, 70 * self.druzyna_A.liczba_pomocnikow, 20 * self.druzyna_A.liczba_napastnikow]
            )[0]
            szanse_formacji_dB_na_posiadanie = random.choices(
                [0,1,2,3],
                [0, 30 * self.druzyna_B.liczba_obroncow, 60 * self.druzyna_B.liczba_pomocnikow, 10 * self.druzyna_B.liczba_napastnikow]
            )[0] 
        elif strefa == 5:
            um_druzyna_A = round(0.5 * self.druzyna_A.sila_pomocy + 0.5 * self.druzyna_A.sila_napadu)
            um_druzyna_B = round(0.8 * self.druzyna_B.sila_obrony + 0.2 * self.druzyna_B.sila_pomocy)
            szanse_formacji_dA_na_posiadanie = random.choices(
                [0,1,2,3],
                [0, 0, 50 * self.druzyna_A.liczba_pomocnikow, 50 * self.druzyna_A.liczba_napastnikow]
            )[0]
            szanse_formacji_dB_na_posiadanie = random.choices(
                [0,1,2,3],
                [0, 80 * self.druzyna_B.liczba_obroncow, 20 * self.druzyna_B.liczba_pomocnikow, 0]
            )[0] 
        elif strefa == 6:
            um_druzyna_A = round(0.2 * self.druzyna_A.sila_pomocy + 0.8 * self.druzyna_A.sila_napadu)
            um_druzyna_B = round(0.4 * self.druzyna_B.sila_bramkarza + 0.5 * self.druzyna_B.sila_obrony + 0.1 * self.druzyna_B.sila_pomocy) 
            szanse_formacji_dA_na_posiadanie = random.choices(
                [0,1,2,3],
                [0, 0, 20 * self.druzyna_A.liczba_pomocnikow, 80 * self.druzyna_A.liczba_napastnikow]
            )[0]
            szanse_formacji_dB_na_posiadanie = random.choices(
                [0,1,2,3],
                [40, 50 * self.druzyna_B.liczba_obroncow, 10 * self.druzyna_B.liczba_pomocnikow, 0]
            )[0]
            
        roznica_umiejetnosci = max(-24, min(24, um_druzyna_A - um_druzyna_B))
        
        #wybierz ktore udzialy na podstawie posiadanie pilki
        if posiadanie_pilki:
            podstawowy_wsp_odbioru = ((12 - roznica_umiejetnosci / 2) + 3 * strefa) if roznica_umiejetnosci > 0 else (12 - roznica_umiejetnosci + 3 * strefa)
            self.formacja_przy_pilce = szanse_formacji_dA_na_posiadanie
        else:
            podstawowy_wsp_odbioru = ((12 + roznica_umiejetnosci / 2) + 3 * (7 - strefa)) if roznica_umiejetnosci < 0 else (12 + roznica_umiejetnosci + 3 * (7 - strefa))
            self.formacja_przy_pilce = szanse_formacji_dB_na_posiadanie
            
        #kara dla hurraofensywnego nastawienia
        if nastawienie == 1:
            if posiadanie_pilki and (self.strefa_aktywna == 5 or self.strefa_aktywna == 6 or self.formacja_przy_pilce == 3):
                podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 3)
            elif not posiadanie_pilki and (self.strefa_aktywna == 1 or self.strefa_aktywna == 2 or self.formacja_przy_pilce == 3):
                podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 3)
        elif nastawienie == 2:
            if posiadanie_pilki and (self.strefa_aktywna == 5 or self.strefa_aktywna == 6 or self.formacja_przy_pilce == 3):
                podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 1)
            elif not posiadanie_pilki and (self.strefa_aktywna == 1 or self.strefa_aktywna == 2 or self.formacja_przy_pilce == 3):
                podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 1)

        #Zmiana szans na przejęcie w obronie kosztem mniejszych szans na przejęcie w ataku jeżeli ustawienie defensywne
        if nastawienie_przeciwnej == 4:
            # Wieksza szansa na strate w ataku jeżeli przeciwnik gra defensywnie
            if posiadanie_pilki and (self.strefa_aktywna == 5 or self.strefa_aktywna == 6):
                podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 3)
            elif not posiadanie_pilki and (self.strefa_aktywna == 1 or self.strefa_aktywna == 2):
                podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 3)
            # Mniejsza szansa na strate w obronie jeżeli przeciwnik gra defensywnie
            if posiadanie_pilki and (self.strefa_aktywna == 1 or self.strefa_aktywna == 2):
                podstawowy_wsp_odbioru = max(0, podstawowy_wsp_odbioru - 3)
            elif not posiadanie_pilki and (self.strefa_aktywna == 5 or self.strefa_aktywna == 6):
                podstawowy_wsp_odbioru = max(0, podstawowy_wsp_odbioru - 3)
        elif nastawienie_przeciwnej == 5:
            # Wieksza szansa na strate w ataku jeżeli przeciwnik gra defensywnie
            if posiadanie_pilki and (self.strefa_aktywna == 5 or self.strefa_aktywna == 6):
                podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 7)
            elif not posiadanie_pilki and (self.strefa_aktywna == 1 or self.strefa_aktywna == 2):
                podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 7)
            # Mniejsza szansa na strate w obronie jeżeli przeciwnik gra defensywnie
            if posiadanie_pilki and (self.strefa_aktywna == 1 or self.strefa_aktywna == 2):
                podstawowy_wsp_odbioru = max(0, podstawowy_wsp_odbioru - 7)
            elif not posiadanie_pilki and (self.strefa_aktywna == 5 or self.strefa_aktywna == 6):
                podstawowy_wsp_odbioru = max(0, podstawowy_wsp_odbioru - 7)

        # Wysoki / niski pressing - przesun szanse z obrony do ataku bądź odwrotnie
        # Wysoki
        if pressing_przeciwnika == 1:
            if posiadanie_pilki:
                if self.strefa_aktywna <= 3:
                    podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 3)
                else:
                    podstawowy_wsp_odbioru = max(0, podstawowy_wsp_odbioru - 3)
            elif not posiadanie_pilki:
                if self.strefa_aktywna <= 3:
                    podstawowy_wsp_odbioru = max(0, podstawowy_wsp_odbioru - 3)
                else:
                    podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 3)
        # Niski
        elif pressing_przeciwnika == 3:
            if posiadanie_pilki:
                if self.strefa_aktywna <= 3:
                    podstawowy_wsp_odbioru = max(0, podstawowy_wsp_odbioru - 3)
                else:
                    podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 3)
            elif not posiadanie_pilki:
                if self.strefa_aktywna <= 3:
                    podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 3)
                else:
                    podstawowy_wsp_odbioru = max(0, podstawowy_wsp_odbioru - 3)

        #Ostre/łagodne wślizgi
        if wslizgi_przeciwnika == 1:
            podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 4)
        elif wslizgi_przeciwnika == 3:
            podstawowy_wsp_odbioru = max(0, podstawowy_wsp_odbioru - 3)

        # Krycie indywidualne - silniejsze kiedy wiecej zawodnikow
        if krycie_przeciwnika == 2:
            dH = [self.druzyna_A.liczba_obroncow, self.druzyna_A.liczba_pomocnikow, self.druzyna_A.liczba_napastnikow]
            dA = [self.druzyna_B.liczba_obroncow, self.druzyna_B.liczba_pomocnikow, self.druzyna_B.liczba_napastnikow]
            if self.strefa_aktywna == 1:
                aktywator = True if (posiadanie_pilki and dH[0] > dA[2]) or (not posiadanie_pilki and dA[2] > dH[0]) else False
            elif self.strefa_aktywna == 2:
                aktywator = True if (posiadanie_pilki and (dH[0] + dH[1]) > (dA[1] + dA[2])) or (not posiadanie_pilki and (dA[1] + dA[2]) > (dH[0] + dH[1])) else False
            elif self.strefa_aktywna == 3:
                aktywator = True if (posiadanie_pilki and (dH[0] + dH[1]) > (dA[1] + dA[2])) or (not posiadanie_pilki and (dA[1] + dA[2]) > (dH[0] + dH[1])) else False
            elif self.strefa_aktywna == 4:
                aktywator = True if (posiadanie_pilki and (dH[1] + dH[2]) > (dA[0] + dA[1])) or (not posiadanie_pilki and (dA[0] + dA[1]) > (dH[1] + dH[2])) else False
            elif self.strefa_aktywna == 5:
                aktywator = True if (posiadanie_pilki and (dH[1] + dH[2]) > (dA[0] + dA[1])) or (not posiadanie_pilki and (dA[0] + dA[1]) > (dH[1] + dH[2])) else False
            elif self.strefa_aktywna == 6:
                aktywator = True if (posiadanie_pilki and dH[2] > dA[0]) or (not posiadanie_pilki and dA[0] > dH[2]) else False
                        
            if aktywator:
                podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 3)
            else:
                podstawowy_wsp_odbioru = max(0, podstawowy_wsp_odbioru - 3)

        # Większa szansa na stratę przy kontrataku
        if self.posiadanie_pilki and self.kontra_A > self.czas_meczu:
            if self.strefa_aktywna > 2:
                podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 10)
        elif not self.posiadanie_pilki and self.kontra_B > self.czas_meczu:
            if self.strefa_aktywna < 5:
                podstawowy_wsp_odbioru = min(100, podstawowy_wsp_odbioru + 10)

        # % akcji nie zakończonych stratą
        podstawowy_wsp_posiadania = 100 - podstawowy_wsp_odbioru
        # Szanse na dane zagranie dla obecnej przy piłce formacji
        podzial_wsp_posiadania = self.oblicz_szanse(self.formacja_przy_pilce, self.strefa_aktywna - 1 if self.posiadanie_pilki else 7 - self.strefa_aktywna - 1)
        # Proporcjonalna zamiana ww szans w odniesieniu do % akcji, które nie będą stratą
        wsp_posiadania_wartosci_po_zamianie = [round(element / 100 * podstawowy_wsp_posiadania, 2) for element in podzial_wsp_posiadania]
        
        wsp_posiadania_wartosci_po_zamianie.append(podstawowy_wsp_odbioru)
        
        #print(f"Minuta meczu: {round(self.czas_meczu)}. Akcja w strefie {strefa}, przy piłce druzyna {druzyna} formacja nr {self.formacja_przy_pilce}")
        
        decyzja = random.choices(
                ["przod_2", "przod_1", "bez_zmian", "tyl_1", "przerwana"],
                wsp_posiadania_wartosci_po_zamianie
            )[0]

        if decyzja == "przod_2":
            self.aktualizuj_sile(1)
            #print(f"druzyna {druzyna} zagrywa 2 strefy do przodu")
            self.strefa_aktywna = (strefa + 2) if posiadanie_pilki else (strefa - 2)
            self.czas_meczu += 1
            if posiadanie_pilki:
                self.posiadanie_druzyna_A += 1
                self.d_podania_A += 0 if self.strefa_aktywna > 6 else 1
            elif not posiadanie_pilki:
                self.posiadanie_druzyna_B += 1
                self.d_podania_B += 0 if self.strefa_aktywna < 1 else 1

            #Jeżeli długie podanie 5% na stratę
            if (posiadanie_pilki and self.strefa_aktywna <= 6) or (not posiadanie_pilki and self.strefa_aktywna >= 1):
                if posiadanie_pilki:
                    szansa_na_strate = 6 if self.sprawdz_podania(1) == 1 else 3
                elif not posiadanie_pilki:
                    szansa_na_strate = 6 if self.sprawdz_podania(2) == 1 else 3
                strata = random.choices(
                    [True, False],
                    [szansa_na_strate, 100 - szansa_na_strate]
                )[0]
                if strata:
                    self.zmien_posiadanie()
            elif self.strefa_aktywna < 1:
                self.oddaj_strzal(2)
            elif self.strefa_aktywna > 6:
                self.oddaj_strzal(1)
            elif (self.strefa_aktywna < 3 and not self.posiadanie_pilki) or (self.strefa_aktywna > 4 and self.posiadanie_pilki):
                self.sprawdz_offside(1 if self.posiadanie_pilki else 2, 'long')
        elif decyzja == "przod_1":
            self.aktualizuj_sile(0.7)
            #print(f"druzyna {druzyna} zagrywa 1 strefe do przodu")
            self.strefa_aktywna = (strefa + 1) if posiadanie_pilki else (strefa - 1)
            self.czas_meczu += 0.7
            if posiadanie_pilki:
                self.posiadanie_druzyna_A += 0.7
                self.podania_A += 0 if self.strefa_aktywna > 6 else 1
            elif not posiadanie_pilki:
                self.posiadanie_druzyna_B += 0.7
                self.podania_B += 0 if self.strefa_aktywna < 1 else 1
                
            if self.strefa_aktywna < 1:
                self.oddaj_strzal(2)
            elif self.strefa_aktywna > 6:
                self.oddaj_strzal(1)
            elif (self.strefa_aktywna < 3 and not self.posiadanie_pilki) or (self.strefa_aktywna > 4 and self.posiadanie_pilki):
                self.sprawdz_offside(1 if self.posiadanie_pilki else 2, 'short')
        elif decyzja == "bez_zmian":
            self.aktualizuj_sile(0.3)
            #print(f"druzyna {druzyna} zostaje w obecnej strefie")
            self.czas_meczu += 0.3
            self.czas_doliczony += 0.06
            if posiadanie_pilki:
                self.posiadanie_druzyna_A += 0.3
                self.podania_A += 0 if self.strefa_aktywna > 6 else 1
            elif not posiadanie_pilki:
                self.posiadanie_druzyna_B += 0.3
                self.podania_B += 0 if self.strefa_aktywna < 1 else 1
        elif decyzja == "tyl_1":
            self.aktualizuj_sile(0.6)
            #print(f"druzyna {druzyna} zagrywa 1 strefe do tylu")
            self.strefa_aktywna = (strefa - 1) if posiadanie_pilki else (strefa + 1)
            self.czas_meczu += 0.5
            self.czas_doliczony += 0.07
            if posiadanie_pilki:
                self.posiadanie_druzyna_A += 0.5
                self.podania_A += 0 if self.strefa_aktywna > 6 else 1
            elif not posiadanie_pilki:
                self.posiadanie_druzyna_B += 0.5
                self.podania_B += 0 if self.strefa_aktywna < 1 else 1
        elif decyzja == "przerwana":
            self.aktualizuj_sile(0.2)
            self.czas_meczu += 0.2
            self.czas_doliczony += 0.12
            if posiadanie_pilki:
                self.posiadanie_druzyna_A += 0.2
            elif not posiadanie_pilki:
                self.posiadanie_druzyna_B += 0.2
            self.sprawdz_czy_udany_odbior()

    def zmien_posiadanie(self):
        self.posiadanie_pilki = not self.posiadanie_pilki
        
    def czy_padl_gol(self, druzyna):
        if druzyna == 1:
            sila_strzalu = self.druzyna_A.sila_napadu if self.formacja_przy_pilce == 3 else self.druzyna_A.sila_pomocy * 2 / 3
            szansa = sila_strzalu / (sila_strzalu + self.druzyna_B.sila_bramkarza + (100 - sila_strzalu) * 2)
        elif druzyna == 2:
            sila_strzalu = self.druzyna_B.sila_napadu if self.formacja_przy_pilce == 3 else self.druzyna_B.sila_pomocy * 2 / 3
            szansa = sila_strzalu / (sila_strzalu + self.druzyna_A.sila_bramkarza + (100 - sila_strzalu) * 2)
        goal = random.choices(
                [True, False],
                [szansa, 1 - szansa]
            )[0]
        return goal
        
    def oddaj_strzal(self, druzyna):
        dr = "pierwsza" if druzyna == 1 else "druga"
        nastawienie = self.sprawdz_nastawienie(druzyna)
        # jezeli napastnik i jezeli strefa
        if self.formacja_przy_pilce == 3:
            if self.strefa_aktywna == 1 or self.strefa_aktywna == 6:
                if nastawienie == 1:
                    szanse_na_strzal = [78,20,2]
                elif nastawienie == 2:
                    szanse_na_strzal = [76,18,6]
                else:
                    szanse_na_strzal = [75,15,10]
            else:
                if nastawienie == 1:
                    szanse_na_strzal = [48,40,12]
                elif nastawienie == 2:
                    szanse_na_strzal = [46,38,16]
                else:
                    szanse_na_strzal = [45,35,20]
        else:
            if self.strefa_aktywna == 1 or self.strefa_aktywna == 6:
                if nastawienie == 1:
                    szanse_na_strzal = [53,35,12]
                elif nastawienie == 2:
                    szanse_na_strzal = [51,33,16]
                else:
                    szanse_na_strzal = [50,30,20]
            else:
                if nastawienie == 1:
                    szanse_na_strzal = [33,35,32]
                elif nastawienie == 2:
                    szanse_na_strzal = [31,33,36]
                else:
                    szanse_na_strzal = [30,30,40]
        #groźniejsze strzały, jeżeli przeciwnik gra z pułapką offsidową
        if (druzyna == 1 and self.druzyna_B.pulapki_offsidowe == 1) or (druzyna == 2 and self.druzyna_A.pulapki_offsidowe == 1):
            szanse_na_strzal = [a + b for a, b in zip(szanse_na_strzal, [4, -2, -2])]

        outcome = random.choices(
            ["ontarget", "offtarget", "nic"],
            szanse_na_strzal
        )[0]
        if outcome == "ontarget":
            goal = self.czy_padl_gol(druzyna)
            if druzyna == 1:
                self.druzyna_A.kondycja_napadu = 0.995 * self.druzyna_A.kondycja_napadu
                self.druzyna_B.kondycja_bramkarza = 0.97 * self.druzyna_B.kondycja_bramkarza
                if goal:
                    # print(f"GOOOOOOOOOL dla druzyna {dr} w {round(self.czas_meczu)} min")
                    self.wynik_A += 1
                    self.dodaj_bramke(1)
                    self.strefa_aktywna = 3
                    self.posiadanie_pilki = False
                else:
                    #print(f"strzal celny dla druzyna {dr}")
                    self.strefa_aktywna = random.randint(5, 6)
                    self.posiadanie_pilki = random.choice([True, False])
                self.strzaly_A += 1
                self.strzalyc_A += 1
            elif druzyna == 2:
                self.druzyna_B.kondycja_napadu = 0.995 * self.druzyna_B.kondycja_napadu
                self.druzyna_A.kondycja_bramkarza = 0.97 * self.druzyna_A.kondycja_bramkarza
                if goal:
                    # print(f"GOOOOOOOOOL dla druzyna {dr} w {round(self.czas_meczu)} min")
                    self.wynik_B += 1
                    self.dodaj_bramke(2)
                    self.strefa_aktywna = 4
                    self.posiadanie_pilki = True
                else:
                    #print(f"strzal celny dla druzyna {dr}")
                    self.strefa_aktywna = random.randint(5, 6)
                    self.posiadanie_pilki = random.choice([True, False])
                self.strzaly_B += 1
                self.strzalyc_B += 1
        elif outcome == "offtarget":
            if druzyna == 1:
                self.druzyna_A.kondycja_napadu = 0.995 * self.druzyna_A.kondycja_napadu
                self.druzyna_B.kondycja_bramkarza = 0.99 * self.druzyna_B.kondycja_bramkarza
                #print(f"strzal niecelny dla druzyna {dr}")
                self.strefa_aktywna = 6
                self.posiadanie_pilki = False
                self.strzaly_A += 1
            elif druzyna == 2:
                self.druzyna_B.kondycja_napadu = 0.995 * self.druzyna_B.kondycja_napadu
                self.druzyna_A.kondycja_bramkarza = 0.99 * self.druzyna_A.kondycja_bramkarza
                #print(f"strzal niecelny dla druzyna {dr}")
                self.strefa_aktywna = 1
                self.posiadanie_pilki = True
                self.strzaly_B += 1
        elif outcome == "nic":
            if druzyna == 1:
                self.druzyna_A.kondycja_pomocy = 0.995 * self.druzyna_A.kondycja_pomocy
                #print(f"nieudana akcja ofensywna dla {dr}")
                self.strefa_aktywna = random.randint(4, 6)
                self.posiadanie_pilki = random.choice([True, False])
            elif druzyna == 2:
                self.druzyna_B.kondycja_pomocy = 0.995 * self.druzyna_B.kondycja_pomocy
                #print(f"nieudana akcja ofensywna dla {dr}")
                self.strefa_aktywna = random.randint(1, 3)
                self.posiadanie_pilki = random.choice([True, False])

    def sprawdz_nastawienie(self, druzyna):
        if druzyna == 1:
            nastawienie = self.druzyna_A.nastawienie
        elif druzyna == 2:
            nastawienie = self.druzyna_B.nastawienie
        return nastawienie
    
    def sprawdz_podania(self, druzyna):
        if druzyna == 1:
            podania = self.druzyna_A.dlugosc_podan
        elif druzyna == 2:
            podania = self.druzyna_B.dlugosc_podan
        return podania
    
    def sprawdz_pressing(self, druzyna):
        if druzyna == 1:
            pressing = self.druzyna_A.pressing
        elif druzyna == 2:
            pressing = self.druzyna_B.pressing
        return pressing
    
    def sprawdz_wslizgi(self, druzyna):
        if druzyna == 1:
            wslizgi = self.druzyna_A.wslizgi
        elif druzyna == 2:
            wslizgi = self.druzyna_B.wslizgi
        return wslizgi
    
    def sprawdz_krycie(self, druzyna):
        if druzyna == 1:
            krycie = self.druzyna_A.krycie
        elif druzyna == 2:
            krycie = self.druzyna_B.krycie
        return krycie
    
    def sprawdz_kontre(self, druzyna):
        if druzyna == 1:
            kontra = self.druzyna_A.kontry
        elif druzyna == 2:
            kontra = self.druzyna_B.kontry
        return kontra
    
    def sprawdz_offside(self, druzyna, dlugosc_podania):
        offside_chances = [
            [6,4,2], #liczba obrońców i zależność wobec dlugich podan
            [3,2,1] #liczba obrońców i zależność wobec krótkich podan
        ]
        liczba_obroncow = (self.druzyna_B.liczba_obroncow if self.posiadanie_pilki else self.druzyna_A.liczba_obroncow) - 3 #Min liczba obrońców to 3
        dlugosc_podania_x = 0 if dlugosc_podania == 'long' else 1
        real_chances = offside_chances[dlugosc_podania_x][liczba_obroncow]
        # Zwieksz szanse jeżeli drużyna gra pułapki offsidowe
        if (druzyna == 1 and self.druzyna_B.pulapki_offsidowe == 1) or (druzyna == 2 and self.druzyna_A.pulapki_offsidowe == 1):
            if dlugosc_podania == 'long':
                real_chances *= 2
            else:
                real_chances *= 2

        outcome = random.choices(
            [True, False],
            [real_chances, 100 - real_chances]
        )[0]

        if outcome:
            self.zmien_posiadanie()

    def dodaj_bramke(self, druzyna):
        self.kontra_A = 0
        self.kontra_B = 0
        minuta = math.ceil(self.czas_meczu)
        if minuta > 45 and self.polowa == 1:
            reszta = minuta - 45
            minuta = f"45 + {reszta}"
        elif minuta > 90 and self.polowa > 1:
            reszta = minuta - 90
            minuta = f"90 + {reszta}"
        else:
            minuta = f"{minuta}"
        wynik = f"{self.wynik_A} - {self.wynik_B}"
        bramka = [druzyna, minuta, wynik]
        self.bramki.append(bramka)

    def dodaj_kartke(self, druzyna):
        minuta = math.ceil(self.czas_meczu)
        if minuta > 45 and self.polowa == 1:
            reszta = minuta - 45
            minuta = f"45 + {reszta}"
        elif minuta > 90 and self.polowa > 1:
            reszta = minuta - 90
            minuta = f"90 + {reszta}"
        else:
            minuta = f"{minuta}"
        self.kartki.append([druzyna, minuta])

    def rozegraj_mecz(self):
        if self.posiadanie_pilki == True:
            self.druzyna_zaczyna = True
        elif self.posiadanie_pilki == False:
            self.druzyna_zaczyna = False
            
        #premia domowa
        
            
        while self.czas_meczu < 90 + self.czas_doliczony:
            # input("Press Enter to continue...")
            self.przenies_akcje(self.strefa_aktywna, self.posiadanie_pilki)
                
            # #print(f"Czas meczu: {round(self.czas_meczu)} min")
            if self.polowa == 1:
                if self.czas_meczu >= 45 + self.czas_doliczony:
                    # print(f"Do przerwy: Druzyna_A {self.wynik_A} - {self.wynik_B} Druzyna_B\n")
                    self.posiadanie_pilki = not self.druzyna_zaczyna
                    self.strefa_aktywna = 4 if self.posiadanie_pilki else 3
                    self.czas_meczu = 45
                    self.czas_doliczony = 0
                    self.polowa = 2 
        # print(f"Wynik: {self.druzyna_A.nazwa} {self.wynik_A} - {self.wynik_B} {self.druzyna_B.nazwa}\n")
        # print(f"Strzaly: {self.druzyna_A.nazwa} {self.strzaly_A} ({self.strzalyc_A}) - ({self.strzalyc_B}) {self.strzaly_B} {self.druzyna_B.nazwa}\n")
        # print(f"Posiadanie: {self.druzyna_A.nazwa} {round(self.posiadanie_druzyna_A/(self.posiadanie_druzyna_A + self.posiadanie_druzyna_B) * 100)} - {round(self.posiadanie_druzyna_B/(self.posiadanie_druzyna_A + self.posiadanie_druzyna_B) * 100)} Druzyna_B\n")
        # print(f"Podania: {self.druzyna_A.nazwa} {self.podania_A} - {self.podania_B} {self.druzyna_B.nazwa}")
        # print(f"Dlugie podania: {self.druzyna_A.nazwa} {self.d_podania_A} - {self.d_podania_B} {self.druzyna_B.nazwa}")
        # print(f"Zolte kartki: {self.druzyna_A.nazwa} {self.z_kartki_A} - {self.z_kartki_B} {self.druzyna_B.nazwa}")
        # print(f"Czerwone kartki: {self.druzyna_A.nazwa} {self.cz_kartki_A} - {self.cz_kartki_B} {self.druzyna_B.nazwa}")

        druzyna_A_stats = [self.druzyna_A.nazwa, self.wynik_A, self.strzaly_A, self.strzalyc_A, round(self.posiadanie_druzyna_A/(self.posiadanie_druzyna_A + self.posiadanie_druzyna_B) * 100),
            self.podania_A + self.d_podania_A, self.z_kartki_A, self.cz_kartki_A]
        druzyna_B_stats = [self.druzyna_B.nazwa, self.wynik_B, self.strzaly_B, self.strzalyc_B, round(self.posiadanie_druzyna_B/(self.posiadanie_druzyna_B + self.posiadanie_druzyna_A) * 100),
            self.podania_B + self.d_podania_B, self.z_kartki_B, self.cz_kartki_B]
        
        druzyna_godpodarzy_stats = {
            'nazwa': self.druzyna_A.nazwa,
            'gole': self.wynik_A,
            'stracone': self.wynik_B,
            'strzaly': self.strzaly_A,
            'strzaly celne': self.strzalyc_A,
            'posiadanie': round(self.posiadanie_druzyna_A/(self.posiadanie_druzyna_A + self.posiadanie_druzyna_B) * 100),
            'podania': self.podania_A + self.d_podania_A,
            'zolte': self.z_kartki_A,
            'czerwone': self.cz_kartki_A,
            'karne': False
        }
        druzyna_gosci_stats = {
            'nazwa': self.druzyna_B.nazwa,
            'gole': self.wynik_B,
            'stracone': self.wynik_A,
            'strzaly': self.strzaly_B,
            'strzaly celne': self.strzalyc_B,
            'posiadanie': round(self.posiadanie_druzyna_B/(self.posiadanie_druzyna_A + self.posiadanie_druzyna_B) * 100),
            'podania': self.podania_B + self.d_podania_B,
            'zolte': self.z_kartki_B,
            'czerwone': self.cz_kartki_B,
            'karne': False
        }
        # bramki jako [[druzyna, minuta, wynik], ...], kartki jako [[minuta, druzyna(1 albo 2)]]
        return {'gospodarze': druzyna_godpodarzy_stats, 'goscie': druzyna_gosci_stats, 'bramki': self.bramki, 'kartki': self.kartki}

def get_formation_bonus(druzyna):
    formation, attitude, passing, pressing, tackle, cover, counters, offside_trap = druzyna[2], druzyna[9], druzyna[10], druzyna[11], druzyna[12], druzyna[13], druzyna[14], druzyna[15]
    attitude_bonus = {
        '3-5-2': [[-0.08,0.04,0.03], [-0.06,0.03,0.01], [-0.04,0.02,0], [0,0.03,-0.02], [0.02,0.02,-0.03]],
        '3-4-3': [[-0.09,0.03,0.05], [-0.06,0.02,0.02], [-0.04,0,0.02], [0,0.01,-0.02], [0.03,0,-0.04]],
        '3-3-4': [[-0.1,0.03,0.07], [-0.07,0.01,0.06], [-0.04,-0.02,0.04], [-0.02,0,0], [0,0,0]],
        '4-5-1': [[-0.04,0.03,0], [-0.01,0.02,-0.01], [0,0.02,-0.02], [0.05,0.03,-0.05], [0.1,0.03,-0.09]],
        '4-4-2': [[-0.04,0.01,0.01], [-0.01,0.01,0], [0,0,0], [0.02,0.01,-0.01], [0.06,0.01,-0.03]],
        '4-3-3': [[-0.09,0.02,0.06], [-0.05,0,0.04], [0,-0.02,0.02], [0.03,0,-0.01], [0.06,0.01,-0.04]],
        '4-2-4': [[-0.1,-0.02,0.1], [-0.07,-0.03,0.07], [0,-0.04,0.04], [0.02,-0.02,0], [0.04,0,-0.02]],
        '5-4-1': [[-0.02,0.02,-0.01], [0.01,0.01,-0.02], [0.04,0,-0.02], [0.08,0.01,-0.1], [0.12,0.02,-0.2]],
        '5-3-2': [[-0.04,0.01,0.03], [0.01,0,0.01], [0.04,-0.02,0], [0.06,0,-0.02], [0.08,0.01,-0.06]],
        '5-2-3': [[-0.08,0,0.07], [0,-0.02,0.04], [0.04,-0.04,0.02], [0.06,-0.04,0], [0.07,-0.02,-0.03]],
    }

    tactic_bonus = {
        '3-5-2': [2,3,3,1,1,1],
        '3-4-3': [3,1,3,1,2,1],
        '3-3-4': [1,2,3,1,2,1],
        '4-5-1': [2,3,2,2,1,2],
        '4-4-2': [3,2,2,2,2,1],
        '4-3-3': [2,1,2,1,1,1],
        '4-2-4': [1,1,2,1,2,2],
        '5-4-1': [3,2,1,2,1,2],
        '5-3-2': [2,3,1,2,1,2],
        '5-2-3': [1,2,1,2,2,2],
    }

    formation_best_choices = tactic_bonus[formation]
    manager_choices = [passing, pressing, tackle, cover, counters, offside_trap]

    compare = sum(x == y for x, y in zip(formation_best_choices, manager_choices))

    if compare < 2:
        bonus = 0
    elif compare == 2:
        bonus = 0.005
    elif compare == 3:
        bonus = 0.01
    elif compare == 4:
        bonus = 0.015
    elif compare == 5:
        bonus = 0.025
    elif compare == 6:
        bonus = 0.035

    final_bonus = [element + bonus for element in attitude_bonus[formation][attitude-1]]

    return final_bonus

def check_counter_formation(formationA, formationB):
    counters = {
        '3-5-2': ['3-4-3', '4-5-1'],
        '3-4-3': ['5-2-3', '4-4-2'],
        '3-3-4': ['3-5-2', '4-2-4'],
        '4-5-1': ['5-2-3', '4-3-3'],
        '4-4-2': ['5-4-1', '3-3-4'],
        '4-3-3': ['5-4-1', '3-3-4'],
        '4-2-4': ['5-3-2', '4-3-3'],
        '5-4-1': ['3-4-3', '4-5-1'],
        '5-3-2': ['3-5-2', '4-4-2'],
        '5-2-3': ['5-3-2', '4-2-4'],
    }
    # B kontruje A
    if formationA in counters.get(formationB, []):
        return 2
    # A kontruje B
    elif formationB in counters.get(formationA, []):
        return 1
    else:
        return 0
    
def check_counter_tactics(attitude, formationB):
    counters = {
        1: [3,2,1,1,1,1],
        2: [2,1,1,1,1,1],
        3: [2,2,2,1,1,2],
        4: [1,3,3,2,2,2],
        5: [2,1,3,2,2,2],
    }

    attitude_counters = counters[attitude]
    opponent_choices = [formationB[10],formationB[11],formationB[12],formationB[13],formationB[14],formationB[15]]

    compare = sum(x == y for x, y in zip(attitude_counters, opponent_choices))

    if compare < 2:
        negative_bonus = 0
    elif compare == 2:
        negative_bonus = 0.005
    elif compare == 3:
        negative_bonus = 0.01
    elif compare == 4:
        negative_bonus = 0.015
    elif compare == 5:
        negative_bonus = 0.025
    elif compare == 6:
        negative_bonus = 0.035

    return negative_bonus

def rozegraj_mecz(druzyna_A, druzyna_B, rozgrywki):
    druzyna_A = list(druzyna_A)
    druzyna_B = list(druzyna_B)
    # 1nazwa, 2formacja, 3sila_bramkarza, 4sila_obrony, 5sila_pomocy, 6sila_napadu, 7zaangazowanie_druzyny, 8sila_trenera, 9nastawienie,
    # 10dlugosc_podan, 11pressing, 12wslizgi, 13krycie, 14kontry, 15pulapki_offsidowe, 16premia_domowa, 23zolte, 24czerwone
    # Bonus dla gospodarza
    druzyna_A[16] += 0.02
    # Bonus za formacje i nastawienie
    counter_bonus = check_counter_formation(druzyna_A[2], druzyna_B[2])
    tactic_counter_A = check_counter_tactics(druzyna_A[9], druzyna_B)
    tactic_counter_B = check_counter_tactics(druzyna_B[9], druzyna_A)
    bonus_A = get_formation_bonus(druzyna_A)
    bonus_B = get_formation_bonus(druzyna_B)
    kary_A = [0,0,0]
    kary_B = [0,0,0]
    # licz kartki tylko w lidze i eu
    if rozgrywki == 'league':
        if druzyna_A[23] > 10 or druzyna_A[24] > 1:
            kara = int((druzyna_A[23] // 10) + (druzyna_A[24] / 1))
            for _ in range(kara):
                formacja = random.choices(
                    [0,1,2]
                )[0]
                kary_A[formacja] += 0.03

        if druzyna_B[23] > 10 or druzyna_B[24] > 1:
            kara = int((druzyna_B[23] // 10) + (druzyna_B[24] / 1))
            for _ in range(kara):
                formacja = random.choices(
                    [0,1,2]
                )[0]
                kary_B[formacja] += 0.03
        clear_cards(druzyna_A[1], druzyna_B[1], rozgrywki)
    elif rozgrywki == 'EU':
        if druzyna_A[23] > 3 or druzyna_A[24] > 1:
            kara = int((druzyna_A[23] // 3) + (druzyna_A[24] / 1))
            for _ in range(kara):
                formacja = random.choices(
                    [0,1,2]
                )[0]
                kary_A[formacja] += 0.03

        if druzyna_B[23] > 3 or druzyna_B[24] > 1:
            kara = int((druzyna_B[23] // 3) + (druzyna_B[24] / 1))
            for _ in range(kara):
                formacja = random.choices(
                    [0,1,2]
                )[0]
                kary_B[formacja] += 0.03
        clear_cards(druzyna_A[1], druzyna_B[1], rozgrywki)

    druzyna_A[4] *= (1 + bonus_A[0] + (0.03 if counter_bonus == 1 else 0) + tactic_counter_B - kary_A[0])
    druzyna_A[5] *= (1 + bonus_A[1] + (0.03 if counter_bonus == 1 else 0) + tactic_counter_B - kary_A[1])
    druzyna_A[6] *= (1 + bonus_A[2] + (0.03 if counter_bonus == 1 else 0) + tactic_counter_B - kary_A[2])
    druzyna_B[4] *= (1 + bonus_B[0] + (0.03 if counter_bonus == 2 else 0) + tactic_counter_A - kary_B[0])
    druzyna_B[5] *= (1 + bonus_B[1] + (0.03 if counter_bonus == 2 else 0) + tactic_counter_A - kary_B[1])
    druzyna_B[6] *= (1 + bonus_B[2] + (0.03 if counter_bonus == 2 else 0) + tactic_counter_A - kary_B[2])
    # druzyna = Druzyna(id, nazwa, formacja, sila_bramkarza, sila_obrony, sila_pomocy, sila_napadu,zaangazowanie, sila_trenera, nastawienie, dlugosc_podan, pressing, wslizgi, krycie, kontry, pulapki_offsidowe, premia_domowa)
    dA = Druzyna(druzyna_A)
    dB = Druzyna(druzyna_B)

    # Inicjalizacja meczu
    #mecz = Mecz(druzyna_A, druzyna_B)
    mecz = Mecz(dA, dB)

    # Rozegranie meczu
    wynik = mecz.rozegraj_mecz()

    # Jeżeli puchar to rzuty karne
    if rozgrywki == 'cup':
        if wynik['gospodarze']['gole'] == wynik['goscie']['gole']:
            karne = random.choice([True, False])
            if karne:
                wynik['gospodarze']['karne'] = True
            else:
                wynik['goscie']['karne'] = True

    return wynik
