import tkinter
import math

import logika_igre

# visina trikotnikov v sestkotniku
VISINA_TRIKOTNIKA = 3 ** (0.5) * (0.5) * logika_igre.STRANICA_SESTKOTNIKA
STRANICA_SESTKOTNIKA = logika_igre.STRANICA_SESTKOTNIKA
VELIKOST_MATRIKE = logika_igre.VELIKOST_MATRIKE

barva = 'green'

class Gui():

    def __init__(self, master):
    
        # ZAČNEMO NOVO IGRO
        self.igra = logika_igre.Igra()
        
        # PLOSCA
        self.plosca = tkinter.Canvas(master, width=VISINA_TRIKOTNIKA * 2 * VELIKOST_MATRIKE + 1
                                     , height=1.5 * STRANICA_SESTKOTNIKA * VELIKOST_MATRIKE + 0.5 * STRANICA_SESTKOTNIKA + 1)
        self.plosca.pack()

        self.plosca.bind("<Button-1>", self.plosca_klik)

        # GLAVNI MENU
        glavni_menu = tkinter.Menu(master)
        master.config(menu=glavni_menu)

        # PODMENUJI
        igra_menu = tkinter.Menu(glavni_menu, tearoff=0)
        glavni_menu.add_cascade(label="Igra", menu=igra_menu)

        velikost_menu = tkinter.Menu(glavni_menu, tearoff=0)
        glavni_menu.add_cascade(label="Velikost polja", menu=velikost_menu)


        # IZBIRE V PODMENUJIH
        igra_menu.add_command(label="Nova igra", command=self.nova_igra)
        velikost_menu.add_command(label="10x10", command=self.velikost_igralnega_polja(10))
        velikost_menu.add_command(label="15x15", command=self.velikost_igralnega_polja(15))
        velikost_menu.add_command(label="20x20", command=self.velikost_igralnega_polja(20))

        # UKAZI OB ZAGONU
        self.narisi_mrezo()
        #print(self.igra.igralno_polje)


    def narisi_sestkotnik(self, x, y):
        a = STRANICA_SESTKOTNIKA
        v = VISINA_TRIKOTNIKA
        t1 = (x, y + a * 0.5)
        t2 = (x + v, y)
        t3 = (x + 2 * v,y + (0.5) * a)
        t4 = (x + 2 * v, y + 1.5 * a)
        t5 = (x + v, y + 2 * a)
        t6 = (x, y + 1.5 * a)
        id = self.plosca.create_polygon(*t1, *t2, *t3, *t4, *t5, *t6, fill='', outline='black')
        return id

    def narisi_mrezo(self):
        '''nariše igralno polje sestavljeno iz šestkotnikov'''
        a = STRANICA_SESTKOTNIKA
        v = VISINA_TRIKOTNIKA
        for i in range(1, VELIKOST_MATRIKE + 1): # vrstica
            #preverimo sodost/lihost in tako določimo zamik prvega šestkotnika
            if i % 2 == 1:
                zacetni_x = 2
                for j in range(1, VELIKOST_MATRIKE + 1): #stolpec
                    x = zacetni_x + (j - 1) * 2 * v
                    y = (i - 1) * 1.5 * a + 2
                    self.igra.igralno_polje[i - 1][j - 1] = [self.narisi_sestkotnik(x, y), i, j, '']
            else:
                zacetni_x = v + 2
                for j in range(1, VELIKOST_MATRIKE + 1): #stolpec
                    x = zacetni_x + (j - 1) * 2 * v
                    y = (i - 1) * 1.5 * a + 2
                    self.igra.igralno_polje[i - 1][j - 1] = [self.narisi_sestkotnik(x, y), i, j, '']

        #shranimo to polje v zacetno_igralno_polje
        self.igra.zacetno_igralno_polje = [vrstica[:] for vrstica in self.igra.igralno_polje]
        # NEJ SE JEBE, TODO


        #pobarvamo prvo polje
        sredina = self.igra.igralno_polje[VELIKOST_MATRIKE // 2][VELIKOST_MATRIKE // 2] #zakaj bi moralo biti še -1? na 5x5 to ni bila sredina
        self.plosca.itemconfig(sredina[0], fill=barva)
        sredina[3]=barva
    
    def nova_igra(self):
        '''počisti ploščo in nariše novo mrežo'''
        self.plosca.delete('all')
        self.narisi_mrezo()

        self.igra.igralno_polje = self.igra.zacetno_igralno_polje
        print(self.igra.igralno_polje)

         #to je tudi treba, ja, sicer se rojevajo indeksiralne anomalije
        #ne, nekaj narobe, bljah. ko se naredi self.narisi_mrezo(), id-ji niso od 1 naprej
        
    def velikost_igralnega_polja(self, matrika):
        '''spremeni velikost igralnega polja'''
        #TODO
        #okno se mora ponovno naložiti
        #VELIKOST_MATRIKE = matrika
        #self.nova_igra()
        pass
        
    def plosca_klik(self, event):
        '''določi koordinate klika in pokliče potezo'''
        m = event.x
        n = event.y
        self.povleci_potezo(m, n)

    def povleci_potezo(self, m, n):
        #zaenkrat samo barvanje ustreznega polja
        #TODO
        id_sestkotnika = self.plosca.find_closest(m, n)[0]
        # preverimo veljavnost poteze
        if self.igra.veljavnost_poteze(id_sestkotnika) == True:
            self.plosca.itemconfig(id_sestkotnika, fill=barva)
            # zabeležimo spremembo barve
            #for vrstica in self.igra.igralno_polje:
            #    for polje in vrstica:
            #        if polje[0] == id_sestkotnika:
            #            polje[3] = barva

            vrstica = id_sestkotnika // VELIKOST_MATRIKE #v kateri se nahaja
            stolpec = id_sestkotnika % VELIKOST_MATRIKE
            self.igra.igralno_polje[vrstica][stolpec][3] = barva
            print(self.igra.igralno_polje)
            print(self.igra.zacetno_igralno_polje)

    


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("SIX")

    aplikacija = Gui(root)

    root.mainloop()
