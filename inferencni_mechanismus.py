# Téma: Semestrální práce - #13 - Rozvržení reklam
# Autor: Daniel Stuš
# Email: stusd@students.zcu.cz
# Datum: 22.01.2021
# Verze: 1.0

import baze_znalosti
import baze_dat
import csv_parser
import output
import tkinter as tk
from operator import itemgetter, attrgetter
from datetime import datetime, timedelta

### Pomocí csv_parseru, načte soubor 'jmenosouboru' který představuje csv seznam reklam a uloží jej do seznamu 'seznam' a báze dat
### a o průběhu informuje uživatele textovým výpisem do textového pole 'text'
def nacti_reklamy(jmenosouboru, text, seznam):
    csv_parser.parse_csv(jmenosouboru, baze_dat.list_reklam, text, seznam)

### Vynuluje načtený seznam reklam v bázi dat
def vynuluj_bazy_dat():
    baze_dat.list_reklam.clear()
    
### Vypíše všechny doposud načtené reklamy v textové podobě
def vypis_nactene_reklamy(text):
    if(len(baze_dat.list_reklam) == 0):
        text.insert(tk.END, "Nejsou načteny žádné reklamy\n\n")

    else:
        for reklama in baze_dat.list_reklam:
            text.insert(tk.END, str(reklama)+"\n")

### Nastaví Maximální počet reklam, které smí být za sebou (maximální počet reklam v reklamním bloku) (v bázi dat)
def nastav_pocet_spojitych_reklam(pocet):
    baze_dat.maximalni_pocet_spojitych_reklam = pocet

### Vypíše aktuálně nastavený počet reklam, které smí být za sebou
def vypis_pocet_spojitych_reklam(text):
    if(baze_dat.maximalni_pocet_spojitych_reklam == 0):
        text.insert(tk.END, "Maximální počet (spojitých) reklam v reklamním bloku nebyl doposud definován\n\n")
    else:
        text.insert(tk.END, "Maximální počet (spojitých) reklam v reklamním bloku: " + str(baze_dat.maximalni_pocet_spojitych_reklam) + "\n")

### Nastaví Minimální počet časových jednotek, které musí mezi reklamními bloky být (v bázi dat)
def nastav_pocet_casovych_jednotek(pocet):
    baze_dat.minimalne_volnych_casovych_jednotek = timedelta(seconds=pocet)

### Vypíše aktuálně nastavený počet časových jednotek
def vypis_pocet_casovych_jednotek(text):
    if(baze_dat.minimalne_volnych_casovych_jednotek == 0):
        text.insert(tk.END, "Minimální čas mezi reklamními bloky nebyl doposud definován\n\n")
    else:
        text.insert(tk.END, "Minimální čas mezi reklamními bloky: " + str(baze_dat.minimalne_volnych_casovych_jednotek) + "\n")

### Smaže reklamu v bázi dat na indexu 'index'
def smaz_reklamu(index):
    del baze_dat.list_reklam[index]

### Přidá reklamu do báze dat a do seznamu 'seznam'
def pridej_reklamu(seznam, nazev, delka, od, do, priorita):
    tmp_reklama = baze_znalosti.Reklama(nazev, delka, od, do, priorita)
    seznam.insert(tk.END, tmp_reklama)
    baze_dat.list_reklam.append(tmp_reklama)


