import pandas as pd
import geopandas as gpd
from util import getGroup


def loadCaseData(country):
    country = country.lower()
    caseData = pd.read_csv(
        "data/csv/cases_" + country + ".csv", header=[0, 1], index_col=[0]
    )
    caseData = caseData.transpose().reset_index()
    caseData.columns = pd.Series(
        ["name", "code"]
        + pd.to_datetime(caseData.columns[2:], dayfirst=True).date.tolist()
    )
    return caseData


def processDataUK():
    # load data
    geoCountryUK = gpd.read_file(
        "data/geometry/Countries_December_2019_Boundaries_UK_BUC.geojson"
    )
    geoUtlaUK = gpd.read_file(
        "data/geometry/Counties_and_Unitary_Authorities_December_2019_Boundaries_UK_BUC.geojson"
    )
    geoHbSct = gpd.read_file(
        "data/geometry/HeathBoards_Boundaries_Scotland_BUC.geojson"
    )
    # geoHbWls = gpd.read_file('data/geometry/Local_Health_Boards_April_2019_Boundaries_WA_BUC.geojson')
    caseEng = loadCaseData("Eng")
    caseWls = loadCaseData("Wls")
    caseSct = loadCaseData("Sct")
    caseNir = loadCaseData("Nir")
    codeGroup = getGroup()

    # process geometry data for the UK UTLAs
    geoUtlaUK = geoUtlaUK[["objectid", "ctyua19cd", "geometry"]].rename(
        columns={"ctyua19cd": "code",}
    )

    geoUtlaUK.loc[49, "objectid"] = "49"
    tempGeo = geoUtlaUK.loc[[48, 49], :].dissolve(by="objectid")
    geoUtlaUK.loc[48, "geometry"] = tempGeo["geometry"].values
    geoUtlaUK = geoUtlaUK.drop(columns="objectid")

    # process geometry data for the Scotland health borders
    geoHbSct = geoHbSct[["HBCode", "geometry"]].rename(columns={"HBCode": "code"})

    # process geometry data for the Northern Ireland country
    geoCountryUK = geoCountryUK[["ctry19cd", "ctry19nm", "geometry"]].rename(
        columns={"ctry19cd": "code", "ctry19nm": "name"}
    )
    geoCountryNir = geoCountryUK[geoCountryUK["name"] == "Northern Ireland"].drop(
        columns="name"
    )

    # merge data
    caseGeoUtlaEng = geoUtlaUK.merge(caseEng, on="code")
    caseGeoUtlaEng["group"] = [codeGroup[code] for code in caseGeoUtlaEng["code"]]
    caseGeoCountyEng = (
        caseGeoUtlaEng.drop(columns=["code", "name"])
        .dissolve(by="group", aggfunc="sum")
        .reset_index()
        .rename(columns={"group": "name"})
    )
    caseGeoCountyWls = geoUtlaUK.merge(caseWls, on="code").drop(columns=["code"])
    caseGeoHbSct = geoHbSct.merge(caseSct, on="code").drop(columns=["code"])
    caseGeoCountryNir = geoCountryNir.merge(caseNir, on="code").drop(columns=["code"])
    caseGeoUK = (
        caseGeoCountyEng.append(caseGeoCountyWls, ignore_index=True)
        .append(caseGeoHbSct, ignore_index=True)
        .append(caseGeoCountryNir, ignore_index=True)
    )
    caseGeoUK.iloc[:, 2:] = caseGeoUK.iloc[:, 2:].astype(float)

    # get the cases timespan
    caseDates = caseGeoUK.columns[2:]
    return caseDates, caseGeoUK


def processDataLdn():
    # load data
    geoBoroLdn = gpd.read_file(
        "data/geometry/Counties_and_Unitary_Authorities_December_2019_Boundaries_London_BFC.geojson"
    )
    caseEng = loadCaseData("Eng")
    caseLdn = caseEng[[code.startswith("E09") for code in caseEng["code"]]]

    # Process geometry data for the London boroughs
    geoBoroLdn = geoBoroLdn[["ctyua19cd", "geometry"]].rename(
        columns={"ctyua19cd": "code",}
    )

    # Merge data
    caseGeoBoroLdn = geoBoroLdn.merge(caseLdn, on="code").drop(columns=["code"])
    caseGeoBoroLdn.iloc[:, 2:] = caseGeoBoroLdn.iloc[:, 2:].astype(float)

    # get the cases timespan
    caseDates = caseGeoBoroLdn.columns[2:]
    return caseDates, caseGeoBoroLdn


def getData(loc):
    loc = loc.lower()
    if loc == "uk":
        return processDataUK()
    if loc == "london":
        return processDataLdn()


def getGeoIreland():
    geoCountryIrl = gpd.read_file("data/geometry/Country_Boundary_Ireland_BUC.geojson")
    return geoCountryIrl
