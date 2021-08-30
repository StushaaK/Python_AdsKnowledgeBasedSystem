# Téma: Semestrální práce - #13 - Rozvržení reklam
# Autor: Daniel Stuš
# Email: stusd@students.zcu.cz
# Datum: 22.01.2021
# Verze: 1.0

from datetime import datetime, timedelta

### Formát času hodiny:minuty:vteřiny
TIME_FORMAT = "%H:%M:%S"

### Třída popisující reklamu
### reklama má svůj název, délku,
### časový interval ve kterém musí být bezpodmínečně vysílána (interval_od a interval_do) a prioritu
class Reklama:

    ### Konstruktor reklamy
    def __init__(self, nazev, delka, interval_od, interval_do, priorita):
        self.nazev = nazev
        self.delka = datetime.strptime(delka,TIME_FORMAT) - datetime(1900, 1, 1)
        self.interval_od = datetime.strptime(interval_od,TIME_FORMAT) - datetime(1900, 1, 1)
        self.interval_do = datetime.strptime(interval_do,TIME_FORMAT) - datetime(1900, 1, 1)
        self.nejpozdeji_spustit_v = self.interval_do - self.delka
        self.priorita = float(priorita)


    ### Definuje, kdy jsou dva objekty stejné
    def __eq__(self, other):
        if (self.nazev == other.nazev and self.delka == other.delka and self.interval_od == other.interval_od and self.interval_do == other.interval_do and self.priorita == other.priorita):
            return True
        else:
            return False


            

    ### Textová reprezentace reklamy
    def __str__(self):
        return "Reklama: '" + self.nazev + "' | trvání: " + str(self.delka) + " | interval od: " + str(self.interval_od) + ", do: " + str(self.interval_do) + " | priorita: " + str(self.priorita)


### Třída reklamní blok uchovává svůj seznam reklam
### reklamní blok má svou velikost (počet reklam M, které může jeden reklamní blok obsahovat)
### a celkový čas který jeho vysílání zabere (součet délek všech reklam v bloku)
### -- Spojitě za sebou smí být promítnuto pouze M reklam
class Reklamni_blok:

    ### Konstruktor reklamního bloku
    def __init__(self, velikost):
        self.velikost = velikost
        self.reklamy = []
        self.delka = timedelta(hours=0, minutes=0, seconds=0)
        self.pocatek = timedelta(hours=0, minutes=0, seconds=0)
    
    ### Přidá reklamu do seznamu reklam a aktualizuje délku reklmního bloku
    def pridej_reklamu(self, reklama):
        self.reklamy.append(reklama)
        self.delka = self.delka + reklama.delka

    ### Odebere reklamu ze seznamu reklam a aktualizuje délku reklmního bloku
    def odstran_reklamu(self, reklama):
        self.reklamy.remove(reklama)
        self.delka - reklama.delka

    ### Vrátí aktuální počet reklam v reklamním bloku
    def vrat_pocet_reklam(self):
        return len(self.reklamy)


    ### Vrátí čas počátku další reklamy reklamního bloku
    def vrat_cas_pocatku_reklamy_bloku(self):
        return self.pocatek + self.delka