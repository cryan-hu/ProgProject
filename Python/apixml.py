import requests
inloggegevens = 'jorrit.strikwerda@student.hu.nl','z0iqfPJWHGLQq-ayz7TBQyp22imLNmKZpuLidpH8HHIdT-I04zBV7g'
request = 'https://webservices.ns.nl/ns-api-avt?station=ut'
response = requests.get(request, auth=inloggegevens)
with open('vertrektijden.xml', 'w') as myXMLFile:
    myXMLFile.write(response.text)



