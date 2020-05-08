import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pickle
from process_data import getData, getGeoIreland
from util import calBinsScale, getPlotPicklePath, checkPlotPickle
from plot import plotCase, plotName, plotCasePickle


def adjustNameUK(xcoord, ycoord, name):
    if name in [
        'Blaenau Gwent',
        'Bridgend',
        'Caerphilly',
        'Cardiff',
        'Merthyr Tydfil',
        'Neath Port Talbot',
        'Newport',
        'Rhondda Cynon Taf',
        'Swansea',
        'Torfaen',
        'Vale of Glamorgan',
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
        font = FontProperties(family='Palatino', size=2)
    else:
        font = FontProperties(family='Palatino', size=3)
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
    if name == 'Rhondda Cynon Taf':
        xcoord += 0.02
        ycoord -= 0.02
    return xcoord, ycoord, name, font


def plot_uk_latest():
    fig, ax = plt.subplots(1, figsize=(6, 9))

    caseDates, caseGeo = getData(loc='UK')
    countryIreGeo = getGeoIreland()

    binsScale = calBinsScale(caseGeo[caseDates[-1]])
    plotPicklePath = getPlotPicklePath(binsScale, loc='UK')
    if not checkPlotPickle(binsScale, loc='UK'):
        caseDate = caseDates[-1]
        plotCase(ax, caseGeo, caseDate)
        countryIreGeo.to_crs(epsg=3857).plot(
            ax=ax, color='silver', edgecolor='grey', linewidths=0.05)
        plotName(caseGeo, adjustNameUK)
        plt.text(
            0.2, 0.1,
            caseDate.strftime('%d %b %Y'),
            transform=ax.transAxes,
            fontproperties=FontProperties(family='Palatino', size=8),
            label='dateText'
        )
        with open(plotPicklePath, 'wb') as f:
            pickle.dump(ax, f, pickle.HIGHEST_PROTOCOL)
    else:
        plotCasePickle(binsScale, caseGeo, caseDates[-1], plotPicklePath)

    plt.savefig('docs/img/uk_cases_latest.png', dpi=1200, transparent=False)
