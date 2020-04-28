import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from process_data import getData
from util import calBinsBoundary, calBinsScale
from plot import plotCase, plotName


def adjustNameLdn(xcoord, ycoord, name):
    '''
    annotations adjustment for london boroughs
    '''
    if name == 'City of London':
        font = FontProperties(family='Palatino', size=3)
    else:
        font = FontProperties(family='Palatino', size=4)
    if name == 'Hammersmith and Fulham':
        xcoord += 0.015
        ycoord -= 0.015
    if name == 'Kensington and Chelsea':
        xcoord -= 0.015
        ycoord += 0.01
    if name == 'Westminster':
        xcoord += 0.01
        ycoord -= 0.005
    if name == 'Camden':
        xcoord -= 0.005
    if name == 'Hackney':
        xcoord += 0.015
    if name == 'Barking and Dagenham':
        ycoord -= 0.005
    if name == 'Lewisham':
        ycoord -= 0.005
    return xcoord, ycoord, name, font


def plot_ldn_latest():
    # plot latest london cases breakdown
    fig, ax = plt.subplots(1, figsize=(6, 4))

    caseDates, caseGeo = getData(loc='London')
    caseDate = caseDates[-1]
    plotCase(ax, caseGeo, caseDate)
    plotName(caseGeo, adjustNameLdn)
    plt.text(
        0.1, 0.05,
        caseDate.strftime('%d %b %Y'),
        transform=ax.transAxes,
        fontproperties=FontProperties(family='Palatino', size=8)
    )

    plt.savefig('london_cases_latest.png', dpi=300, transparent=False)
