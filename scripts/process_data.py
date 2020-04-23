import pandas as pd
import geopandas as gpd

# load data
boroLdnGeo = gpd.read_file(
    'data/geometry/Counties_and_Unitary_Authorities_December_2019_Boundaries_London_BFC.geojson')
countryUKGeo = gpd.read_file(
    'data/geometry/Countries_December_2019_Boundaries_UK_BUC.geojson')
utlaUKGeo = gpd.read_file(
    'data/geometry/Counties_and_Unitary_Authorities_December_2019_Boundaries_UK_BUC.geojson')
hbScotGeo = gpd.read_file(
    'data/geometry/HeathBoards_Boundaries_Scotland_BUC.geojson')
hbWaGeo = gpd.read_file(
    'data/geometry/Local_Health_Boards_April_2019_Boundaries_WA_BUC.geojson')
countryIreGeo = gpd.read_file(
    'data/geometry/Country_Boundary_Ireland_BUC.geojson')
caseData = pd.read_csv('data/csv/cases_uk_table.csv')

# Process geometry data for the UK countries
countryUKGeo = countryUKGeo[
    ['ctry19cd', 'ctry19nm', 'geometry']
].rename(columns={
    'ctry19cd': 'code',
    'ctry19nm': 'name'
})

# Process geometry data for the London boroughs
boroLdnGeo = boroLdnGeo[
    ['ctyua19cd', 'ctyua19nm', 'geometry']
].rename(columns={
    'ctyua19cd': 'code',
    'ctyua19nm': 'name'
})

# Process geometry data for the UK UTLAs
utlaUKGeo = utlaUKGeo[
    ['objectid', 'ctyua19cd', 'ctyua19nm', 'geometry']
].rename(columns={
    'ctyua19cd': 'code',
    'ctyua19nm': 'name'
})

utlaUKGeo.loc[49, 'objectid'] = '49'
tempGeo = utlaUKGeo.loc[[48, 49], :].dissolve(by='objectid')
utlaUKGeo.loc[48, 'name'] = 'Cornwall and Isles of Scilly'
utlaUKGeo.loc[48, 'geometry'] = tempGeo['geometry'].values

# Process geometry data for the Scotland health borders
hbScotGeo = hbScotGeo[
    ['HBCode', 'HBName', 'geometry']
].rename(columns={
    'HBCode': 'code',
    'HBName': 'name'
})

# Process geometry data for the Northern Ireland country
countryNIGeo = countryUKGeo[countryUKGeo['name'] == 'Northern Ireland']

# Process COVID-19 cases data for the UK UTLAs
caseData.columns = caseData.columns[:3].tolist(
) + pd.to_datetime(caseData.columns[3:], dayfirst=True).date.tolist()
caseDates = caseData.columns[3:]
caseData = caseData.rename(columns={'GSS_CD': 'code'})
caseData = caseData.drop(columns=['GSS_NM'])

# Merge data
caseGeoBoroLdn = boroLdnGeo.merge(caseData, on='code').drop(
    columns=['code', 'countyName'])
caseGeoBoroLdn.iloc[:, 2:] = caseGeoBoroLdn.iloc[:, 2:].astype(float)

caseGeoUtlaUK = utlaUKGeo.drop(columns=['objectid']).merge(caseData, on='code')
caseGeoUtlaEng = caseGeoUtlaUK[pd.Series(
    [code.startswith('E') for code in caseGeoUtlaUK['code']])]
caseGeoCountyEng = caseGeoUtlaEng.drop(columns=['code', 'name']).dissolve(
    by='countyName', aggfunc='sum').reset_index().rename(columns={'countyName': 'name'})
caseGeoCountyWa = caseGeoUtlaUK[pd.Series([code.startswith(
    'W') for code in caseGeoUtlaUK['code']])].drop(columns=['code', 'countyName'])
caseGeoCountryNI = countryNIGeo.merge(
    caseData, on='code').drop(columns=['code', 'countyName'])
caseGeoHbScot = hbScotGeo.merge(caseData, on='code').drop(
    columns=['code', 'countyName'])
# caseGeoHbWa = hbWaGeo.merge(caseData, on='code').drop(columns=['code', 'countyName'])
caseGeoCountryUK = countryUKGeo.merge(
    caseData, on='code').drop(columns=['code', 'countyName'])
caseGeoUK = caseGeoCountyEng.append(
    caseGeoCountyWa, ignore_index=True).append(
    caseGeoHbScot, ignore_index=True).append(
    caseGeoCountryNI, ignore_index=True)
caseGeoUK.iloc[:, 2:] = caseGeoUK.iloc[:, 2:].astype(float)


def getData(loc):
    loc = loc.lower()
    if loc == 'london':
        return caseDates, caseGeoBoroLdn
    if loc == 'uk':
        return caseDates, caseGeoUK


def getGeoIreland():
    return countryIreGeo
