import pandas as pd
import geopandas as gpd

# load data
caseData = pd.read_csv('data/csv/cases_uk_table.csv')

# Process COVID-19 cases data for the UK UTLAs
caseData.columns = caseData.columns[:3].tolist(
) + pd.to_datetime(caseData.columns[3:], dayfirst=True).date.tolist()
caseDates = caseData.columns[3:]
caseData = caseData.rename(columns={'GSS_CD': 'code'})
caseData = caseData.drop(columns=['GSS_NM'])


def processDataUK():
    # load data
    geoCountryUK = gpd.read_file(
        'data/geometry/Countries_December_2019_Boundaries_UK_BUC.geojson')
    geoUtlaUK = gpd.read_file(
        'data/geometry/Counties_and_Unitary_Authorities_December_2019_Boundaries_UK_BUC.geojson')
    geoHbSct = gpd.read_file(
        'data/geometry/HeathBoards_Boundaries_Scotland_BUC.geojson')
    # geoHbWls = gpd.read_file('data/geometry/Local_Health_Boards_April_2019_Boundaries_WA_BUC.geojson')

    # Process geometry data for the UK countries
    geoCountryUK = geoCountryUK[
        ['ctry19cd', 'ctry19nm', 'geometry']
    ].rename(columns={
        'ctry19cd': 'code',
        'ctry19nm': 'name'
    })

    # Process geometry data for the UK UTLAs
    geoUtlaUK = geoUtlaUK[
        ['objectid', 'ctyua19cd', 'ctyua19nm', 'geometry']
    ].rename(columns={
        'ctyua19cd': 'code',
        'ctyua19nm': 'name'
    })

    geoUtlaUK.loc[49, 'objectid'] = '49'
    tempGeo = geoUtlaUK.loc[[48, 49], :].dissolve(by='objectid')
    geoUtlaUK.loc[48, 'name'] = 'Cornwall and Isles of Scilly'
    geoUtlaUK.loc[48, 'geometry'] = tempGeo['geometry'].values

    # Process geometry data for the Scotland health borders
    geoHbSct = geoHbSct[
        ['HBCode', 'HBName', 'geometry']
    ].rename(columns={
        'HBCode': 'code',
        'HBName': 'name'
    })

    # Process geometry data for the Northern Ireland country
    geoCountryNir = geoCountryUK[geoCountryUK['name'] == 'Northern Ireland']

    # Merge data
    caseGeoUtlaUK = geoUtlaUK.drop(
        columns=['objectid']).merge(caseData, on='code')
    caseGeoUtlaEng = caseGeoUtlaUK[pd.Series(
        [code.startswith('E') for code in caseGeoUtlaUK['code']])]
    caseGeoCountyEng = caseGeoUtlaEng.drop(columns=['code', 'name']).dissolve(
        by='countyName', aggfunc='sum').reset_index().rename(columns={'countyName': 'name'})
    caseGeoCountyWls = caseGeoUtlaUK[pd.Series([code.startswith(
        'W') for code in caseGeoUtlaUK['code']])].drop(columns=['code', 'countyName'])
    caseGeoCountryNir = geoCountryNir.merge(
        caseData, on='code').drop(columns=['code', 'countyName'])
    caseGeoHbSct = geoHbSct.merge(caseData, on='code').drop(
        columns=['code', 'countyName'])
    # caseGeoHbWa = geoHbWls.merge(caseData, on='code').drop(columns=['code', 'countyName'])
    caseGeoUK = caseGeoCountyEng.append(
        caseGeoCountyWls, ignore_index=True).append(
        caseGeoHbSct, ignore_index=True).append(
        caseGeoCountryNir, ignore_index=True)
    caseGeoUK.iloc[:, 2:] = caseGeoUK.iloc[:, 2:].astype(float)
    return caseGeoUK


def processDataLdn():
    # load data
    geoBoroLdn = gpd.read_file(
        'data/geometry/Counties_and_Unitary_Authorities_December_2019_Boundaries_London_BFC.geojson')

    # Process geometry data for the London boroughs
    geoBoroLdn = geoBoroLdn[
        ['ctyua19cd', 'ctyua19nm', 'geometry']
    ].rename(columns={
        'ctyua19cd': 'code',
        'ctyua19nm': 'name'
    })

    # Merge data
    caseGeoBoroLdn = geoBoroLdn.merge(caseData, on='code').drop(
        columns=['code', 'countyName'])
    caseGeoBoroLdn.iloc[:, 2:] = caseGeoBoroLdn.iloc[:, 2:].astype(float)
    return caseGeoBoroLdn


def getData(loc):
    loc = loc.lower()
    if loc == 'uk':
        return caseDates, processDataUK()
    if loc == 'london':
        return caseDates, processDataLdn()


def getGeoIreland():
    geoCountryIrl = gpd.read_file(
        'data/geometry/Country_Boundary_Ireland_BUC.geojson')
    return geoCountryIrl
