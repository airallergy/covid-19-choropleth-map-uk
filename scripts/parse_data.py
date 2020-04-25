import pandas as pd
import os


def parseData(df):
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)
    df['cases'] = df['cases'].astype('float')
    df = df.pivot(index='name', columns='date', values='cases').transpose()
    df.index = pd.DatetimeIndex(df.index)
    deltaDay = (pd.Timestamp.today().date() - df.index.max().date()).days
    df = df.reindex(pd.date_range('25/01/2020', pd.Timestamp.today())
                    ).shift(periods=deltaDay).fillna(method='ffill').fillna(0)
    return df


def parseDataEng():
    df = pd.read_csv('data/csv/src/data_latest_eng.csv', usecols=['Area name', 'Area type', 'Specimen date', 'Cumulative lab-confirmed cases']).rename(
        columns={'Area name': 'name', 'Area type': 'group', 'Specimen date': 'date', 'Cumulative lab-confirmed cases': 'cases'})
    df = df[df['group'] == 'Upper tier local authority'].drop(columns=[
                                                              'group'])
    parseData(df).to_csv('data/csv/src/cases_eng.csv')


def parseDataWls():
    df = pd.read_excel('data/csv/src/data_latest_wls.xlsx', sheet_name='Tests by specimen date', usecols=[
                       'Local Authority', 'Specimen date', 'Cumulative cases']).rename(columns={'Local Authority': 'name', 'Specimen date': 'date', 'Cumulative cases': 'cases'})
    df = df[(df['name'] != 'Unknown') & (df['name'] != 'Outside Wales')]
    parseData(df).to_csv('data/csv/src/cases_wls.csv')


def parseDataSct():
    df = pd.read_csv('data/csv/src/data_latest_sct.csv', usecols=['Date', 'Country', 'Area', 'TotalCases']).rename(
        columns={'Area': 'name', 'Country': 'group', 'Date': 'date', 'TotalCases': 'cases'})
    df = df[df['group'] == 'Scotland'].drop(columns=['group'])
    df = df[df['name'] != 'Golden Jubilee National Hospital']
    parseData(df).to_csv('data/csv/src/cases_sct.csv')


def ParseDataNir():
    df = pd.read_csv('data/csv/src/data_latest_nir.csv', usecols=['Date', 'Country', 'Indicator', 'Value']).rename(
        columns={'Country': 'name', 'Indicator': 'group', 'Date': 'date', 'Value': 'cases'})
    df = df[df['group'] == 'ConfirmedCases'].drop(columns=['group'])
    df = df[df['name'] == 'Northern Ireland']
    parseData(df).to_csv('data/csv/src/cases_nir.csv')


parseDataEng()
parseDataWls()
parseDataSct()
ParseDataNir()
