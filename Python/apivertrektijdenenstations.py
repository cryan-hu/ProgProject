import requests
import xmltodict

locatieAutomaat = "br"
def apicall(url):
    inloggegevens = 'jorrit.strikwerda@student.hu.nl','z0iqfPJWHGLQq-ayz7TBQyp22imLNmKZpuLidpH8HHIdT-I04zBV7g'
    response = requests.get(url, auth=inloggegevens)
    vertrekXML = xmltodict.parse(response.text)
    return vertrekXML

def vertrekUt():
    print('Dit zijn de vertrekkende treinen:')
    for vertrek in apicall('https://webservices.ns.nl/ns-api-avt?station='+locatieAutomaat)['ActueleVertrekTijden']['VertrekkendeTrein']:
        eindbestemming = vertrek['EindBestemming']
        vertrektijd = vertrek['VertrekTijd'] # 2016-09-27T18:36:00+0200
        vertrektijd = vertrektijd[11:16] # 18:36
        print('Om '+vertrektijd+' vertrekt een trein naar '+ eindbestemming)

def stations():
    for station in apicall('http://webservices.ns.nl/ns-api-stations-v2')['Stations']['Station']:
        code = station['Code']
        naamLang = station['Namen']['Lang']
        lat = station['Lat']
        lon = station['Lon']
        print('{} - {} - {} - {}'.format(code,naamLang,lat,lon))


vertrekUt()
