import pandas as pd
import numpy as np


def getAbbrv():
    nameAbbrv = pd.read_csv('data/csv/name_abbrv.csv')
    nameAbbrvDict = pd.Series(nameAbbrv.countyNameAbbrv.values,
                              index=nameAbbrv.countyName).to_dict()
    return nameAbbrvDict


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
