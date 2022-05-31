import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def download_Kyushu_Supply_Demand_data():
    """
    This function downloads all past demand and supply data from the url, 
    clean the data and translate column names, and reads to CSV files.
    Supply data is broken down by fuel type and most recent data appears from the top.
    """
    url = "https://www.kyuden.co.jp/td_service_wheeling_rule-document_disclosure"
    response = requests.get(url)

    # response.status_code is 200 if the website didn't block it
    # raise error if response.status_code != 200
    if response.status_code != 200: 
        raise Exception('Failed to load page {}'.format(url))
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        td_elem = soup.findAll('td', {'class': 'n_align_center'})
        csv_href = []
        for td in td_elem:
            csv_a = td.find('a', {'class': 'n_icon_excel'})
            if csv_a:
                csv_href.append(csv_a.get('href'))

        for i in range(len(csv_href)):
            csv_url = "https://www.kyuden.co.jp/" + csv_href[i]
            df = pd.read_csv(csv_url, encoding='shift-jis')

            # data cleaning
            dflist = []
            for i in range(1, len(df)):
                data_list = list(df.iloc[i])
                if not np.all(pd.isna(data_list)): 
                    dflist.append(data_list)

            df = pd.DataFrame(dflist, columns=list(df.iloc[0]))
            df.columns = ['Date_Time',
                        'Area_Demand',
                       'Nuclear Power', 
                       'Thermal Power',
                       'Hydropower',
                       'Geothermal', 
                       'Biomass',
                       'Solar performance', 
                       'Solar Supression Amount', 
                       'Wind Performance',
                       'Wind Suppression Amount',
                       'Pumped storage',
                       'Interconnector']

            # assign units and region
            df['Region'] = 'Kyushu'
            df['Unit'] = 'MWh'

            # get demand data into one df
            demand_df = df[['Date_Time', 'Region', 'Unit', 'Area_Demand']].copy()
            # sort by datetime so that most recent data appears up top
            demand_df.sort_values(by=['Date_Time'], ascending=False, inplace=True)


            # get supply data into another df
            supply_df = df.copy()
            supply_df.drop('Area_Demand', axis=1, inplace=True)
            supply_df = pd.melt(supply_df, id_vars=['Date_Time','Region', 'Unit'], var_name='Fuel_Type', value_name='Supply')
            # sort by datetime so that most recent data appears up top
            supply_df.sort_values(by=['Date_Time','Fuel_Type'], ascending=False, inplace=True)

            start_date = df['Date_Time'][0].split()[0].replace('/', '-')
            end_date = df['Date_Time'][df['Date_Time'].size-1].split()[0].replace('/', '-')


            # write df to csvs
            demand_df.to_csv('Kyushu_Demand_{}.csv'.format(start_date+"_to_"+end_date), index=False)
            supply_df.to_csv('Kyushu_Supply_{}.csv'.format(start_date+"_to_"+end_date), index=False)


def main():
    download_Kyushu_Supply_Demand_data()


if __name__ == '__main__':
    main()