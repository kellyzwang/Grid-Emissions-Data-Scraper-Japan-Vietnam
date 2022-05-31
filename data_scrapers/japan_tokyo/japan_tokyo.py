# Downloads all past demand data (2016-2022) for Tokyo, Japan from 
# https://www.tepco.co.jp/en/forecast/html/download-e.html
# Converts all demand values from 10,000 kW to MW and read 
# formatted data to csv files. Each year's data will be downloaded
# to a separate csv file labeled by the corresponding year.

import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_page():
    """
    This function sends a request to the url and parses the HTML source. 
    :return: BeautifulSoup object of HTML source codes
    """ 
    url = 'https://www.tepco.co.jp/en/forecast/html/download-e.html'
    r = requests.get(url)
    if r.status_code != 200:
        r.raise_for_status()
    page = BeautifulSoup(r.text, "html.parser")
    return page

def get_csv_urls(page):
    """
    This function extracts all links for the demand/supply CSV's
    :param page: BeautifulSoup object with HTML source codes
    :return: a list of CSV urls
    """
    csv_urls = []
    base_url = 'https://www.tepco.co.jp'
    for tag in page.find_all('li', {'class': 'btn'}):
        for anchor in tag.find_all('a'):
            csv_urls.append(base_url + anchor['href'])
    return csv_urls

def download_csv():
    """
    This function downloads CSV's from the url, cleans and formats the data,
    and reads to CSV files
    """
    page = get_page()
    csv_urls = get_csv_urls(page)
    
    for url in csv_urls: 
        df = pd.read_csv(url, encoding= 'unicode_escape', header=1, parse_dates=[['DATE', 'TIME']])

        # rename columns, add columns for region and unit
        df.columns = ('Date_Time', 'Demand')
        df['Region'], df['Unit'] = ['Tokyo', 'MW']
        
        # convert from 10,000kW to MW
        df.Demand = df.Demand * 10
        
        # sort by datetime so that most recent data appears up top
        df.sort_values(by='Date_Time',ascending=False, inplace=True)

        # write each year's df to csv
        df.to_csv('Tokyo_{}'.format(url[-8:]), index=False)
        
if __name__ == '__main__':
    download_csv()