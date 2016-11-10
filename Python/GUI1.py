from tkinter import *
import requests
import xmltodict
import csv
import time



class NSApp():
    def __init__(self, tk):
        self.tk = tk
        self.tk.title("NS App")
        self.tk.geometry("1186x890")
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
        self.knoppenFrame.place(relx=0.5, rely=0.65, anchor=CENTER)
        self.knop1 = Button(self.knoppenFrame, text="Kopen los kaartje", bg=self.NSKnopBlauw, fg=self.NSwit)
        self.knop1.grid(row=0,column=0, padx=5, pady=5)
        self.knop2 = Button(self.knoppenFrame, text="Kopen OV-Chipkaart", bg=self.NSKnopBlauw, fg=self.NSwit)
        self.knop2.grid(row=0,column=1, padx=5, pady=5)
        self.knop3 = Button(self.knoppenFrame, text="Ik wil naar het buitenland", bg=self.NSKnopBlauw, fg=self.NSwit)
        self.knop3.grid(row=0,column=2, padx=5, pady=5)
        self.knop4 = Button(self.knoppenFrame, text="Toon actuele vertrektijden", bg=self.NSKnopBlauw, fg=self.NSwit, command=self.venster2)
        self.knop4.grid(row=0,column=3, padx=5, pady=5)

    def venster2(self):
        self.knop1.grid_remove()
        self.knop2.grid_remove()
        self.knop3.grid_remove()
        self.knop4.grid_remove()
        self.Layout()


    def Layout(self):
        self.tekstFont = ('Courier',12)
        self.lengte = len(self.nummer)
        self.stop = 8
        self.verschil = 0
        self.start = 0

        self.hoofdframe= Frame(self.tk, bg=self.NSwit, bd=3)
        self.hoofdframe.place(relx=0.5, rely=0.4, anchor=CENTER)
        tekst = "Vertrektijden {}".format(self.naamLang)
        stationLabel = Label(self.hoofdframe,text=tekst,font=('Courier',16),fg="#53CCF5").grid(row=0,columnspan=3)
        if self.lengte > 8:
            self.staat = NORMAL
        else:
            self.staat = DISABLED
        self.vorigeButton = Button(self.hoofdframe,text="Vorige", state=DISABLED, command=self.vorige)
        self.vorigeButton.grid(row=1,column=0)
        tijdLabel = Label(self.hoofdframe,textvariable=self.tijd)
        tijdLabel.grid(row=1,column=1)
        self.volgendeButton = Button(self.hoofdframe,text="Volgende", state=self.staat, command=self.volgende)
        self.volgendeButton.grid(row=1,column=2)
        self.vertrektijden()

    def volgende(self):
        for volgende in range(self.stop-self.start):
            self.vertrekframe[volgende].pack_forget()
        self.start += 8
        self.stop +=8
        if self.stop > self.lengte:
            self.stop = self.lengte
            self.verschil = self.lengte-self.start
            self.volgendeButton.config(state=DISABLED)
        self.vorigeButton.config(state=NORMAL)
        self.vertrektijden()

    def vorige(self):
        if self.verschil > 0:
            for vorige in range(self.stop-self.start):
                self.vertrekframe[vorige].pack_forget()
            self.stop = self.start
            self.start -= 8
            self.verschil = 0
            self.volgendeButton.config(state=NORMAL)
        else:
            for vorige in range(self.stop-self.start):
                self.vertrekframe[vorige].pack_forget()
            self.stop -= 8
            self.start -= 8
        if self.start == 0:
            self.vorigeButton.config(state=DISABLED)
        self.vertrektijden()


    def vertrektijden(self):
        self.vertrekframe = list(range(8))
        tijdLabel = list(range(8))
        eindbestemmingLabel = list(range(8))
        vertrekspoorLabel = list(range(8))
        vervoerderLabel = list(range(8))
        treinsoortLabel = list(range(8))
        routetekstLabel = list(range(8))
        vertragingLabel = list(range(8))
        n=self.start
        m=0
        for vertrek in range(self.start,self.stop):
            if self.spoorwijziging[n] == 'true':
                self.perronFg = "red"
            elif self.spoorwijziging[n] == 'false':
                self.perronFg = "#1162BF"
            self.vertrekframe[m] = Frame(self.hoofdframe,height=120)
            self.vertrekframe[m].grid(row=2+m, columnspan=3,padx=5, pady=5)
            tijdLabel[m] = Label(self.vertrekframe[m],text=self.vertrektijd[n],fg="#1162BF",relief=RIDGE,  font=self.tekstFont).grid(row=0, column=0,sticky=W)
            eindbestemmingLabel[m] = Label(self.vertrekframe[m],text=self.eindbestemming[n],relief=RIDGE,fg="#1162BF",font=('Courier',12, 'bold'), width=30).grid(row=0,column=1, columnspan=2)
            vertrekspoorLabel[m] = Label(self.vertrekframe[m],text=self.vertrekspoor[n],relief=RIDGE,fg=self.perronFg, font=('Courier',13, 'bold'), width=10).grid(row=0,column=3, sticky=E)
            if self.vertraging[n] != "":
                vertragingLabel[m] = Label(self.vertrekframe[m],text=self.vertraging[n],relief=RIDGE,fg='red', font=('Courier',10, 'bold')).grid(row=1,column=0, sticky=W)
            vervoerderLabel[m] = Label(self.vertrekframe[m],text=self.vervoerder[n],relief=RIDGE,fg="#1162BF", font=self.tekstFont).grid(row=1,column=1, sticky=W)
            treinsoortLabel[m] = Label(self.vertrekframe[m],text=self.treinsoort[n],relief=RIDGE,fg="#1162BF", font=self.tekstFont).grid(row=1,column=2,sticky=W)
            if self.routetekst[n] != "":
                routetekstLabel[m] = Label(self.vertrekframe[m],text=self.routetekst[n],relief=RIDGE, fg="#1162BF", font=('Courier',9)).grid(row=2,column=1,columnspan=3, sticky=W)
            n+=1
            m+=1













root = Tk()
background= PhotoImage(file="background.gif")
nsapp = NSApp(root)
root.mainloop()
