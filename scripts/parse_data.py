import pandas as pd


def parseDataEngland():
    df = pd.read_csv('data/csv/src/coronavirus-cases_latest.csv', usecols=[
                     'Area name', 'Area code', 'Area type', 'Specimen date', 'Cumulative lab-confirmed cases'])
    df = df[df['Area type'] == 'Upper tier local authority'].drop(
        columns=['Area type']).reset_index(drop=True)
    df['Specimen date'] = pd.to_datetime(df['Specimen date'], dayfirst=True)
    df['Cumulative lab-confirmed cases'] = df['Cumulative lab-confirmed cases'].astype(
        'float')
    df = df.pivot_table(index=['Area name', 'Area code'], columns='Specimen date',
                        values='Cumulative lab-confirmed cases').sort_values(by=['Area code'])
    dfT = df.transpose()
    dfT.index = pd.DatetimeIndex(dfT.index)
    df = dfT.reindex(pd.date_range(
        '25/01/2020', pd.Timestamp.today().strftime("%d/%m/%Y"))).transpose()
    df = df.shift(periods=(pd.Timestamp.today().date() -
                           dfT.index.max().date()).days, axis=1).reset_index()
    df.columns = df.columns[0:2].to_list(
    ) + pd.to_datetime(df.columns[2:], dayfirst=True).date.tolist()
    df.iloc[:, 2:] = df.iloc[:, 2:].fillna(method='ffill', axis=1).fillna(0)
    df.to_csv('data/csv/src/data_update_england.csv')


def parseDataWales():
    df = pd.read_excel('data/csv/src/Rapid COVID-19 surveillance data.xlsx',
                       sheet_name='Tests by specimen date', usecols=['Local Authority', 'Specimen date', 'Cumulative cases'])
    df['Cumulative cases'] = df['Cumulative cases'].astype('float')
    df = df.pivot_table(index=['Local Authority'], columns='Specimen date',
                        values='Cumulative cases').drop(index=['Unknown', 'Outside Wales'])
    dfT = df.transpose()
    dfT.index = pd.DatetimeIndex(dfT.index)
    df = dfT.reindex(pd.date_range(
        '25/01/2020', pd.Timestamp.today().strftime("%d/%m/%Y"))).transpose()
    df = df.shift(periods=(pd.Timestamp.today().date() -
                           dfT.index.max().date()).days, axis=1).reset_index()
    df.columns = df.columns[0:1].to_list(
    ) + pd.to_datetime(df.columns[1:], dayfirst=True).date.tolist()
    df.iloc[:, 1:] = df.iloc[:, 1:].fillna(method='ffill', axis=1).fillna(0)
    df.to_csv('data/csv/src/data_update_wales.csv')


def parseDataScotland():
    df = pd.read_csv('data/csv/src/covid-19-cases-uk.csv',
                     usecols=['Date', 'Country', 'AreaCode', 'Area', 'TotalCases'])
    df = df[df['Country'] == 'Scotland'].drop(columns=['Country'])
    df['TotalCases'] = df['TotalCases'].astype('float')
    df = df[df['Area'] != 'Golden Jubilee National Hospital']
    df = df.pivot_table(index=['AreaCode', 'Area'], columns='Date',
                        values='TotalCases').sort_values(by=['Area'])
    dfT = df.transpose()
    dfT.index = pd.DatetimeIndex(dfT.index)
    df = dfT.reindex(pd.date_range(
        '25/01/2020', pd.Timestamp.today().strftime("%d/%m/%Y"))).transpose()
    df = df.shift(periods=(pd.Timestamp.today().date() -
                           dfT.index.max().date()).days, axis=1).reset_index()
    df.columns = df.columns[0:2].to_list(
    ) + pd.to_datetime(df.columns[2:], dayfirst=True).date.tolist()
    df.iloc[:, 2:] = df.iloc[:, 2:].fillna(method='ffill', axis=1).fillna(0)
    df.to_csv('data/csv/src/data_update_scotland.csv')


def ParseDataNI():
    df = pd.read_csv('data/csv/src/covid-19-indicators-uk.csv',
                     usecols=['Date', 'Country', 'Indicator', 'Value'])
    df = df[df['Indicator'] == 'ConfirmedCases'].drop(columns=['Indicator'])
    df = df[df['Country'] == 'Northern Ireland']
    df['Value'] = df['Value'].astype('float')
    df = df.pivot_table(index=['Country'], columns='Date', values='Value')
    dfT = df.transpose()
    dfT.index = pd.DatetimeIndex(dfT.index)
    df = dfT.reindex(pd.date_range(
        '25/01/2020', pd.Timestamp.today().strftime("%d/%m/%Y"))).transpose()
    df = df.shift(periods=(pd.Timestamp.today().date() -
                           dfT.index.max().date()).days, axis=1).reset_index()
    df.columns = df.columns[0:1].to_list(
    ) + pd.to_datetime(df.columns[1:], dayfirst=True).date.tolist()
    df.iloc[:, 1:] = df.iloc[:, 1:].fillna(method='ffill', axis=1).fillna(0)
    df.to_csv('data/csv/src/data_update_northernireland.csv')


parseDataEngland()
parseDataWales()
parseDataScotland()
ParseDataNI()
