# Téma: Semestrální práce - #13 - Rozvržení reklam
# Autor: Daniel Stuš
# Email: stusd@students.zcu.cz
# Datum: 22.01.2021
# Verze: 1.0

# Tkinter -> GUI
import tkinter as tk
from tkinter import filedialog, simpledialog, ttk, messagebox
import tkinter.scrolledtext as scrolledtext

# Funkce os
import os
# Vykreslování grafu
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Inferenční mechanismus
import inferencni_mechanismus


### Hlavní třída GUI
### Využívá standardní knihovny tkinter a vytváří úvodní stránku
class Aplikace(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.zmen_stranku(UvodniStranka)

    ### Změní aktuálně zobrazovanou stránku
    def zmen_stranku(self, trida_stranky):
        nova_stranka = trida_stranky(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = nova_stranka
        self._frame.pack()

### Úvodní stránka aplikace
class UvodniStranka(tk.Frame):
    def __init__(self, master):
        inferencni_mechanismus.vynuluj_bazy_dat()
        tk.Frame.__init__(self, master)

        # Nadpis
        tk.Label(self, text="Expertní systém - Rozvržení reklam", font=("Helvetica", 18, "bold")).pack(side="top", fill="x", pady=5)

        # Tlačítka
        tk.Button(self, text="Start", width=30, height=3, command=lambda: master.zmen_stranku(Start)).pack(pady=(100,0))
        tk.Button(self, text="Informace", width=30, height=3, command=lambda: master.zmen_stranku(Informace)).pack()
        tk.Button(self, text="Ukončit", width=30, height=3, command=self.master.destroy).pack()

### Hlavní stránka aplikace
class Start(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)

        # Vytvoř Záložky
        notebook = ttk.Notebook(self)
        notebook.pack()

        # Záložky
        zalozka_hlavni = tk.Frame(notebook, width=1000, height=500)
        zalozka_reklamy = tk.Frame(notebook, width=1000, height=500)

        zalozka_hlavni.pack(fill="both", expand=True)
        zalozka_reklamy.pack(fill="both", expand=True)

        notebook.add(zalozka_hlavni, text="Hlavní")
        notebook.add(zalozka_reklamy, text="Správce reklam")

        ## --- Hlavní záložka ---
        # Menu tlačítka
        menu = tk.LabelFrame(zalozka_hlavni, text="Menu", padx=5, pady=5)
        menu.pack(side = tk.LEFT, fill="y")

        tk.Button(menu, text="Spustit", command=self.start).pack(fill="x")
        tk.Button(menu, text="Vypiš seznam reklam", command=self.vypis_nactene_reklamy).pack(fill="x")
        tk.Button(menu, text="Vypiš max. počet reklam v bloku", command=self.vypis_pocet_spojitych_reklam).pack(fill="x")
        tk.Button(menu, text="Vypiš min. počet časových jednotek", command=self.vypis_pocet_casovych_jednotek).pack(fill="x")
        self.graf_tlacitko = tk.Button(menu, text="Vykresli graf", command=self.vykresli_graf, state=tk.DISABLED)
        self.graf_tlacitko.pack(fill="x")
        tk.Button(menu, text="Zpět na úvodní stránku", command=lambda: master.zmen_stranku(UvodniStranka)).pack(fill="x")


        # Vypisovací okno
        self.txt = scrolledtext.ScrolledText(zalozka_hlavni, undo=True, width=120, height=120)
        self.txt.pack(side = tk.RIGHT, expand=True, fill="both")
        self.txt.insert(tk.END, "Začněte naplněním báze dat reklamami pomocí záložky 'SPRÁVCE REKLAM'\n\n")

        ## --- Správce reklam ---
        # Menu tlačítka
        spravcereklam_menu = tk.Frame(zalozka_reklamy,width=1000, height=120)

        tk.Button(spravcereklam_menu, text="Načti reklamy z csv souboru", command=self.nacticsv).pack(side=tk.LEFT)
        tk.Button(spravcereklam_menu, text="Smazat reklamu", command= self.smazreklamu).pack(side=tk.LEFT)

        # Seznam reklam
        seznam = tk.Frame(zalozka_reklamy)
        scrollbar = tk.Scrollbar(seznam, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(seznam, yscrollcommand=scrollbar.set)

        scrollbar.config(command=self.listbox.yview)
        
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.listbox.pack(side=tk.LEFT, fill="both", expand=True)

        # Přidání reklamy
        pridat_reklamu = tk.LabelFrame(zalozka_reklamy, text="Přidat reklamu: ", height=200)
        

        #Vstupy
        tk.Label(pridat_reklamu, text="Název").grid(row=0, sticky=tk.E)
        tk.Label(pridat_reklamu, text="Délka").grid(row=1, sticky=tk.E)
        tk.Label(pridat_reklamu, text="Od").grid(row=2, sticky=tk.E)
        tk.Label(pridat_reklamu, text="Do").grid(row=3, sticky=tk.E)
        tk.Label(pridat_reklamu, text="Priorita").grid(row=4, sticky=tk.E)

        # Vstupní pole
        self.e1 = tk.Entry(pridat_reklamu)
        self.e2 = tk.Entry(pridat_reklamu)
        self.e3 = tk.Entry(pridat_reklamu)
        self.e4 = tk.Entry(pridat_reklamu)
        self.e5 = tk.Entry(pridat_reklamu)

        # Placeholdery
        self.e1.insert(0, "Název reklamy")
        self.e2.insert(0, "00:10:00")
        self.e3.insert(0, "02:35:00")
        self.e4.insert(0, "10:58:00")
        self.e5.insert(0, "1.0")

        # Přidej vstupní pole do GUI
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)
        self.e5.grid(row=4, column=1)

        # Tlačítko přidej reklamu
        tk.Button(pridat_reklamu, text="Přidat reklamu", command=self.pridejreklamu).grid(row=5, columnspan=2, sticky=tk.E)

        # Status bar
        self.statustext = tk.StringVar()
        self.statustext.set("Reklam: " + str(len(inferencni_mechanismus.baze_dat.list_reklam)))
        status = tk.Label(zalozka_reklamy, textvariable=self.statustext, bd=1, relief=tk.SUNKEN, anchor=tk.E)

        # Přidání prvků na frame (do GUI)
        spravcereklam_menu.pack(fill="x",side = tk.TOP)
        seznam.pack(fill="both", expand=True)
        pridat_reklamu.pack(fill="x")
        status.pack(fill="x",side = tk.BOTTOM)
        
        



    ### funkce tlačítka - Započne hlavní část programu
    def start(self):

        # Zkontroluj, zda jsou načteny reklamy
        if (len(inferencni_mechanismus.baze_dat.list_reklam) == 0):
            self.txt.insert(tk.END, "Musí být přidána alespoň jedna reklama!\n" +
            "Nejprve naplňte bázi dat reklamami v záložce 'SPRÁVCE REKLAM' a poté znovu spusťe program!\n\n")
        
        else:

            # Vyzvi uživatele k zadání počtu reklam v bloku M
            self.txt.insert(tk.END, "Vyzývám uživatele k zadání počtu reklam v bloku...\n")
            max_reklam_v_bloku = simpledialog.askinteger("Počet reklam M v bloku", "Zadejte počet reklam M v bloku jako celé číslo: ")

            # Pokud uživatel zrušil zadávání, vlož výchozí hodnotu (8)
            if(max_reklam_v_bloku == None):
                self.txt.insert(tk.END, "Uživatel zrušil zadávání, nastavuji výchozí hodnotu...\n")
                max_reklam_v_bloku = 8

            inferencni_mechanismus.nastav_pocet_spojitych_reklam(max_reklam_v_bloku)
            self.txt.insert(tk.END, "Maximimální spojitý počet reklam nastaven na: " +str(max_reklam_v_bloku)+ "\n\n")


            # Vyzvi uživatele k zadání rozestupu N
            self.txt.insert(tk.END, "Vyzývám uživatele k zadání rozestupu mezi bloky...\n")
            min_rozestup = simpledialog.askinteger("Časový rozestup N", "Zadejte minimální časový rozestup N mezi bloky (ve vteřinách, celé číslo): ")

            # Pokud uživatel zrušil zadávání, vlož výchozí hodnotu (1200s = 20min)
            if(min_rozestup == None):
                self.txt.insert(tk.END, "Uživatel zrušil zadávání, nastavuji výchozí hodnotu...\n")
                min_rozestup = 1200

            inferencni_mechanismus.nastav_pocet_casovych_jednotek(min_rozestup)
            self.txt.insert(tk.END, "Minimální časový rozestup mezi bloky nastaven na: " +str(min_rozestup)+ " (s)\n\n")


            # Spust hlavní část programu v inferenčním mechanismu
            inferencni_mechanismus.vyres(self.txt)


            # Vypiš výsledek do textového pole
            self.txt.insert(tk.END, "NAVRHOVANÉ ROZDĚLENÍ REKLAM: \n" +
            "---------------------------------------------------------------------\n\n")

            # Vypiš navrhované rozdělení
            for num, reklamni_blok in enumerate(inferencni_mechanismus.baze_dat.reklamni_bloky):
                self.txt.insert(tk.END, "Blok č. {}\n".format(num+1))
                self.txt.insert(tk.END, "Počet reklam: {}\n".format(reklamni_blok.vrat_pocet_reklam()))
                self.txt.insert(tk.END, "Počáteční čas bloku (od): {}\n".format(reklamni_blok.pocatek))
                self.txt.insert(tk.END, "Koncový čas bloku (do): {}\n".format(reklamni_blok.vrat_cas_pocatku_reklamy_bloku()))
                self.txt.insert(tk.END, "Reklamy bloku: {}\n")
                for reklama in reklamni_blok.reklamy:
                    self.txt.insert(tk.END, str(reklama) + "\n")
                self.txt.insert(tk.END, "\n")

            # Aktivuj tlačítko pro vykrelsení grafu
            self.graf_tlacitko['state'] =tk.NORMAL

            # Zeptej se zda chce uživatel vykreslit graf
            if(messagebox.askyesno("Otázka", "Chcete zapsat výsledek do souboru?")):
                self.zapis_do_souboru()

            # Zeptej se zda chce uživatel vykreslit graf
            if(messagebox.askyesno("Otázka", "Chcete vykreslit graf navrhnutého rozvržení?")):
                self.vykresli_graf()

            



    ### funkce tlačítka - Načte csv soubor s reklamamy
    def nacticsv(self):
        jmenoSouboru = filedialog.askopenfilename(title="Vyberte csv soubor se seznamem reklam")
        if jmenoSouboru:
            self.txt.insert(tk.END, "Načítám seznam reklam z csv souboru\n")
            inferencni_mechanismus.nacti_reklamy(jmenoSouboru, self.txt, self.listbox)
            self.update_status_text(None)
            self.txt.insert(tk.END, "Reklamy úspěšně načteny\n\nNyní můžete pokračovat tlačítkem 'SPUSTIT'\n\n")

    ### funkce tlačítka - Smaže vybranou reklamu
    def smazreklamu(self):
        if (len(inferencni_mechanismus.baze_dat.list_reklam) == 0):
            self.txt.insert(tk.END, "Seznam reklam je prázdný!\nŽádná reklama k smazání.\n\n")
            self.update_status_text("Seznam reklam je prázdný! Žádná reklama k smazání.")

        elif(len(self.listbox.curselection()) == 0):
            return
        
        else:
            inferencni_mechanismus.smaz_reklamu(self.listbox.curselection()[0])
            self.listbox.delete(tk.ANCHOR)
    
    ### funkce tlačítka - Přidá reklamu do seznamu reklam
    def pridejreklamu(self):
        if(self.e1.get() == "" or self.e2.get() == "" or self.e3.get() == "" or self.e4.get() == "" or self.e5.get() == ""):
            self.txt.insert(tk.END, "Nelze přidat reklamu!\nProsím vyplňte všechny pole.\n\n")
            self.update_status_text("Nelze přidat reklamu! Prosím vyplňte všechny pole.")
        else:
            inferencni_mechanismus.pridej_reklamu(self.listbox, self.e1.get(), self.e2.get(), self.e3.get(), self.e4.get(), self.e5.get())
            self.txt.insert(tk.END, "Přidána reklama: "+self.e1.get()+"\n\n")
            self.update_status_text(None)



    ### funkce tlačítka - vypíše všechny načtené reklamy
    def vypis_nactene_reklamy(self):
        inferencni_mechanismus.vypis_nactene_reklamy(self.txt)

    ### funkce tlačítka - vypíše maximální počet spojitých reklam v bloku
    def vypis_pocet_spojitych_reklam(self):
        inferencni_mechanismus.vypis_pocet_spojitych_reklam(self.txt)

    ### funkce tlačítka - vypíše minimální rozestup mezi reklamnímy bloky
    def vypis_pocet_casovych_jednotek(self):
        inferencni_mechanismus.vypis_pocet_casovych_jednotek(self.txt)
        
    ### funkce tlačítka - vykreslí graf reklam    
    def vykresli_graf(self):
        graf_reklam = []
        zero = datetime(2021,1,1)


        for reklamni_blok in inferencni_mechanismus.baze_dat.reklamni_bloky:
            graf_reklam.append((reklamni_blok.pocatek + zero, reklamni_blok.delka))

        TIME_FORMAT = "%H:%M:%S"

        fig, ax= plt.subplots(num="Graf Reklam",figsize=(10,2))
        ax.broken_barh(graf_reklam, (-1, 1), facecolors='tab:blue')


        ax.margins(0)
        ax.set_yticks([])
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter(TIME_FORMAT))
        plt.xlim([timedelta(hours=0)+zero, timedelta(hours=24)+zero])
        plt.show()

    ### Zapíše výsledek do soubor a informuje o tom uživatele
    def zapis_do_souboru(self):
        inferencni_mechanismus.zapis_vysledek_do_souboru(self.txt)

    ### Aktualizuje status text na záložce správce reklam
    def update_status_text(self, text):
        if (text == None):
            self.statustext.set("Reklam: " + str(len(inferencni_mechanismus.baze_dat.list_reklam)))
        else:
            self.statustext.set(text)

### Stránka aplikace s informacemi o aplikaci
class Informace(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="Informace o programu", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Label(self, text="KIV/UZI - SEM. PRÁCE - DANIEL STUŠ").pack(fill="x")
        tk.Label(self, text="stusd@students.zcu.cz", font=('Helvetica', 10, "bold")).pack(fill="x")
        tk.Label(self, text="Program ze zadaného seznamu reklam vytvoří dle vstupních parametrů reklamní bloky a navrhne jejich rozvržení během dne.\n" +
                            "Reklamy lze zadat ručně v hlavní částí aplikace nebo lze jejich kompletní seznam načíst prostřednictvím csv souboru.\n", wraplength=400, justify="left").pack(fill="y", pady=(20,0))

        formatreklamy = tk.LabelFrame(self, text="Formát reklamy v csv souboru: ", padx=5, pady=5)
        formatreklamy.pack(padx=10, pady=10)

        tk.Label(formatreklamy, text="Název,Délka,Od,Do,Priorita").pack()
        tk.Label(formatreklamy, text="Příklad: Avon,00:10:00,08:25:00,18:32:00,0.4").pack()
        tk.Label(formatreklamy, text="Formát času musí být dodržen (hodiny:minuty:vteřiny)\nPriorita je desetinné číslo v rozmezí 0.0 až 1.0\n"
        + "Priorita 1.0 je nejvyšší a říká, že musí být daná reklama bezpodmínečně odvysílána ve stanoveném časovém rozmezí", wraplength=350, justify="left").pack(pady=(10, 0))

        tk.Label(self, text="verze 1.0").pack(fill="x")
        tk.Button(self, text="Zpět na úvodní stránku",
                  command=lambda: master.zmen_stranku(UvodniStranka)).pack(side = tk.BOTTOM, pady=(50,0))


### Vstupní bod programu
if __name__ == "__main__":
    # Hlavní okno aplikace
    app = Aplikace()

    # Název okna
    app.title("Expertní systém - Daniel Stuš")

    # Rozlišení okna
    app.geometry("1000x500")

    # Hlavní smyčka pro vykreslování GUI
    app.mainloop()