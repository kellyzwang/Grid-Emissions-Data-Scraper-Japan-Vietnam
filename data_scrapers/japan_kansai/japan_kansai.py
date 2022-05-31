import pandas as pd
import numpy as np
from datetime import datetime
from urllib.request import Request, urlopen  # Python 3

def read_kansai_csv():
    combined_data = pd.DataFrame()
    for year in range(2016, datetime.now().year + 1):
        # Bypass 403 Forbidden error
        req = Request('https://www.kansai-td.co.jp/denkiyoho/csv/area_jyukyu_jisseki_' +
                          str(year) + '.csv')
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
        content = urlopen(req)

        csv = pd.read_csv(content, header = 1, encoding = 'shift_jis')

        # Combine multi-year CSVs into one dataframe
        combined_data = combined_data.append(csv, ignore_index=True)

        # Drop NaN columns
        combined_data.drop(combined_data.iloc[:, 13:], axis=1, inplace=True)

    # Translate Japanese column names to English
    combined_data.columns = ['Date_Time', 'Area_Demand', 'Nuclear', 'Thermal',
                          'Hydraulic', 'Geothermal', 'Biomass', 'Solar(Actual)',
                          'Solar(Output_Control)', 'Wind(Actual)', 'Wind(Output_Control)',
                          'Pumped_Hydro', 'Interconnector']

    # assign units and region
    combined_data['Region'] = 'Kansai'
    combined_data['Unit'] = 'MWh'

    # Format the datetime
    combined_data['Date_Time']=pd.to_datetime(combined_data['Date_Time'], format='%Y/%m/%d %H:%M')

    # get demand data into one df
    demand_df = combined_data[['Date_Time', 'Region', 'Unit', 'Area_Demand']].copy()
    demand_df.sort_values(by=['Date_Time'],ascending=False, inplace=True)
    # Drop NaN rows (not sure why there are NaN rows...)
    demand_df.dropna(inplace = True)

    # get supply data into another df
    supply_df = combined_data
    supply_df.drop('Area_Demand', axis=1, inplace=True)
    # Pivot "wide" to "long" format
    supply_df = pd.melt(combined_data, id_vars=['Date_Time','Region', 'Unit'], var_name='Fuel_Type', value_name='Supply')
    supply_df.sort_values(by=['Date_Time','Fuel_Type'], ascending=False, inplace=True)
    # Drop NaN rows (not sure why there are NaN rows...)
    supply_df.dropna(inplace = True)

    return demand_df, supply_df

if __name__ == '__main__':
    demand_df, supply_df = read_kansai_csv()
#     demand_df
#     supply_df
    