import pandas as pd
import os
import numpy as np
from util import getCode


def cleanDataEng():
    df = pd.read_csv(
        "data/csv/src/data_latest_eng.csv",
        usecols=[
            "Area name",
            "Area type",
            "Specimen date",
            "Cumulative lab-confirmed cases",
        ],
    ).rename(
        columns={
            "Area name": "name",
            "Area type": "group",
            "Specimen date": "date",
            "Cumulative lab-confirmed cases": "cases",
        }
    )
    df = df[df["group"] == "Upper tier local authority"].drop(columns=["group"])
    return df


def cleanDataWls():
    df = pd.read_excel(
        "data/csv/src/data_latest_wls.xlsx",
        sheet_name="Tests by specimen date",
        usecols=["Local Authority", "Specimen date", "Cumulative cases"],
    ).rename(
        columns={
            "Local Authority": "name",
            "Specimen date": "date",
            "Cumulative cases": "cases",
        }
    )
    df = df[(df["name"] != "Unknown") & (df["name"] != "Outside Wales")]
    return df


# def cleanDataSct():
#     df = pd.read_csv('data/csv/src/data_latest_sct.csv', usecols=['Date', 'Country', 'Area', 'TotalCases']).rename(
#         columns={'Area': 'name', 'Country': 'group', 'Date': 'date', 'TotalCases': 'cases'})
#     df = df[df['group'] == 'Scotland'].drop(columns=['group'])
#     df = df[df['name'] != 'Golden Jubilee National Hospital']
#     return df


def cleanDataSct():
    df = (
        pd.read_excel(
            "data/csv/src/data_latest_sct.xlsx",
            sheet_name="Table 1 - Cumulative cases",
            header=2,
        )
        .drop(columns="Scotland")
        .set_index("Date")
        .transpose()
    )
    df = df.stack().reset_index()
    df.columns = ["name", "date", "cases"]
    df["name"] = [name.split("NHS ")[1].replace("&", "and") for name in df["name"]]
    df["cases"] = pd.to_numeric(df["cases"], errors="coerce")
    df = df[df["cases"].notna()]
    dfArchive = pd.read_csv(
        "data/csv/archive/data_archive_sct.csv", parse_dates=["date"], dayfirst=True
    )
    df = df.append(dfArchive)
    df = df.sort_values(by=["name", "date"], ignore_index=True)
    return df


def cleanDataNir():
    df = pd.read_csv(
        "data/csv/src/data_latest_nir.csv",
        usecols=["Date", "Country", "Indicator", "Value"],
    ).rename(
        columns={
            "Country": "name",
            "Indicator": "group",
            "Date": "date",
            "Value": "cases",
        }
    )
    df = df[df["group"] == "ConfirmedCases"].drop(columns=["group"])
    df = df[df["name"] == "Northern Ireland"]
    return df


def parseData(country, today=None):
    nameCodeDict = getCode()
    if not today:
        today = pd.Timestamp.today()
    df = eval("cleanData" + country.capitalize() + "()")
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    df["cases"] = df["cases"].astype("float")
    df = df.pivot(index="name", columns="date", values="cases").transpose()
    df.index = pd.DatetimeIndex(df.index)
    deltaDay = (today.date() - df.index.max().date()).days
    df = (
        df.reindex(pd.date_range("25/01/2020", today))
        .shift(periods=deltaDay)
        .fillna(method="ffill")
        .fillna(0)
    )
    df.columns = pd.MultiIndex.from_arrays(
        np.array([df.columns, [nameCodeDict[name] for name in df.columns]])
    )
    df.to_csv(os.path.join("data/csv", "cases_" + country.lower() + ".csv"))
