import pandas as pd
import numpy as np


def getAbbrv():
    nameAbbrv = pd.read_csv('data/csv/name_abbrv.csv')
    nameAbbrvDict = pd.Series(nameAbbrv.countyNameAbbrv.values,
                              index=nameAbbrv.countyName).to_dict()
    return nameAbbrvDict


def calBoundariesScale(caseNo):
    '''
    calculate the bins scale
    '''
    caseNoMax = caseNo.max()
    caseNoMax4thRoot = np.sqrt(np.sqrt(caseNoMax))
    caseNoMax4thRootFloor = np.floor(caseNoMax4thRoot)
    binsBase = caseNoMax4thRootFloor if caseNoMax4thRootFloor < 10 else 10
    boundariesScale = np.float_power(binsBase, [-1, 0, 1, 2, 3, 4, 5])
    return boundariesScale
