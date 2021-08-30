# Téma: Semestrální práce - #13 - Rozvržení reklam
# Autor: Daniel Stuš
# Email: stusd@students.zcu.cz
# Datum: 22.01.2021
# Verze: 1.0

import os
import csv
import baze_znalosti
import tkinter as tk


### Načte ze souboru seznam reklam
def parse_csv(soubor, list_reklam, text, seznam):

    # Kompletní cesta k souboru z názvu
    kompletni_cesta = os.path.abspath(soubor)

    # Otevři soubor pro čtení jako csv_file
    with open(kompletni_cesta, 'r', encoding="UTF-8") as csv_file:

        # csv_reader pro čtení souboru pomocí DictReader
        csv_reader = csv.DictReader(csv_file)

        # Pro každou reklamu v csv souboru ji projdi a vytvoř i její index 'num'
        for num, reklama in enumerate(csv_reader, start=1):

            # Pomocná, nově vytvořená reklama
            tmp_reklama = baze_znalosti.Reklama(reklama['Název'], reklama['Délka'], reklama['Od'],
             reklama['Do'], reklama['Priorita'])

            # Přidej do seznamu reklam
            list_reklam.append(tmp_reklama)

            # Přidej na seznam v GUI
            seznam.insert(tk.END, tmp_reklama)

            # Informuj uživatele
            text.insert(tk.END, "Načtena reklama {}: {}\n".format(num, tmp_reklama.nazev))