from tkinter import *
import requests
import xmltodict
import csv
import time



class NSApp():
    def __init__(self, tk):
        self.tk = tk
        self.tk.title("NS App")
        self.tk.resizable(width=False, height=False)
        #self.tk.geometry("1186x890")
        self.tk.geometry("1024x768")
        label = Label(self.tk, image=background, text="hello")
        label.place(x=0, y=0, relwidth=1, relheight=1)


        #constanten:
        self.locatieAutomaat = 'ut' #verander voor ander station
        self.naamLang = "Utrecht Centraal"
        self.nummer = []
        self.ritnummer = []
        self.vertrektijd = []
        self.vertraging = []
        self.eindbestemming = []
        self.treinsoort = []
        self.vervoerder = []
        self.vertrekspoor = []
        self.spoorwijziging = []
        self.routetekst = []
        self.tijd = StringVar(value=time.strftime("%H:%M:%S"))
        self.NSgeel = "#fece22"
        self.NSblauw = "#002272"
        self.NSwit = "#ffffff"
        self.NSKnopBlauw ="#003399"
        self.fontHoofdknop = 'Helvetica',11,"bold"
        self.lengteVertrek = 6

        self.vertrektijdenCsv()
        self.labels()
        self.hoofdKnoppen()
        self.updateTijd()

    def updateTijd(self):
        self.tijd.set(time.strftime("%H:%M:%S"))
        self.tk.after(1000,self.updateTijd)


    def apicall(self,url):
        inloggegevens = 'jorrit.strikwerda@student.hu.nl','z0iqfPJWHGLQq-ayz7TBQyp22imLNmKZpuLidpH8HHIdT-I04zBV7g'
        response = requests.get(url, auth=inloggegevens)
        vertrekXML = xmltodict.parse(response.text)
        return vertrekXML

    def vertrektijdenCsv(self):
        with open('vertrektijden.csv', 'w', newline='', encoding="UTF-8") as bestand:
            i = 0
            schrijf = csv.writer(bestand, delimiter=';')
            schrijf.writerow(('nummer','ritnummer', 'vertrektijd', 'eindbestemming', 'treinsoort','vertrekspoor', 'spoorwijziging', 'vervoerder', 'routetekst','vertraging'))
            for vertrek in self.apicall('https://webservices.ns.nl/ns-api-avt?station='+self.locatieAutomaat)['ActueleVertrekTijden']['VertrekkendeTrein']:
                eindbestemming = vertrek['EindBestemming']
                ritnummer = vertrek['RitNummer']
                vertrektijd = vertrek['VertrekTijd'] # 2016-09-27T18:36:00+0200
                try:
                    vertraging = vertrek['VertrekVertragingTekst']
                except KeyError:
                    vertraging = ""
                vertrektijdUurMin = vertrektijd[11:16] # 18:36
                spoor = vertrek['VertrekSpoor']['#text']
                spoorWijziging = vertrek['VertrekSpoor']['@wijziging']
                treinsoort = vertrek['TreinSoort']
                vervoerder = vertrek['Vervoerder']
                try:
                    routetekst = "Via {}".format(vertrek['RouteTekst'])
                except KeyError:
                    routetekst = ""

                schrijf.writerow((i,ritnummer, vertrektijdUurMin, eindbestemming, treinsoort, spoor, spoorWijziging, vervoerder,routetekst,vertraging))
                i += 1

    def labels(self):
        with open('vertrektijden.csv', 'r', newline='') as bestand:
            lees = csv.DictReader(bestand, delimiter=';')
            for rij in lees:
                self.nummer.append(int(rij['nummer']))
                self.ritnummer.append(rij['ritnummer'])
                self.vertrektijd.append(rij['vertrektijd'])
                self.eindbestemming.append(rij['eindbestemming'])
                self.treinsoort.append(rij['treinsoort'])
                self.vertrekspoor.append(rij['vertrekspoor'])
                self.spoorwijziging.append(rij['spoorwijziging'])
                self.vervoerder.append(rij['vervoerder'])
                self.routetekst.append(rij['routetekst'])
                self.vertraging.append(rij['vertraging'])

    def hoofdKnoppen(self):
        self.knoppenFrame = Frame(self.tk,bg=self.NSgeel)
        self.knoppenFrame.place(relx=0.5, rely=0.75, anchor=CENTER)
        knop1 = Button(self.knoppenFrame, text="Kopen\nlos kaartje",font=self.fontHoofdknop, bg=self.NSKnopBlauw, fg=self.NSwit, width=20, height=4)
        knop1.grid(row=0,column=0, padx=5, pady=5)
        knop2 = Button(self.knoppenFrame, text="Kopen\nOV-Chipkaart",font=self.fontHoofdknop, bg=self.NSKnopBlauw, fg=self.NSwit, width=20, height=4)
        knop2.grid(row=0,column=1, padx=5, pady=5)
        knop3 = Button(self.knoppenFrame, text="Ik wil naar\nhet buitenland",font=self.fontHoofdknop, bg=self.NSKnopBlauw, fg=self.NSwit, width=20, height=4)
        knop3.grid(row=0,column=2, padx=5, pady=5)
        knop4 = Button(self.knoppenFrame, text="Toon actuele\nvertrektijden",font=self.fontHoofdknop, bg=self.NSKnopBlauw, fg=self.NSwit, command=self.venster2, width=20, height=4)
        knop4.grid(row=0,column=3, padx=5, pady=5)

    def venster2(self):
        self.knoppenFrame.place_forget()
        self.terugKnop = Button(self.tk, text="Terug", font=self.fontHoofdknop, bg=self.NSKnopBlauw, fg=self.NSwit, command=self.terug)
        self.terugKnop.pack(pady=18, side=LEFT)
        self.Layout()

    def terug(self):
        self.hoofdframe.pack_forget()
        self.terugKnop.pack_forget()
        self.hoofdKnoppen()


    def Layout(self):
        self.tekstFont = ('Courier',12)
        self.lengte = len(self.nummer)
        self.stop = self.lengteVertrek
        self.verschil = 0
        self.start = 0

        self.hoofdframe= Frame(self.tk, bg=self.NSblauw,width=400, height=400)
        self.hoofdframe.pack(pady=(60, 120), side=TOP, expand=True, fill=Y)
        self.bovenframe = Frame(self.hoofdframe,bg=self.NSblauw)
        self.bovenframe.grid(row=0,columnspan=4,padx=5, pady=5)
        tekst = "Vertrektijden {}".format(self.naamLang)
        stationLabel = Label(self.bovenframe,text=tekst,font=('Courier',17,"bold"),fg=self.NSwit,bg=self.NSblauw).grid(row=0,columnspan=3)
        if self.lengte > self.lengteVertrek:
            self.staat = NORMAL
        else:
            self.staat = DISABLED
        self.vorigeButton = Button(self.bovenframe,text="Vorige", state=DISABLED, command=self.vorige, fg=self.NSwit, bg=self.NSblauw)
        self.vorigeButton.grid(row=1,column=0)
        tijdLabel = Label(self.bovenframe,textvariable=self.tijd, fg=self.NSwit, bg=self.NSblauw)
        tijdLabel.grid(row=1,column=1)
        self.volgendeButton = Button(self.bovenframe,text="Volgende", state=self.staat, command=self.volgende, fg=self.NSwit, bg=self.NSblauw)
        self.volgendeButton.grid(row=1,column=2)
        self.vertrektijden()

    def volgende(self):
        for volgende in range(self.stop-self.start):
            self.vertrekframe[volgende].grid_remove()
        self.start += self.lengteVertrek
        self.stop +=self.lengteVertrek
        if self.stop > self.lengte:
            self.stop = self.lengte
            self.verschil = self.lengte-self.start
            self.volgendeButton.config(state=DISABLED)
        self.vorigeButton.config(state=NORMAL)
        self.vertrektijden()

    def vorige(self):
        if self.verschil > 0:
            for vorige in range(self.stop-self.start):
                self.vertrekframe[vorige].grid_remove()
            self.stop = self.start
            self.start -=self.lengteVertrek
            self.verschil = 0
            self.volgendeButton.config(state=NORMAL)
        else:
            for vorige in range(self.stop-self.start):
                self.vertrekframe[vorige].grid_remove()
            self.stop -= self.lengteVertrek
            self.start -= self.lengteVertrek
        if self.start == 0:
            self.vorigeButton.config(state=DISABLED)
        self.vertrektijden()


    def vertrektijden(self):
        self.vertrekframe = list(range(self.lengteVertrek))
        tijdLabel = list(range(self.lengteVertrek))
        eindbestemmingLabel = list(range(self.lengteVertrek))
        vertrekspoorLabel = list(range(self.lengteVertrek))
        vervoerderLabel = list(range(self.lengteVertrek))
        treinsoortLabel = list(range(self.lengteVertrek))
        routetekstLabel = list(range(self.lengteVertrek))
        vertragingLabel = list(range(self.lengteVertrek))
        n=self.start
        m=0
        for vertrek in range(self.start,self.stop):
            if self.spoorwijziging[n] == 'true':
                self.perronFg = "red"
            elif self.spoorwijziging[n] == 'false':
                self.perronFg = "#1162BF"
            self.vertrekframe[m] = Frame(self.hoofdframe,height=120)
            self.vertrekframe[m].grid(row=1+m, columnspan=3,padx=5, pady=5)
            tijdLabel[m] = Label(self.vertrekframe[m],text=self.vertrektijd[n],fg="#1162BF",  font=self.tekstFont).grid(row=0, column=0,sticky=W)
            eindbestemmingLabel[m] = Label(self.vertrekframe[m],text=self.eindbestemming[n],fg="#1162BF",font=('Courier',12, 'bold'), width=50).grid(row=0,column=1, columnspan=2)
            vertrekspoorLabel[m] = Label(self.vertrekframe[m],text=self.vertrekspoor[n],fg=self.perronFg, font=('Courier',13, 'bold'), width=10).grid(row=0,column=3, sticky=E)
            if self.vertraging[n] != "":
                vertragingLabel[m] = Label(self.vertrekframe[m],text=self.vertraging[n],fg='red', font=('Courier',10, 'bold')).grid(row=1,column=0, sticky=W)
            vervoerderLabel[m] = Label(self.vertrekframe[m],text=self.vervoerder[n],fg="#1162BF", font=self.tekstFont).grid(row=1,column=1, sticky=W)
            treinsoortLabel[m] = Label(self.vertrekframe[m],text=self.treinsoort[n],fg="#1162BF", font=self.tekstFont).grid(row=1,column=2,sticky=W)
            routetekstLabel[m] = Label(self.vertrekframe[m],text=self.routetekst[n], fg="#1162BF", font=('Courier',9)).grid(row=2,column=1,columnspan=3, sticky=W)
            n+=1
            m+=1













root = Tk()
background= PhotoImage(file="backgroundkleiner.png")
nsapp = NSApp(root)
root.mainloop()
