# Téma: Semestrální práce - #13 - Rozvržení reklam
# Autor: Daniel Stuš
# Email: stusd@students.zcu.cz
# Datum: 22.01.2021
# Verze: 1.0


### Zapíše do souboru s názvem 'soubor' výsledný seznam 'vysledny_seznam'
def zapis_do_souboru(soubor, vysledny_seznam):
    with open(soubor, 'w') as f:
        for num, reklamni_blok in enumerate(vysledny_seznam):
            print("Blok č. {}".format(num+1), file=f)
            print("Počet reklam: {}".format(reklamni_blok.vrat_pocet_reklam()), file=f)
            print("Počáteční čas bloku (od): {}".format(reklamni_blok.pocatek), file=f)
            print("Koncový čas bloku (do): {}".format(reklamni_blok.vrat_cas_pocatku_reklamy_bloku()), file=f)
            for reklama in reklamni_blok.reklamy:
                print(str(reklama), file=f)
            print("\n", file=f)


    

