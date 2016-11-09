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


        self.vertrektijdenCsv()
    def apicall(self,url):
        inloggegevens = 'jorrit.strikwerda@student.hu.nl','z0iqfPJWHGLQq-ayz7TBQyp22imLNmKZpuLidpH8HHIdT-I04zBV7g'
        response = requests.get(url, auth=inloggegevens)
        vertrekXML = xmltodict.parse(response.text)
        return vertrekXML

    def vertrektijdenCsv(self):
        with open('vertrektijden.csv', 'w', newline='', encoding="UTF-8") as bestand:
            schrijf = csv.writer(bestand, delimiter=';')
            schrijf.writerow(('ritnummer', 'vertrektijd', 'vertraging', 'eindbestemming', 'treinsoort', 'vervoerder', 'vertrekspoor', 'spoorwijziging'))
            for vertrek in self.apicall('https://webservices.ns.nl/ns-api-avt?station='+self.locatieAutomaat)['ActueleVertrekTijden']['VertrekkendeTrein']:
                eindbestemming = vertrek['EindBestemming']
                ritnummer = vertrek['RitNummer']
                vertrektijd = vertrek['VertrekTijd'] # 2016-09-27T18:36:00+0200
                if vertrek['VertrekTijd']['VertrekVertragingTekst'] == 1:
                    print("ja")
                vertraging = "swag" #vertrek['VertrekTijd']['VertrekVertragingTekst']
                #vertrektijdUurMin = vertrektijd[11:16] # 18:36
                spoor = vertrek['VertrekSpoor']['#text']
                spoorWijziging = vertrek['VertrekSpoor']['@wijziging']
                treinsoort = vertrek['TreinSoort']
                vervoerder = 'swag2'#vertrek['TreinSoort']['Vervoerder']
                schrijf.writerow((ritnummer, vertrektijd, vertraging, eindbestemming, treinsoort, vervoerder, spoor, spoorWijziging))








root = Tk()
nsapp = NSApp(root)
root.mainloop()
