import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.collections import PatchCollection
from matplotlib.font_manager import FontProperties
# from matplotlib.animation import FuncAnimation, writers
from mapclassify import UserDefined
from pyproj import Proj, transform
from geopandas.plotting import _flatten_multi_geoms, _mapclassify_choro
from util import getAbbrv, calBoundariesScale


def plotCase(ax, caseGeo, caseDate, boundariesScale=None):
    '''
    plot the choropleth map
    '''
    ax.axis('off')
    ax.set_aspect('equal')

    if boundariesScale is None:
        boundariesScale = calBoundariesScale(caseGeo[caseDate])
    bins = boundariesScale[1:] - 0.01

    cmap = 'OrRd'
    ncolor = 256
    norm = mcolors.BoundaryNorm(
        boundariesScale, ncolor, clip=True)  # norm takes (..., ...]

    pc = PatchCollection([], edgecolors='none', cmap=cmap, norm=norm)

    binsTextsLeft = boundariesScale.astype(int).astype(str)
    binsTextsRight = (boundariesScale - 1).astype(int).astype(str)
    binsTexts = zip(binsTextsLeft[1:-2], binsTextsRight[2:-1])
    texts = ['0'] + ['{:s} - {:s}'.format(i, j)
                     for i, j in binsTexts] + ['≥ ' + binsTextsLeft[-2]]

    handles = [
        plt.plot([], [], marker='s', linestyle='', color=pc.cmap(
            pc.norm(j)), label='{:s}'.format(texts[i]))[0]
        for i, j in tuple(zip(range(len(texts)), bins))
    ]

    font = FontProperties(family='Palatino', size=4)

    caseGeo.to_crs(epsg=3857).plot(
        column=caseDate,
        ax=ax,
        legend=True,
        legend_kwds={
            'handles': handles,
            'bbox_to_anchor': (0.5, -0.1),
            'loc': 'lower center',
            'ncol': len(bins),
            'prop': font,
            'frameon': False,
            'markerscale': 0.5,
        },
        scheme='user_defined',
        classification_kwds={
            'bins': bins,  # mapclassify takes [..., ...)
        },
        cmap=cmap,
        norm=mcolors.BoundaryNorm(
            np.arange(len(boundariesScale)), ncolor, clip=True),
        edgecolor='grey',
        linewidths=0.05,
        zorder=1
    )


def plotName(caseGeo, adjustName):
    '''
    plot region names
    '''
    nameAbbrvDict = getAbbrv()
    caseGeo['coords'] = caseGeo['geometry'].apply(lambda x: x.centroid)
    for idx, row in caseGeo.iterrows():
        xcoord = row['coords'].x
        ycoord = row['coords'].y
        name = row['name']
        xcoord, ycoord, name, font = adjustName(xcoord, ycoord, name)
        s = nameAbbrvDict[name].replace('\\n', '\n')
        xy = transform(Proj(init='epsg:4326'), Proj(
            init='epsg:3857'), xcoord, ycoord)
        plt.annotate(s=s, xy=xy, horizontalalignment='center',
                     verticalalignment='center', fontproperties=font)