### Hlavní algoritmus programu
### Vytváří a ohodnocuje seznamy reklam na jejichž základě vybírá reklamy do reklamních bloků
### Výsledek je uložen v bázi dat v seznamu: reklamni_bloky
def vyres(text):
    # Vymaž seznam řešení a tím případně vyčisti předchozí řešení
    baze_dat.reklamni_bloky.clear()

    # Vezmi všechny načtené reklamy a vlož je do seznamu doposud nezařazených reklam
    baze_dat.nezarazene_reklamy = baze_dat.list_reklam.copy()
    text.insert(tk.END, "Vytvářím seznam doposud nezařazených reklam...\n")

    
    # Seřaď seznam nezařazených reklam podle počátečního intervalu kdy mám být reklama vysílána.
    # Pokud jsou počáteční intervaly stejné, seřaď podle koncového intervalu
    # Pokud i ty jsou stejné seřaď podle priority sestupně
    multisort(baze_dat.nezarazene_reklamy, (('interval_od', False), ('interval_do', False), ('priorita', True)))
    text.insert(tk.END, "Seřazuji seznam doposud nezařazencýh reklam dle kritérií\n\n")

    # Číslo právě řešeného bloku
    cislo_bloku = 0

    # Offset počátku dalšího bloku
    offset_bloku = timedelta(seconds=0) + baze_dat.nezarazene_reklamy[0].interval_od

    while len(baze_dat.nezarazene_reklamy) > 0:
        # Vezmi (vyjmi) první reklamu ze seřazeného seznamu
        zkoumana_reklama = baze_dat.nezarazene_reklamy.pop(0)
        text.insert(tk.END, "Vybrána reklama {}\n".format(zkoumana_reklama))

        # Vytvoř pro ni nový reklamní blok
        novy_reklamni_blok = baze_znalosti.Reklamni_blok(baze_dat.maximalni_pocet_spojitych_reklam)

        # Zvyš čítač zpracovávaného bloku
        cislo_bloku += 1
        text.insert(tk.END, "Vytvářím pro ni {}. reklamní blok\n".format(cislo_bloku))


        # Přiřad ji do bloku
        novy_reklamni_blok.pridej_reklamu(zkoumana_reklama)
        
        # Přiřad reklamni blok do seznamu bloků
        baze_dat.reklamni_bloky.append(novy_reklamni_blok)

        # Cas počátku nového reklamního bloku
        novy_reklamni_blok.pocatek += offset_bloku

        # Pokud cas pocatku vybrane reklamy je vetsi nez mozny pocatek dalsiho bloku
        # tak dalsi blok zacina od casu sve prvni reklamy
        if (novy_reklamni_blok.pocatek < novy_reklamni_blok.reklamy[0].interval_od):
            novy_reklamni_blok.pocatek = novy_reklamni_blok.reklamy[0].interval_od

        # Pokud je překročen interval reklamy (reklamní blok začíná až po koncovém intervalu reklamy)
        # -> reklama se nevešla do žádného z časových bloků a musela být posunuta mimo svůj interval
        # -> informuj o tom uživatele
        if (novy_reklamni_blok.reklamy[0].interval_do < novy_reklamni_blok.pocatek):
            text.insert(tk.END, "Reklama {}. se nevešela do žádného předešlého časového bloku a musela být posunuta mimo svůj interval\n".format(zkoumana_reklama))

        text.insert(tk.END, "Zpracovávám {}. reklamní blok\n".format(cislo_bloku))

        # Dokud není reklamní blok naplněn, přiřazuj mu reklamy
        while novy_reklamni_blok.vrat_pocet_reklam() < novy_reklamni_blok.velikost:

            # Vytvoř seznam všech další reklam, které by mohli být v reklamním bloku s aktuálně zkoumanou reklamou
            mozne_reklamy_v_bloku = []

            # Čas počátku další reklamy = počátek předchozí reklamy bloku + její délka
            cas_pocatku = novy_reklamni_blok.vrat_cas_pocatku_reklamy_bloku()
            
            # Projdi všechny reklamy v nezařazených reklamách
            for reklama in baze_dat.nezarazene_reklamy:
                # Pokud reklama spadá intervalu reklamního bloku, přidej ji do seznamu možných reklam
                if(reklama.interval_od <= cas_pocatku and (reklama.interval_do-reklama.delka) >= cas_pocatku):
                    mozne_reklamy_v_bloku.append(reklama)
                else:
                # Seznam nezařazených reklam je seřazen, pokud tedy narazíme na první reklamu která nespadá do intervalu, můžeme hledání přerušit
                    break

            # Pokud nelze přiřadit do bloku žádnou reklamu -> přeruš přidávání reklam a založ nový blok
            if len(mozne_reklamy_v_bloku) == 0:
                text.insert(tk.END, "Do reklamního bloku nelze přiřadit žádné další reklamy\n")
                break

            # Seřad možné reklamy v bloku podle času, kdy se nejpozději musí pustit (čas do - reklama.delka)
            # Pokud je stejný, pak podle priority
            text.insert(tk.END, "Nalezeny další možné reklamy, které lze přiřadit do reklamního bloku\n"+
            "- seřazuji a ohodnocuji jejich seznam\n")
            multisort(mozne_reklamy_v_bloku, (('nejpozdeji_spustit_v', False), ('priorita', True)))

            # Vyber první reklamu v seřazeném (ohodnoceném) seznamu možných reklam
            vybrana_reklama = mozne_reklamy_v_bloku.pop(0)
            text.insert(tk.END, "Přiřazuji další reklamu do reklamního bloku: {}\n".format(vybrana_reklama))

            # Přidej ji do reklamního bloku
            novy_reklamni_blok.pridej_reklamu(vybrana_reklama)

            # Odstraň ji ze seznamu nezařazených reklam
            baze_dat.nezarazene_reklamy.remove(vybrana_reklama)

        # Vypočítej možný čas počátku dalšího reklamního bloku = konečný čas bloku před ním + minimální rozestup mezi bloky
        offset_bloku = baze_dat.reklamni_bloky[-1].vrat_cas_pocatku_reklamy_bloku() + baze_dat.minimalne_volnych_casovych_jednotek

        text.insert(tk.END, "{}. reklamní blok úspěšně zpracován\n\n".format(cislo_bloku))


    



### Umožňuje seřadit list 'xs' podle více kritérií 'specs'
def multisort(xs, specs):
    for key, reverse in reversed(specs):
        xs.sort(key=attrgetter(key), reverse = reverse)
    return xs

### Zapíše výsledek aplikace do souboru pomocí modulu output
def zapis_vysledek_do_souboru(text):
    output.zapis_do_souboru("output.txt",baze_dat.reklamni_bloky)
    text.insert(tk.END, "Výsledek byl zapsán do souboru output.txt v kořenovém adresáři programu\n\n")


