import pandas as pd
import numpy as np
from util import calBinsScale, calBinsBoundary


def testCalBinsScale():
    assert calBinsScale(pd.Series([65])) == (4.0, 5.0)
    assert calBinsScale(pd.Series([1234])) == (10.0, 5.0)
    assert calBinsScale(pd.Series([7777777])) == (10.0, 8.0)


def testCalBinsBoundary():
    assert (calBinsBoundary((10.0, 3.0)) == np.array([0.1, 1.0, 10.0, 100.0])).all()


if __name__ == "__main__":
    testCalBinsScale()
    testCalBinsBoundary()
