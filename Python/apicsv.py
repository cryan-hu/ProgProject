def stations():
    with open('stations.csv', 'w', newline='') as bestand:
        schrijf = csv.writer(bestand, delimiter=';')
        schrijf.writerow(('code','naamKort','naamMiddel','naamLang','lat','lon'))
        for station in apicall('http://webservices.ns.nl/ns-api-stations-v2')['Stations']['Station']:
            code = station['Code']
            naamLang = station['Namen']['Lang']
            naamMiddel = station['Namen']['Middel']
            naamKort = station['Namen']['Kort']
            lat = station['Lat']
            lon = station['Lon']
            schrijf.writerow((code,naamKort,naamMiddel,naamLang,lat,lon))
