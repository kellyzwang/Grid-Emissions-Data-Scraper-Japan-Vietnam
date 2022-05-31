# Downloads all past demand data (2016-April,2022) for Shikoku, Japan from 
# https://www.yonden.co.jp/nw/renewable_energy/data/supply_demand.html
# Converts all demand and supply values from 10,000 kWh to MWh and reads 
# formatted data to two csv files: one for demand data and one for supply

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def get_page():
    """
    This function downloads HTML content of the given url
    :return: BeautifulSoup object with HTML source codes
    """
    url = 'https://www.yonden.co.jp/nw/renewable_energy/data/supply_demand.html'
    r = requests.get(url)
    if r.status_code != 200:
        r.raise_for_status()
    page = BeautifulSoup(r.text, "html.parser")
    return page

def get_excel_urls(page):
    """
    This function parses the HTML codes to get all urls for downloading
    excels that contains demand and supply data
    :param page: BeautifulSoup object with HTML source codes
    :return: a list of excel urls
    """
    excel_urls = []
    base_url = 'https://www.yonden.co.jp'
    tags = page.find_all('p', {'class':'c-text_01'})[1:]
    for tag in tags:
        link = tag.find('a').get('href')
        excel_urls.append(base_url + link)
    return excel_urls

def download_data_to_csv():
    """
    This function downloads past demand/supply data, reformats data, and
    reads demand data to one csv and supply data to another csv
    """
    page = get_page()
    excel_urls = get_excel_urls(page)
    
    # reads and combine all data into a single df
    data = [pd.read_excel(url, skiprows=8, usecols=range(0,14), skipfooter=1) for url in excel_urls]
    data = pd.concat(data, ignore_index=True)
    data = data.dropna().replace('－', np.nan)

    # combine date and time to a single column
    data.iloc[:,0] = pd.to_datetime(data.iloc[:,0].astype(str) + ' ' + data.iloc[:,1].astype(str))
    data.drop(data.columns[1], axis=1, inplace=True)

    # column names
    data.columns = ('Date_Time', 'Area_Demand', 'Nuclear Power', 'Thermal Power', 'Hydropower', 
                    'Geothermal', 'Biomass', 'Solar Power', 'Solar Power Suppression', 'Wind Power',
                    'Wind Power Suppression', 'Pumped Storage', 'Interconnector')

    # convert from kWh to MWh
    # assign units and region
    data.loc[:,data.columns!='Date_Time'] = data.loc[:,data.columns!='Date_Time'] * 10
    data['Region'], data['Unit'] = ['Shikoku', 'MWh']

    # get demand data
    demand_df = data[['Date_Time', 'Region', 'Unit', 'Area_Demand']].copy()
    demand_df.sort_values(by=['Date_Time'],ascending=False, inplace=True)

    # get supply data
    data.drop('Area_Demand', axis=1, inplace=True)
    supply_df = pd.melt(data, id_vars=['Date_Time','Region', 'Unit'], var_name='Fuel_Type', value_name='Supply')
    supply_df.sort_values(by=['Date_Time','Fuel_Type'], ascending=False, inplace=True)

    # write demand and supply data to seperate csv files 
    demand_df.to_csv('Japan_Shikoku_Demand_Data.csv', index=False)
    supply_df.to_csv('Japan_Shikoku_Supply_Data.csv', index=False)
    
if __name__ == '__main__':
    download_data_to_csv()