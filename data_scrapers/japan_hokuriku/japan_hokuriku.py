# This scraper downloads all past area demand and supply data from 2016-April,2022 as 
# separate CSV files for each month of the year. Columns are translated from 
# Japanese to English. Most recent data appears up top. Supply data is broken
# down by fuel types and all values are converted from 10,000 kWh to MWh.

import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_page():
    """
    This function sends a request to the url and parses for the HTML codes 
    :return: BeautifulSoup object with HTML source codes
    """ 
    url = 'https://www.rikuden.co.jp/nw_jyukyudata/area_jisseki.html'
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('Failed to load page {}'.format(url))
    page = BeautifulSoup(r.text, 'html.parser')
    return page

def get_csv_urls(page):
    """
    This function extracts all urls of the demand/supply CSV's
    :param page: BeautifulSoup object with HTML source codes
    :return: a list of CSV urls
    """
    csv_urls = []
    base_url = 'https://www.rikuden.co.jp'
    for tag in page.find_all('li', {'class': 'MarkNewwin'}):
        for anchor in tag.find_all('a'):
            csv_urls.append(base_url + anchor['href'])
    return csv_urls

def download_csv():
    """
    This is the main function for donwloading all CSV's that contain demand/
    supply data from the webpage. It reads the CSV's as dataframes, cleans data,
    and reads the reformatted data to separate files for demand and supply.
    """
    page = get_page()
    csv_urls = get_csv_urls(page)
    
    for url in csv_urls:
        data = pd.read_csv(url, index_col=None, encoding= 'unicode_escape',
                           skiprows=5, usecols=range(14))
            
        # remove empty rows-- some files contain trailing rows with no values
        data = data.dropna(axis=0, how='all')
            
        # combine columns 'DATE' and 'TIME' to make a datetime object
        if 'DATE' not in data.columns:
            data.columns = data.iloc[0]
            data.drop(index=0, axis=0, inplace=True)
        data['DATE']=pd.to_datetime(data.DATE + ' ' + data.TIME, format='%Y/%m/%d %H:%M')
        data.drop('TIME', axis=1, inplace=True)

        # rename fuel types
        data.columns = ['Date_Time',
                      'Area_Demand',
                      'Nuclear Power',
                      'Thermal Power',
                      'Hydropower', 
                      'Geothermal', 
                      'Biomass', 
                      'Solar Performance', 
                      'Solar Supression Amount', 
                      'Wind Performance', 
                      'Wind Suppression Amount', 
                      'Pumped Storage', 
                      'Interconnector']
        
        # convert from kWh to MWh
        # assign units and region
        data.loc[:,data.columns!='Date_Time'] = data.loc[:,data.columns!='Date_Time'] * 10
        data['Region'], data['Unit'] = ['Hokuriku', 'MWh']

        # get demand data into one df
        demand_df = data[['Date_Time', 'Region', 'Unit', 'Area_Demand']].copy()
        demand_df.sort_values(by=['Date_Time'],ascending=False, inplace=True)

        # get supply data into another df
        data.drop('Area_Demand', axis=1, inplace=True)
        supply_df = pd.melt(data, id_vars=['Date_Time','Region', 'Unit'], var_name='Fuel_Type', value_name='Supply')
        supply_df.sort_values(by=['Date_Time','Fuel_Type'], ascending=False, inplace=True)

        # write df to csvs
        demand_df.to_csv('Hokuriku_Demand_{}'.format(url[67:]), index=False)
        supply_df.to_csv('Hokuriku_Supply_{}'.format(url[67:]), index=False)
        
if __name__ == '__main__':
    download_csv()