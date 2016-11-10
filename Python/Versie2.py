from tkinter import *
import requests
import xmltodict
import csv

class NSApp():
    def __init__(self, tk):
        self.tk = tk
        self.tk.title("NS App")
        self.tk.geometry("480x800")

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


        self.vertrektijdenCsv()
        self.labels()
        self.Layout()


    def apicall(self,url):
        inloggegevens = 'jorrit.strikwerda@student.hu.nl','z0iqfPJWHGLQq-ayz7TBQyp22imLNmKZpuLidpH8HHIdT-I04zBV7g'
        response = requests.get(url, auth=inloggegevens)
        vertrekXML = xmltodict.parse(response.text)
        return vertrekXML

    def vertrektijdenCsv(self):
        with open('vertrektijden.csv', 'w', newline='', encoding="UTF-8") as bestand:
            i = 0
            schrijf = csv.writer(bestand, delimiter=';')
            schrijf.writerow(('nummer','ritnummer', 'vertrektijd', 'eindbestemming', 'treinsoort','vertrekspoor', 'spoorwijziging', 'vervoerder'))
            #schrijf.writerow(('ritnummer', 'vertrektijd', 'vertraging', 'eindbestemming', 'treinsoort', 'vervoerder', 'vertrekspoor', 'spoorwijziging'))
            for vertrek in self.apicall('https://webservices.ns.nl/ns-api-avt?station='+self.locatieAutomaat)['ActueleVertrekTijden']['VertrekkendeTrein']:
                eindbestemming = vertrek['EindBestemming']
                ritnummer = vertrek['RitNummer']
                vertrektijd = vertrek['VertrekTijd'] # 2016-09-27T18:36:00+0200
                #vertraging =vertrek['VertrekTijd']['VertrekVertragingTekst']
                vertrektijdUurMin = vertrektijd[11:16] # 18:36
                spoor = vertrek['VertrekSpoor']['#text']
                spoorWijziging = vertrek['VertrekSpoor']['@wijziging']
                treinsoort = vertrek['TreinSoort']
                #vervoerder = vertrek['TreinSoort']['#Vervoerder']
                vervoerder = vertrek['Vervoerder']
                schrijf.writerow((i,ritnummer, vertrektijdUurMin, eindbestemming, treinsoort, spoor, spoorWijziging, vervoerder))
                i += 1
                #schrijf.writerow((ritnummer, vertrektijd, vertraging, eindbestemming, treinsoort, vervoerder, spoor, spoorWijziging))




    def labels(self):
        i = 0
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


    def Layout(self):
        self.tekstFont = ('Courier',12)
        self.lengte = len(self.nummer)

        self.hoofdframe= Frame(self.tk)
        self.hoofdframe.pack()
        stationLabel = Label(self.hoofdframe,text=self.naamLang,font=('Courier',16),fg="#53CCF5").pack()
        if self.lengte > 8:
            self.staat = NORMAL
        else:
            self.staat = DISABLED
        volgendeButton = Button(self.hoofdframe,text="Volgende", state=self.staat, command=self.volgende).pack()
        vorigeButton = Button(self.hoofdframe,text="Vorige", state=DISABLED).pack()
        self.start = 0
        self.vertrektijden()




    def volgende(self):
        for verwijder in range(8):
            self.vertrekframe[verwijder].pack_forget()
        self.start += 8
        self.vertrektijden()

    def vertrektijden(self):

        self.vertrekframe = list(range(8))
        tijdLabel = list(range(8))
        eindbestemmingLabel = list(range(8))
        vertrekspoorLabel = list(range(8))
        vervoerderLabel = list(range(8))
        treinsoortLabel = list(range(8))
        routetekstLabel = list(range(8))

        n=self.start
        m=0
        for vertrek in range(8):
            if self.spoorwijziging[n] == 'true':
                self.perronFg = "red"
            elif self.spoorwijziging[n] == 'false':
                self.perronFg = "#1162BF"
            self.vertrekframe[m] = Frame(self.hoofdframe)
            self.vertrekframe[m].pack()
            tijdLabel[m] = Label(self.vertrekframe[m],text=self.vertrektijd[n],fg="#1162BF", relief=RAISED, font=self.tekstFont).grid(row=0, column=0)
            eindbestemmingLabel[m] = Label(self.vertrekframe[m],text=self.eindbestemming[n], relief=RAISED,fg="#1162BF",font=self.tekstFont, width=30).grid(row=0,column=1, columnspan=2)
            vertrekspoorLabel[m] = Label(self.vertrekframe[m],text=self.vertrekspoor[n], relief=RAISED,fg=self.perronFg, font=self.tekstFont).grid(row=0,column=3)
            vervoerderLabel[m] = Label(self.vertrekframe[m],text=self.vervoerder[n],fg="#1162BF", relief=RAISED, font=self.tekstFont).grid(row=1,column=1)
            treinsoortLabel[m] = Label(self.vertrekframe[m],text=self.treinsoort[n], relief=RAISED,fg="#1162BF", font=self.tekstFont).grid(row=1,column=2)
            routetekstLabel[m] = Label(self.vertrekframe[m],text="Via Houten, Geldermalsen", relief=RAISED, fg="#1162BF", font=self.tekstFont).grid(row=2,column=1,columnspan=3)
            n+=1
            m+=1











root = Tk()
nsapp = NSApp(root)
root.mainloop()
