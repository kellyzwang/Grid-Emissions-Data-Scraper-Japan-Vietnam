import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_price_data():
    """
    This function downloads price data from 2022 back to 2005
    in Spot Market Trading Results CSVs from the url,
    clean the data, and reads to CSV files

    Note: Time_code: Time zone every 30 minutes divided into 1 to 48
    """
    url = "http://www.jepx.org/english/market/index.html"
    response = requests.get(url)

    # response.status_code is 200 if the website didn't block it
    # raise error if response.status_code != 200
    if response.status_code != 200: 
        raise Exception('Failed to load page {}'.format(url))
    else:
        soup = BeautifulSoup(response.text, 'html.parser')

        # get csv URLs for spot market trading results
        trading_results_csv_url = []
        for link in soup.find_all('a', {'class': 'arw'}):
            relative_link_to_csv = link.get('href') # looks like "../../market/excel/spot_2022.csv"

            # cut off "../../"
            relative_link_to_csv = relative_link_to_csv[6:]

            # combine "http://www.jepx.org" and relative_link_to_csv,
            # add to trading_results_csv_url 
            combined_url = "http://www.jepx.org/" + relative_link_to_csv

            if "spot" in combined_url:
                trading_results_csv_url.append(combined_url)

        for i in range(len(trading_results_csv_url)):
            df = pd.read_csv(trading_results_csv_url[i], encoding='shift-jis')

            # drop columns other than date, time, system price and area price.
            df = df[['年月日', '時刻コード', 'システムプライス(円/kWh)', 'エリアプライス北海道(円/kWh)',
                   'エリアプライス東北(円/kWh)', 'エリアプライス東京(円/kWh)', 'エリアプライス中部(円/kWh)', 
                   'エリアプライス北陸(円/kWh)', 'エリアプライス関西(円/kWh)', 'エリアプライス中国(円/kWh)',
                   'エリアプライス四国(円/kWh)', 'エリアプライス九州(円/kWh)']]

            # translate and rename columns
            df.rename({'年月日': 'Date',
                     '時刻コード': 'Time_code',
                     'システムプライス(円/kWh)': 'System price (yen/kWh)',
                     'エリアプライス北海道(円/kWh)': 'Area Price Hokkaido (yen/kWh)',
                     'エリアプライス東北(円/kWh)': 'Area Price Tohoku (yen/kWh)', 
                     'エリアプライス東京(円/kWh)': 'Area Price Tokyo (yen/kWh)',
                     'エリアプライス中部(円/kWh)': 'Area Price Chubu (yen/kWh)', 
                     'エリアプライス北陸(円/kWh)': 'Area Price Hokuriku (yen/kWh)', 
                     'エリアプライス関西(円/kWh)': 'Area Price Kansai (yen/kWh)',
                     'エリアプライス中国(円/kWh)': 'Area Price Chūgoku (yen/kWh)',
                     'エリアプライス四国(円/kWh)': 'Area Price Shikoku (yen/kWh)', 
                     'エリアプライス九州(円/kWh)': 'Area Price Kyushu (yen/kWh)'}, axis=1, inplace=True)

            year = trading_results_csv_url[i].split("_")[1]
            return df
            
            df.to_csv('Spot_Market_Trading_Results_Price_{}'.format(year), index=False)

def main():
    get_price_data()

if __name__ == '__main__':
    main()