import requests
import pandas as pd
import os
from datetime import datetime

def get_latest_data():
    """
    Function for scraping daily system price and area price data from CSV file 
    from http://www.jepx.org/english/market/index.html.
    Writes daily data to a csv file. If the csv already exists, append new
    data to it, otherwise create new csv with new data.
    """
    currentYear = datetime.now().year
    url = 'http://www.jepx.org/market/excel/spot_{}.csv'.format(currentYear)
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('Failed to load page {}'.format(url))
        
    df = pd.read_csv(url, encoding='shift-jis').tail(48)
    df = df[['年月日', '時刻コード', 'システムプライス(円/kWh)',
             'エリアプライス北海道(円/kWh)', 'エリアプライス東北(円/kWh)',
             'エリアプライス東京(円/kWh)', 'エリアプライス中部(円/kWh)',
             'エリアプライス北陸(円/kWh)', 'エリアプライス関西(円/kWh)',
             'エリアプライス中国(円/kWh)', 'エリアプライス四国(円/kWh)',
             'エリアプライス九州(円/kWh)']]
    
    df.columns  = ('Date', 'Time_code', 'System price (yen/kWh)',
                   'Area Price Hokkaido (yen/kWh)', 'Area Price Tohoku (yen/kWh)',
                   'Area Price Tokyo (yen/kWh)', 'Area Price Chubu (yen/kWh)',
                   'Area Price Hokuriku (yen/kWh)', 'Area Price Kansai (yen/kWh)',
                   'Area Price Chūgoku (yen/kWh)', 'Area Price Shikoku (yen/kWh)',
                   'Area Price Kyushu (yen/kWh)')

    csv_file = 'Spot_Market_Trading_Results_Price_{}.csv'.format(currentYear)
    df.to_csv(csv_file, mode='a', header=not os.path.exists(csv_file))
            
if __name__ == '__main__':
    get_latest_data()