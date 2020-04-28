import requests
import os

fileLinks = {
    'eng': 'https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv',
    'wls': 'http://www2.nphs.wales.nhs.uk:8080/CommunitySurveillanceDocs.nsf/61c1e930f9121fd080256f2a004937ed/77fdb9a33544aee88025855100300cab/$FILE/Rapid%20COVID-19%20surveillance%20data.xlsx',
    'sct': 'https://raw.githubusercontent.com/tomwhite/covid-19-uk-data/master/data/covid-19-cases-uk.csv',
    'nir': 'https://raw.githubusercontent.com/tomwhite/covid-19-uk-data/master/data/covid-19-indicators-uk.csv'
}


def downloadFile(fileLink, fileDir, filename):
    response = requests.get(fileLink, stream=True)
    fileExtension = '.' + fileLink.split('.')[-1]
    filePath = os.path.join(fileDir, filename + fileExtension)
    with open(filePath, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)


def retrieveData(country):
    country = country.lower()
    fileLink = fileLinks[country]
    fileDir = 'data/csv/src'
    filename = 'data_latest_' + country
    downloadFile(fileLink, fileDir, filename)
