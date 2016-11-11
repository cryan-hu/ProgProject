from tkinter import *
import requests
import xmltodict
import csv
import time
import string


class NSApp():
    def __init__(self, tk):
        self.tk = tk
        self.tk.title("NS App")
        self.tk.resizable(width=False, height=False)
        self.tk.geometry("1024x768")
        self.achtergrond = Label(self.tk, image=backgroundStart)
        self.achtergrond.place(x=0, y=0, relwidth=1, relheight=1)

        #constanten:
        self.locatieAutomaat = 'bd' #verander naar de code van de locatie van de automaat
        self.tijd = StringVar(value=time.strftime("%H:%M:%S"))
        self.NSgeel = "#fece22"
        self.NSblauw = "#002272"
        self.NSwit = "#ffffff"
        self.NSKnopBlauw ="#003399"
        self.fontHoofdknop = 'Helvetica',11,"bold"
        self.tekstFont = ('Helvetica',12)
        self.lengteVertrek = 6
        self.toppadding = 20

        self.stations()
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
        self.reistip = []
        self.opmerkingen = []
        with open('vertrektijden.csv', 'w', newline='', encoding="UTF-8") as bestand:
            i = 0
            schrijf = csv.writer(bestand, delimiter=';')
            schrijf.writerow(('nummer','ritnummer', 'vertrektijd', 'eindbestemming', 'treinsoort','vertrekspoor', 'spoorwijziging', 'vervoerder', 'routetekst','vertraging','reistip','opmerkingen'))
            for vertrek in self.apicall('https://webservices.ns.nl/ns-api-avt?station='+self.locatie)['ActueleVertrekTijden']['VertrekkendeTrein']:
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
                try:
                    reistip= vertrek['ReisTip']
                except KeyError:
                    reistip = ""
                try:
                    opmerkingen = vertrek['Opmerkingen']['Opmerking']
                except KeyError:
                    opmerkingen = ""
                schrijf.writerow((i,ritnummer, vertrektijdUurMin, eindbestemming, treinsoort, spoor, spoorWijziging, vervoerder,routetekst,vertraging,reistip,opmerkingen))
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
                self.reistip.append(rij['reistip'])
                self.opmerkingen.append(rij['opmerkingen'])

    def hoofdKnoppen(self):
        self.knoppenFrame = Frame(self.tk,bg=self.NSgeel)
        self.knoppenFrame.place(relx=0.5, rely=0.75, anchor=CENTER)
        knop1 = Button(self.knoppenFrame, text="Kopen\nlos kaartje",font=self.fontHoofdknop, bg=self.NSKnopBlauw, fg=self.NSwit, width=20, height=4)
        knop1.grid(row=0,column=0, padx=5, pady=5)
        knop2 = Button(self.knoppenFrame, text="Kopen\nOV-Chipkaart",font=self.fontHoofdknop, bg=self.NSKnopBlauw, fg=self.NSwit, width=20, height=4)
        knop2.grid(row=0,column=1, padx=5, pady=5)
        knop3 = Button(self.knoppenFrame, text="Ik wil naar\nhet buitenland",font=self.fontHoofdknop, bg=self.NSKnopBlauw, fg=self.NSwit, width=20, height=4)
        knop3.grid(row=0,column=2, padx=5, pady=5)
        knop4 = Button(self.knoppenFrame, text="Toon actuele\nvertrektijden",font=self.fontHoofdknop, bg=self.NSKnopBlauw, fg=self.NSwit, command=self.opties, width=20, height=4)
        knop4.grid(row=0,column=3, padx=5, pady=5)

    def opties(self):
        self.achtergrond.config(image=backgroundLeeg)
        self.knoppenFrame.place_forget()
        self.naarStart = Button(self.tk,text="Terug naar beginscherm",font=self.fontHoofdknop, bg="red", fg=self.NSwit, width=20, command=self.naarStartFunctie)
        self.naarStart.place(anchor=SE,rely=1,relx=1,height=58)
        self.knoppenFrame2=Frame(self.tk,bg=self.NSgeel)
        self.knoppenFrame2.place(anchor=NW,y=self.toppadding)
        self.terugKnop2 = Button(self.knoppenFrame2,text="Terug",font=self.fontHoofdknop, bg=self.NSKnopBlauw, fg=self.NSwit, width=20, height=4,command=self.terug2)
        self.terugKnop2.pack(pady=(0,5))
        self.ditStationKnop = Button(self.knoppenFrame2,text="Toon vertrektijden\ndit station",font=self.fontHoofdknop, bg=self.NSKnopBlauw, fg=self.NSwit, width=20, height=4,command=self.ditStation)
        self.ditStationKnop.pack(pady=5)
        self.anderStationKnop = Button(self.knoppenFrame2,text="Toon vertrektijden\nander station",font=self.fontHoofdknop, bg=self.NSKnopBlauw, fg=self.NSwit, width=20, height=4, command=self.invoerFunctie)
        self.anderStationKnop.pack(pady=(5,0))

    def ditStation(self):
        self.locatie = self.locatieAutomaat
        if self.locatie.upper() in self.codes:
            self.naam = self.naamLang[self.codes.index(self.locatie.upper())]
        self.vertrektijdenCsv()
        self.labels()
        self.knoppenFrame2.place_forget()
        self.terugKnop = Button(self.tk, text="Terug", font=self.fontHoofdknop, bg=self.NSKnopBlauw, fg=self.NSwit, width=20, height=4, command=self.terug)
        self.terugKnop.place(anchor=NW,y=self.toppadding)
        self.Layout()

    def terug(self):
        self.hoofdframe.pack_forget()
        self.terugKnop.place_forget()
        self.opties()

    def terug2(self):
        self.naarStart.place_forget()
        self.achtergrond.config(image=backgroundStart)
        self.knoppenFrame2.place_forget()
        self.hoofdKnoppen()

    def terug3(self):
        self.terugKnop3.place_forget()
        self.invoerFrame.place_forget()
        self.opties()

    def terug4(self):
        self.terugKnop4.place_forget()
        self.hoofdframe.pack_forget()
        self.invoerFunctie()

    def Layout(self):
        self.lengte = len(self.nummer)
        self.stop = self.lengteVertrek
        self.verschil = 0
        self.start = 0

        self.hoofdframe= Frame(self.tk, bg=self.NSblauw, width=400, height=400)
        self.hoofdframe.pack(pady=(self.toppadding, 80), side=TOP, expand=True, fill=Y)
        self.bovenframe = Frame(self.hoofdframe,bg=self.NSblauw)
        self.bovenframe.grid(row=0,columnspan=4,padx=5, pady=5)
        tekst = "Vertrektijden {}".format(self.naam)
        stationLabel = Label(self.bovenframe,text=tekst,font=('Helvetica',18,"bold"),fg=self.NSwit,bg=self.NSblauw).grid(row=0,columnspan=3)
        if self.lengte > self.lengteVertrek:
            self.staat = NORMAL
        else:
            self.staat = DISABLED
        self.vorigeButton = Button(self.bovenframe,text="Vorige", state=DISABLED, command=self.vorige, fg=self.NSwit, bg=self.NSKnopBlauw, font=("Helvetica", 10, "bold"))
        self.vorigeButton.grid(row=1,column=0)
        tijdLabel = Label(self.bovenframe,textvariable=self.tijd, fg=self.NSwit, bg=self.NSblauw, font=("Helvetica", 10, "bold"))
        tijdLabel.grid(row=1,column=1)
        self.volgendeButton = Button(self.bovenframe,text="Volgende", state=self.staat, command=self.volgende, fg=self.NSwit, bg=self.NSKnopBlauw, font=("Helvetica", 10, "bold"))
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
        reistipLabel = list(range(self.lengteVertrek))
        opmerkingenLabel = list(range(self.lengteVertrek))
        n=self.start
        m=0
        for vertrek in range(self.start,self.stop):
            if self.spoorwijziging[n] == 'true':
                self.perronFg = "red"
            elif self.spoorwijziging[n] == 'false':
                self.perronFg = "#1162BF"
            self.vertrekframe[m] = Frame(self.hoofdframe,height=120)
            self.vertrekframe[m].grid(row=1+m, columnspan=3,padx=5, pady=5)
            tijdLabel[m] = Label(self.vertrekframe[m],text=self.vertrektijd[n],fg="#1162BF",  font=self.tekstFont, width=6).grid(row=0, column=0,sticky=W)
            eindbestemmingLabel[m] = Label(self.vertrekframe[m],text=self.eindbestemming[n],fg="#1162BF",font=('Helvetica',12, 'bold'), width=40).grid(row=0,column=1, columnspan=2)
            vertrekspoorLabel[m] = Label(self.vertrekframe[m],text=self.vertrekspoor[n],fg=self.perronFg, font=('Helvetica',13, 'bold'), width=10).grid(row=0,column=3, sticky=E)
            if self.vertraging[n] != "":
                vertragingLabel[m] = Label(self.vertrekframe[m],text=self.vertraging[n],fg='red', font=('Helvetica',10, 'bold'),width=6).grid(row=1,column=0, sticky=W)
            vervoerderLabel[m] = Label(self.vertrekframe[m],text=self.vervoerder[n],fg="#1162BF", font=self.tekstFont).grid(row=1,column=1, sticky=W)
            treinsoortLabel[m] = Label(self.vertrekframe[m],text=self.treinsoort[n],fg="#1162BF", font=self.tekstFont).grid(row=1,column=2,sticky=W)
            routetekstLabel[m] = Label(self.vertrekframe[m],text=self.routetekst[n], fg="#1162BF", font=('Helvetica',11)).grid(row=2,column=1,columnspan=3, sticky=W)
            if self.reistip[n] != "":
                reistipLabel[m] = Label(self.vertrekframe[m],text=self.reistip[n], fg="#1162BF", font=('Helvetica',10)).grid(row=3,column=1,columnspan=3, sticky=W)
            if self.opmerkingen[n] != "":
                opmerkingenLabel[m] = Label(self.vertrekframe[m],text=self.opmerkingen[n], fg="#1162BF", font=('Helvetica',10)).grid(row=4,column=1,columnspan=3, sticky=W)
            n+=1
            m+=1

    def stations(self):
        self.naamLang = []
        self.codes = []
        self.naamMiddel = []
        self.naamKort = []
        for station in self.apicall('http://webservices.ns.nl/ns-api-stations-v2')['Stations']['Station']:
            self.codes.append(station['Code'])
            self.naamLang.append(string.capwords(station['Namen']['Lang']))
            self.naamMiddel.append(string.capwords(station['Namen']['Middel']))
            self.naamKort.append(string.capwords(station['Namen']['Kort']))

    def invoerFunctie(self):
        self.knoppenFrame2.place_forget()
        self.terugKnop3 = Button(self.tk, text="Terug", font=self.fontHoofdknop, bg=self.NSKnopBlauw, fg=self.NSwit, width=20, height=4, command=self.terug3)
        self.terugKnop3.place(anchor=NW,y=self.toppadding)
        self.invoerFrame = Frame(self.tk,bg=self.NSKnopBlauw)
        self.invoerFrame.place(anchor=CENTER,relx=0.5,rely=0.5)
        self.invoerLabel = Label(self.invoerFrame,text="Voer het station waarvan u de vertrektijden wil weten in",bg=self.NSKnopBlauw,fg=self.NSwit,font=self.fontHoofdknop)
        self.invoerLabel.pack(padx=5, pady=5)
        self.waarschuwingVar = StringVar()
        self.waarschuwing = Label(self.invoerFrame,textvariable=self.waarschuwingVar, bg=self.NSKnopBlauw, fg="red",font=self.fontHoofdknop)
        self.waarschuwing.pack()
        self.stationVar = StringVar()
        self.invoer = Entry(self.invoerFrame, bg="#ffffff",font=self.fontHoofdknop, fg=self.NSKnopBlauw,textvariable=self.stationVar)
        self.invoer.pack(padx=5, pady=5,fill=X)
        self.invoer.focus_set()
        self.invoerButton = Button(self.invoerFrame,text="Bekijk vertrektijden station",bg=self.NSblauw,fg=self.NSwit,font=self.fontHoofdknop,command=self.verifieer)
        self.invoerButton.pack(padx=5, pady=5)

    def verifieer(self):
        stad = string.capwords(self.stationVar.get())
        if stad in self.naamLang:
            self.terugKnop3.place_forget()
            self.locatie = self.codes[self.naamLang.index(stad)]
            self.tussenstap()
        elif stad in self.naamMiddel:
            self.terugKnop3.place_forget()
            self.locatie = self.codes[self.naamMiddel.index(stad)]
            self.tussenstap()
        elif stad in self.naamKort:
            self.terugKnop3.place_forget()
            self.locatie = self.codes[self.naamKort.index(stad)]
            self.tussenstap()
        elif stad == "":
            self.waarschuwingVar.set("Voer een station in!")
        else:
            self.waarschuwingVar.set("Geen geldig station!")

    def tussenstap(self):
        if self.locatie.upper() in self.codes:
            self.naam = self.naamLang[self.codes.index(self.locatie.upper())]
        self.vertrektijdenCsv()
        self.labels()
        self.invoerFrame.place_forget()
        self.terugKnop4 = Button(self.tk, text="Terug", font=self.fontHoofdknop, bg=self.NSKnopBlauw, fg=self.NSwit, width=20, height=4, command=self.terug4)
        self.terugKnop4.place(anchor=NW,y=self.toppadding)
        self.Layout()

    def naarStartFunctie(self):
        self.naarStart.place_forget()
        try:
            self.hoofdframe.pack_forget()
        except:
            pass
        try:
            self.knoppenFrame2.place_forget()
        except:
            pass
        try:
            self.terugKnop4.place_forget()
        except:
            pass
        try:
            self.terugKnop3.place_forget()
        except:
            pass
        try:
            self.terugKnop.place_forget()
        except:
            pass
        try:
            self.terugKnop.place_forget()
        except:
            pass
        try:
            self.invoerFrame.place_forget()
        except:
            pass
        self.achtergrond.config(image=backgroundStart)
        self.knoppenFrame.place(relx=0.5, rely=0.75, anchor=CENTER)


root = Tk()
backgroundStart= PhotoImage(file="backgroundkleiner.png")
backgroundLeeg= PhotoImage(file="backgroundkleinerleeg.png")
nsapp = NSApp(root)
root.mainloop()
