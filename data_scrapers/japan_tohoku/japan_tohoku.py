# Downloads all past demand data (2016-April,2022) for Tohoku, Japan from 
# https://setsuden.nw.tohoku-epco.co.jp/download.html
# Converts all demand and supply values from 10,000 kWh to MWh and reads 
# formatted data to two csv files: one for demand data and one for supply

import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_csv_urls():
    """
    This function downloads the page from the above url and get all the 
    links of the CSV's that contains supply/demand data
    :return: a list of CSV urls
    """
    url = 'https://setsuden.nw.tohoku-epco.co.jp/download.html'
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('Failed to load page {}'.format(url))
    page = BeautifulSoup(r.text, 'html.parser')
    
    link_urls = []
    base_url = 'https://setsuden.nw.tohoku-epco.co.jp/'
    div_tags = page.find_all('div', {'class':'download clearFix'})
    link_tags = div_tags[1].find_all('a')
    
    for tag in link_tags:
        link_urls.append(base_url + tag['href'])
        
    return link_urls

def download_csv():
    """
    This is the main function for downloading supply/demand data from CSV urls,
    cleaning and formatting data. Then, reading demand data to one CSV file 
    and supply data to another CSV file.
    """
    csv_urls = get_csv_urls()

    # read all csvs, concat into a single df
    data = [pd.read_csv(url, encoding= 'unicode_escape', parse_dates=['DATE_TIME']) for url in csv_urls]
    data = pd.concat(data, ignore_index=True)
    
    # rename columns
    data.columns = ['Date_Time', 
                    'Area_Demand', 
                    'Hydropower', 
                    'Thermal Power', 
                    'Nuclear Power', 
                    'Solar Power', 
                    'Solar Power Suppression', 
                    'Wind Power', 
                    'Wind Power Suppression', 
                    'Geothermal', 
                    'Biomass', 
                    'Pumped Storage', 
                    'Interconnector']

    # convert from kWh to MWh
    # assign units and region
    data.loc[:,data.columns!='Date_Time'] = data.loc[:,data.columns!='Date_Time'] * 10
    data['Region'], data['Unit'] = ['Tohoku', 'MWh']

    # get demand data into one df
    demand_df = data[['Date_Time', 'Region', 'Unit', 'Area_Demand']].copy()
    demand_df.sort_values(by=['Date_Time'],ascending=False, inplace=True)

    # get supply data into one df
    data.drop('Area_Demand', axis=1, inplace=True)
    supply_df = pd.melt(data, id_vars=['Date_Time','Region', 'Unit'], var_name='Fuel_Type', value_name='Supply')
    supply_df.sort_values(by=['Date_Time','Fuel_Type'], ascending=False, inplace=True)
    
    # write demand and supply data to seperate csv files 
    demand_df.to_csv('Japan_Tohoku_Demand_Data.csv', index=False)
    supply_df.to_csv('Japan_Tohoku_Supply_Data.csv', index=False) 
    
if __name__ == '__main__':
    download_csv()