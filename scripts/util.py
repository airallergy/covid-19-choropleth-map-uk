import pandas as pd
import numpy as np
import sys
import os
from lxml import html
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


def calBinsScale(caseNo):
    caseNoMax = caseNo.max()
    binsNo = 5.0
    if caseNoMax < np.float_power(10, binsNo - 2):
        caseNoMax3rdRootFloor = np.floor(np.cbrt(caseNoMax))
        binsBase = caseNoMax3rdRootFloor
    else:
        binsBase = 10.0
        caseNoMaxLog10 = np.log10(caseNoMax)
        binsNo = np.floor(caseNoMaxLog10) + 2
    return binsBase, binsNo


def calBinsBoundary(binsScale):
    binsBase, binsNo = binsScale
    binsBoundary = np.float_power(binsBase, np.arange(-1, binsNo))
    return binsBoundary


def getPlotPicklePath(binsScale, loc):
    binsBase, binsNo = binsScale
    binsBase = 'b' + str(int(binsBase))
    binsNo = 'n' + str(int(binsNo))
    loc = loc.lower()
    plotPicklePath = os.path.join(
        'data/pickle', '_'.join([loc, binsBase, binsNo]) + '.pickle')
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


if __name__ == '__main__':
    retrieveFileLinkWls()
