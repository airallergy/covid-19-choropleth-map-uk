import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from process_data import getData, getGeoIreland
from util import calBoundariesScale
from plot import plotCase, plotName


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


# plot latest london cases breakdown
fig, ax = plt.subplots(1, figsize=(6, 9))

countryIreGeo = getGeoIreland()
countryIreGeo.to_crs(epsg=3857).plot(
    ax=ax, color='silver', edgecolor='grey', linewidths=0.05)
caseDates, caseGeo = getData(loc='UK')
caseDate = caseDates[-1]
plotCase(ax, caseGeo, caseDate)
plotName(caseGeo, adjustNameUK)
plt.text(
    0.2, 0.1,
    caseDate.strftime('%d %b %Y'),
    transform=ax.transAxes,
    fontproperties=FontProperties(family='Palatino', size=8)
)

plt.savefig('uk_cases_latest.png', dpi=1200, transparent=False)
