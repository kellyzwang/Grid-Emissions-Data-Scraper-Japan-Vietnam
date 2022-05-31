# Downloads all past demand data (2016-March,2022) for Tohoku, Japan from 
# https://www.energia.co.jp/nw/service/retailer/data/area/
# Converts all demand and supply values from 10,000 kWh to MWh and reads
# formatted data to two csv files: one for demand data and one for supply

import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup
import numpy as np

def get_csv_urls():
    """
    This function downloads the page from the above url and get all the 
    links of the CSV's that contains supply/demand data
    :return: a list of CSV urls
    """
    url = 'https://www.energia.co.jp/nw/service/retailer/data/area/'
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('Failed to load page {}'.format(url))
    page = BeautifulSoup(r.text, 'html.parser')

    tags = page.find_all('a', {'class':'link-button-1'})
    csv_urls = []
    for tag in tags:
        link = url + tag['href']
        if '../../' in link:
            link = link.replace('data/area/../../','')
        csv_urls.append(link)
    
    return csv_urls

def download_csv():
    """
    This is the main function for downloading supply/demand data from CSV urls,
    cleaning and formatting data. Then, reading demand data to one CSV file 
    and supply data to another CSV file.
    """
    csv_urls = get_csv_urls()
    
    data = [pd.read_csv(url, encoding= 'unicode_escape', header=2) for url in csv_urls]
    data = pd.concat(data, ignore_index=True)

    # remove empty rows-- some files contain trailing rows with no values
    data = data.dropna(axis=0, how='all')
    # replace characters below with NaNs
    data = data.replace('|', np.nan)

    # combine columns 'DATE' and 'TIME' to make a datetime object
    data['DATE']=pd.to_datetime(data.DATE + ' ' + data.TIME, format='%Y/%m/%d %H:%M')
    data.drop('TIME', axis=1, inplace=True)
    
    # set column names
    data.columns = ('Date_Time',
                  'Area_Demand', 
                  'Nuclear Power', 
                  'Thermal Power', 
                  'Hydropower', 
                  'Geothermal', 
                  'Biomass', 
                  'Solar', 
                  'Solar Power Supression', 
                  'Wind Power',  
                  'Wind Power Suppression', 
                  'Pumped Storage', 
                  'Interconnector')

    # convert from kWh to MWh
    # assign units and region
    data.loc[:,data.columns!='Date_Time'] = data.loc[:,data.columns!='Date_Time'] * 10
    data['Region'], data['Unit'] = ['Chugoku', 'MWh']

    # get demand data
    demand_df = data[['Date_Time', 'Region', 'Unit', 'Area_Demand']].copy()
    demand_df.sort_values(by=['Date_Time'],ascending=False, inplace=True)

    # get supply data
    data.drop('Area_Demand', axis=1, inplace=True)
    supply_df = pd.melt(data, id_vars=['Date_Time','Region', 'Unit'], var_name='Fuel_Type', value_name='Supply')
    supply_df.sort_values(by=['Date_Time','Fuel_Type'], ascending=False, inplace=True)
    
    # write demand and supply data to seperate csv files 
    demand_df.to_csv('Japan_Chugoku_Demand_Data.csv', index=False)
    supply_df.to_csv('Japan_Chugoku_Supply_Data.csv', index=False)

if __name__ == '__main__':
    download_csv()