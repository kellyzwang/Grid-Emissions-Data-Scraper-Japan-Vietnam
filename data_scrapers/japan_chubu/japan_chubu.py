# This is for Japan data source, Chubu Electric Power.
# Author: Sang-Won Yu

# NOTE: The data source starts from April 2016 until now. There are separate CSVs for each year. 
# Each CSV starts from April, and ends in March the following year, because fiscal year in Japan
# is from April through March. Chubu Electric Power serves the Chubu region, which is located in
# the middle of Honshu Island, the main island of Japan. 

import pandas as pd
import numpy as np
from datetime import datetime

def read_chubu_csv():
    combined_data = pd.DataFrame()
    for year in range(2016, datetime.now().year + 1):
        csv = pd.read_csv('https://powergrid.chuden.co.jp/denki_yoho_content_data/' +
                          str(year) + '_areabalance_current_term.csv', header = 4,
                          encoding = 'shift_jis')
        combined_data = combined_data.append(csv, ignore_index=True)
    # Translate Japanese column names to English
    combined_data.columns = ['Date', 'Time', 'Area_Demand', 'Nuclear', 'Thermal',
                          'Hydraulic', 'Geothermal', 'Biomass', 'Solar(Actual)',
                          'Solar(Output_Control)', 'Wind(Actual)', 'Wind(Output_Control)',
                          'Pumped_Hydro', 'Interconnector']

    # assign units and region
    combined_data['Region'] = 'Chubu'
    combined_data['Unit'] = 'MWh'

    # combine columns 'DATE' and 'TIME' to make a datetime object
    combined_data['Date']=pd.to_datetime(combined_data['Date'] + ' ' + combined_data['Time'], format='%Y/%m/%d %H:%M')
    combined_data.drop('Time', axis=1, inplace=True)
    combined_data.rename(columns={"Date": "Date_Time"}, inplace=True)

    # get demand data into one df
    demand_df = combined_data[['Date_Time', 'Region', 'Unit', 'Area_Demand']].copy()
    demand_df.sort_values(by=['Date_Time'],ascending=False, inplace=True)

    # get supply data into another df
    supply_df = combined_data
    supply_df.drop('Area_Demand', axis=1, inplace=True)
    # Pivot "wide" to "long" format
    supply_df = pd.melt(combined_data, id_vars=['Date_Time','Region', 'Unit'], var_name='Fuel_Type', value_name='Supply')
    supply_df.sort_values(by=['Date_Time','Fuel_Type'], ascending=False, inplace=True)

    return demand_df, supply_df

if __name__ == '__main__':
    chubu_data = read_chubu_csv()
    chubu_data[0] # demand data
    chubu_data[1] # supply data