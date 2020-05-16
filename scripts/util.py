import pandas as pd
import numpy as np
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from geopandas.plotting import _mapclassify_choro


def getCode():
    nameCode = pd.read_csv('data/csv/name_code.csv')
    nameCodeDict = pd.Series(nameCode['code'].values,
                             index=nameCode['name']).to_dict()
    return nameCodeDict


def getAbbrv():
    nameAbbrv = pd.read_csv('data/csv/name_abbrv.csv')
    nameAbbrvDict = pd.Series(nameAbbrv.countyNameAbbrv.values,
                              index=nameAbbrv.countyName).to_dict()
    return nameAbbrvDict


def getGroup():
    codeGroup = pd.read_csv('data/csv/code_group.csv')
    codeGroupDict = pd.Series(codeGroup['group'].values,
                              index=codeGroup['code']).to_dict()
    return codeGroupDict


def calBinsScale(caseData):
    caseDataMax = caseData.max()
    binsNum = 5.0
    if caseDataMax < np.float_power(10, binsNum - 2):
        caseDataMax3rdRootFloor = np.floor(np.cbrt(caseDataMax))
        binsBase = caseDataMax3rdRootFloor
    else:
        binsBase = 10.0
        caseDataMaxLog10 = np.log10(caseDataMax)
        binsNum = np.floor(caseDataMaxLog10) + 2
    return binsBase, binsNum


def calBinsBoundary(binsScale):
    binsBase, binsNum = binsScale
    binsBoundary = np.float_power(binsBase, np.arange(-1, binsNum))
    return binsBoundary


def getPlotPicklePath(binsScale, loc):
    binsBase, binsNum = binsScale
    binsBase = 'b' + str(int(binsBase))
    binsNum = 'n' + str(int(binsNum))
    loc = loc.lower()
    plotPicklePath = os.path.join(
        'data/pickle', '_'.join([loc, binsBase, binsNum]) + '.pickle')
    return plotPicklePath


def checkPlotPickle(binsScale, loc):
    plotPicklePath = getPlotPicklePath(binsScale, loc)
    if os.path.isfile(plotPicklePath):
        return True
    else:
        return False


def retrieveFileLinkWls():
    url = 'https://public.tableau.com/views/RapidCOVID-19virology-Public/Headlinesummary?:display_count=y&:embed=y&:showAppBanner=false&:showVizHome=no'
    driver = webdriver.Chrome()
    driver.get(url)
    try:
        fileLink = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="tabZoneId66"]/div/div/div/a'))).get_attribute('href')
    finally:
        driver.quit()
    return fileLink


def classifyDf(df, binsScale):
    dfArray = df.to_numpy()
    dfShape = dfArray.shape
    binsBoundary = calBinsBoundary(binsScale)
    bins = binsBoundary[1:] - 0.01
    binning = _mapclassify_choro(
        dfArray.flatten(), scheme='UserDefined', bins=bins, k=len(bins))
    dfClass = df.copy()
    dfClass.loc[:, :] = binning.yb.reshape(dfShape)
    return dfClass
