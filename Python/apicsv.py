import csv
import requests
import xmltodict

def apicall(url):
    inloggegevens = 'jorrit.strikwerda@student.hu.nl','z0iqfPJWHGLQq-ayz7TBQyp22imLNmKZpuLidpH8HHIdT-I04zBV7g'
    response = requests.get(url, auth=inloggegevens)
    vertrekXML = xmltodict.parse(response.text)
    return vertrekXML

def stations():
    with open('stations.csv', 'w', newline='', encoding='UTF-8') as bestand:
        schrijf = csv.writer(bestand, delimiter=';')
        schrijf.writerow(('code','naamLang','lat','lon'))
        for station in apicall('http://webservices.ns.nl/ns-api-stations-v2')['Stations']['Station']:
            code = station['Code']
            naamLang = station['Namen']['Lang']
            lat = station['Lat']
            lon = station['Lon']
            schrijf.writerow((code,naamLang,lat,lon))

stations()

