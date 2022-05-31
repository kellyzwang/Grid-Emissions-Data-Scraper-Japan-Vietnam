# This is for Japan data source #6, Hokkaido Electric Power.
# Contributor(s): Sang-Won Yu

# Japanese fiscal year starts in every April.
# Which means 1st quarter = April, May, June; 2nd quarter = July, August, September etc.
# For Hokkaido, CSVs are quarterly instead of yearly.

# importing necessary modules
import pandas as pd
import numpy as np
from datetime import datetime

def read_hokkaido_csv():
    combined_data = pd.DataFrame()
    for year in range(2016, datetime.now().year + 1): # 2016 - current year
        for quarter in range(1, 5): # 1st quarter - 4th quarter
            try:
                csv = pd.read_csv('https://www.hepco.co.jp/network/renewable_energy/fixedprice_purchase/csv/sup_dem_results_' +
                                  str(year) + '_' + str(quarter) + 'q.csv', header = 2, encoding = 'shift_jis')
                csv.drop(labels=0, axis=0, inplace=True) # Delete the empty row at the beginning of the CSV
                combined_data = combined_data.append(csv, ignore_index=True)
            except: # If no such CSV exists yet, skip
                continue

    combined_data = combined_data.replace(np.nan).ffill() # Fill empty trailing values with last known value (for dates)
    combined_data['時刻'] = combined_data['時刻'].str.replace(r'時$',':00') # Fix the format of the time. "時" means "hour".
    combined_data.drop('供給力合計', axis=1, inplace=True) # Delete 供給力合計 column, it's just supply total.

    # combine columns 'DATE' and 'TIME' to make a datetime object
    combined_data['月日']=pd.to_datetime(combined_data['月日'] + ' ' + combined_data['時刻'], format='%Y/%m/%d %H:%M')
    combined_data.drop('時刻', axis=1, inplace=True)

    # Translate Japanese column names to English
    combined_data.columns = ['Date_Time', 'Area_Demand', 'Nuclear', 'Thermal',
                          'Hydraulic', 'Geothermal', 'Biomass', 'Solar(Actual)',
                          'Solar(Output_Control)', 'Wind(Actual)', 'Wind(Output_Control)',
                          'Pumped_Hydro', 'Interconnector']

    # assign units and region
    combined_data['Region'] = 'Hokkaido'
    combined_data['Unit'] = 'MWh'

    # get demand data into one df
    demand_df = combined_data[['Date_Time', 'Region', 'Unit', 'Area_Demand']].copy()
    demand_df.sort_values(by=['Date_Time'],ascending=False, inplace=True)

    # get supply data into another df
    supply_df = combined_data
    supply_df.drop('Area_Demand', axis=1, inplace=True)
    supply_df = pd.melt(combined_data, id_vars=['Date_Time','Region', 'Unit'], var_name='Fuel_Type', value_name='Supply')
    supply_df.sort_values(by=['Date_Time','Fuel_Type'], ascending=False, inplace=True)

    # write df to csvs
    # demand_df.to_csv('Hokkaido_Demand')
    # supply_df.to_csv('Hokkaido_Supply')
  
    return demand_df, supply_df

if __name__ == '__main__':
    hokkaido_data = read_hokkaido_csv()
    hokkaido_data[0] # demand data
    hokkaido_data[1] # supply data