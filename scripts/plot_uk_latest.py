import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib import __version__ as mpl_version
import pickle
import os
import shutil
import numpy as np
from itertools import compress
from process_data import getData, getGeoIreland
from util import calBinsScale, getPlotPicklePath, classifyDf
from plot import plotCase, plotName, plotCasePickle
import warnings


def adjustNameUK(xcoord, ycoord, name):
    if name in [
        "Blaenau Gwent",
        "Bridgend",
        "Caerphilly",
        "Cardiff",
        "Merthyr Tydfil",
        "Neath Port Talbot",
        "Newport",
        "Rhondda Cynon Taf",
        "Swansea",
        "Torfaen",
        "Vale of Glamorgan",
        # 'Antrim and Newtownabbey',
        # 'Ards and North Down',
        # 'Armagh City, Banbridge and Craigavon',
        # 'Belfast',
        # 'Causeway Coast and Glens',
        # 'Derry City and Strabane',
        # 'Fermanagh and Omagh',
        # 'Lisburn and Castlereagh',
        # 'Mid and East Antrim',
        # 'Mid Ulster',
        # 'Newry, Mourne and Down',
    ]:
        font = FontProperties(family="Palatino", size=2)
    else:
        font = FontProperties(family="Palatino", size=3)
    # if name == 'Ards and North Down':
    #     xcoord += 0.16
    # if name == 'Mid Ulster':
    #     xcoord += 0.08
    # if name == 'Mid and East Antrim':
    #     xcoord -= 0.04
    # if name == 'Fermanagh and Omagh':
    #     xcoord -= 0.12
    # if name == 'Newry, Mourne and Down':
    #     ycoord -= 0.08
    # if name == 'Derry City and Strabane':
    #     xcoord += 0.12
    if name == "Rhondda Cynon Taf":
        xcoord += 0.02
        ycoord -= 0.02
    return xcoord, ycoord, name, font


def plotUK():
    fig, ax = plt.subplots(1, figsize=(6, 9))

    caseDates, caseGeo = getData(loc="UK")
    countryIreGeo = getGeoIreland()

    binsScale = calBinsScale(caseGeo[caseDates[-1]])
    plotPicklePath = getPlotPicklePath(binsScale, loc="uk")
    binsScaleShifted = not os.path.isfile(plotPicklePath)

    with warnings.catch_warnings(record=True) as w:
        with open(plotPicklePath, "rb") as f:
            ax = pickle.load(f)
        mplVersionShifted = "This figure was saved with matplotlib version" in str(
            w[-1].message
        )

    if binsScaleShifted or mplVersionShifted:
        countryIreGeo.to_crs(epsg=3857).plot(
            ax=ax, color="silver", edgecolor="grey", linewidths=0.05
        )
        caseDate = caseDates[-1]
        plotCase(ax, caseGeo, caseDate, legendScale=2.0)
        plotName(caseGeo, adjustNameUK)
        plt.text(
            0.2,
            0.1,
            caseDate.strftime("%d %b %Y"),
            transform=ax.transAxes,
            fontproperties=FontProperties(family="Palatino", size=8),
            label="dateText",
        )
        with open(plotPicklePath, "wb") as f:
            pickle.dump(ax, f, pickle.HIGHEST_PROTOCOL)

    caseToday = (
        caseGeo.drop(columns=["geometry", "coords"], errors="ignore")
        .set_index("name")
        .transpose()
    )
    caseYesterdayPicklePath = os.path.join(
        "data/pickle", "_".join(["cases", "uk", "yesterday"]) + ".pickle"
    )
    if (not binsScaleShifted) and os.path.isfile(caseYesterdayPicklePath):
        with open(caseYesterdayPicklePath, "rb") as f:
            caseYesterday = pickle.load(f)
        caseDiff = (
            classifyDf(caseYesterday, binsScale)
            .eq(classifyDf(caseToday, binsScale))
            .all(axis=1)
            .to_numpy()
        )
    else:
        caseDiff = np.full(len(caseDates), False)

    for caseDate in compress(caseDates, ~caseDiff):
        plt.cla()
        ax = plotCasePickle(binsScale, caseGeo, caseDate, plotPicklePath)
        caseImgPath = os.path.join(
            "docs/img",
            "_".join(["uk", "cases"]),
            "_".join(["uk", "cases", caseDate.strftime("%Y_%m_%d")]) + ".png",
        )
        plt.savefig(caseImgPath, dpi=1200, transparent=False)
        if caseDate == caseDates[-1]:
            caseLatestImgPath = os.path.join(
                "docs/img", "_".join(["uk", "cases", "latest"]) + ".png"
            )
            shutil.copy2(caseImgPath, caseLatestImgPath)

    with open(caseYesterdayPicklePath, "wb") as f:
        pickle.dump(caseToday, f, pickle.HIGHEST_PROTOCOL)

    plt.close("all")
