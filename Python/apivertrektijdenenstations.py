import requests
import xmltodict


locatieAutomaat = "ut"
def apicall(url):
    inloggegevens = 'jorrit.strikwerda@student.hu.nl','z0iqfPJWHGLQq-ayz7TBQyp22imLNmKZpuLidpH8HHIdT-I04zBV7g'
    response = requests.get(url, auth=inloggegevens)
    vertrekXML = xmltodict.parse(response.text)
    return vertrekXML

def werkzaamheden(): #werkt niet
    print('Dit zijn de werkzaamheden en storingen:')
    for werk in apicall('https://webservices.ns.nl/ns-api-storingen?station='+locatieAutomaat)['Storingen']['Ongepland']['Storing']:
        traject = werk['Traject'] #er gaat hier iets mis -> hij ziet werk als string en niet als dict, hoe komt dit?
        print(traject)

def vertrekUt(): #werkt wel
    print('Dit zijn de vertrekkende treinen:')
    for vertrek in apicall('https://webservices.ns.nl/ns-api-avt?station='+locatieAutomaat)['ActueleVertrekTijden']['VertrekkendeTrein']:
        eindbestemming = vertrek['EindBestemming']
        vertrekTijdFull = vertrek['VertrekTijd'] # 2016-09-27T18:36:00+0200
        vertrektijd = vertrekTijdFull[11:16] # 18:36
        vertrekspoor = vertrek['VertrekSpoor']
        spoor = vertrekspoor['#text']
        spoorWijziging = vertrekspoor['@wijziging']
        if spoorWijziging == 'false':
            gewijzigd = 'Niet'
        elif spoorWijziging == 'true':
            gewijzigd = 'Wel'
        treinsoort = vertrek['TreinSoort']
        print('Om {} vertrekt een {} naar {} van spoor {}({} gewijzigd).'.format(vertrektijd,treinsoort,eindbestemming,spoor,gewijzigd))


werkzaamheden()
