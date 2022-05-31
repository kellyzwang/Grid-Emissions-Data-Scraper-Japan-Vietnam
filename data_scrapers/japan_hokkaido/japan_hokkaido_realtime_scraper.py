# The codes extract the realtime hourly performance data and 5-minutes data from
# a downloadable csv in file from http://denkiyoho.hepco.co.jp/area_forecast.html
# Writes the latest performance data to a csv file.
# Values are originally provided in 10,000 kW, the codes below converts to MW.
import csv
import os
import datetime
import requests
from bs4 import BeautifulSoup

def get_data_pos(data):
    """
    This function loops through all lines in the the csv file to get 
    the position of the 1 hour and 5 minute performance tables
    :param data: a list of all strings in the csv file
    :return: a list of the starting position of the 1 hour and 5 minute tables
    """
    data_position = []
    for i in range(len(data)): 
        if 'DATE,TIME,' in data[i]:
            data_position.append(i)
    return data_position

def get_data_values(data, table_pos, table_length):
    """
    This function loops through all rows starting from the given table_pos
    to check for the latest performance data. Returns the date, time, and 
    values of the latest data row. 
    :param data: a list of all strings in the csv file
    :param table_pos: the starting position of either the one-hour or 5-min table
    :param table_length: the expected length of either the one-hour or 5-min table
    :return: list of latest performance data values
    """
    for i in range(table_length):
        data_row = data[table_pos + i + 1].strip().split(',')
        date = data_row[0].strip()
        time = data_row[1].strip()
        
        # get one hour performance
        if len(data_row) == 6:
            perf = data_row[2].strip()
            estimated_perf = data_row[3].strip()
            usage_rate = data_row[4].strip()
            supply = data_row[5].strip()        
            if not perf:
                break            
            perf_data = [date, time, perf, estimated_perf, usage_rate, supply]
        
        # get 5 min performance
        else:
            perf = data_row[2].strip()
            solar_perf = data_row[3].strip()
            if not perf:
                break
            perf_data = [date, time, perf, solar_perf]
            
    return perf_data

def format_data(data):
    """
    Reformats given data values to categories: Date_Time, Region, Data_Type, and Value
    :param data: the latest data values from the performance table
    :return: a list of dictionaries of formatted performance data
    """
    formatted_data = []
    date_time = datetime.datetime.strptime(data[0] + ' ' + data[1], '%Y/%m/%d %H:%M')
    
    if len(data) == 6:
        formatted_data.append({'Date_Time': date_time, 'Region':'Hokkaido', 
                           'Data_Type':'Hourly Performance', 'Unit':'MW', 
                           'Value': int(data[2]) * 10})
        formatted_data.append({'Date_Time': date_time, 'Region':'Hokkaido', 
                           'Data_Type':'Estimated Hourly Performance', 'Unit':'MW', 
                           'Value': int(data[3]) * 10})
        formatted_data.append({'Date_Time': date_time, 'Region':'Hokkaido', 
                           'Data_Type':'Hourly Usage Rate', 'Unit':'%', 
                           'Value': int(data[4])})
        formatted_data.append({'Date_Time': date_time, 'Region':'Hokkaido', 
                           'Data_Type':'Estimated Hourly Supply', 'Unit':'MW', 
                           'Value': int(data[5]) * 10})    
    else:
        formatted_data.append({'Date_Time': date_time, 'Region':'Hokkaido', 
                           'Data_Type':'5-Minute Performance', 'Unit':'MW', 
                           'Value': int(data[2]) * 10})
        formatted_data.append({'Date_Time': date_time, 'Region':'Hokkaido', 
                           'Data_Type':'5-Minute Solar Performance', 'Unit':'MW', 
                           'Value': int(data[3]) * 10})                
    return formatted_data

def write_to_csv(latest_data):
    """
    Writes the latest performance data to a CSV file.
    :param latest_data: list of realtime performance data
    """
    csv_columns = ['Date_Time','Region','Data_Type', 'Unit', 'Value']
    csv_file = "Realtime_Hokkaido_Data.csv"

    # if file does not exist write header and read to csv 
    if not os.path.isfile(csv_file):
        with open(csv_file, "w+") as f:
            csvwriter = csv.DictWriter(f, csv_columns)
            csvwriter.writeheader()
            csvwriter.writerows(latest_data)
    else: # else if exists, append data without writing the header
        with open(csv_file,'a') as f:
            csvwriter = csv.DictWriter(f, csv_columns)
            csvwriter.writerows(latest_data) 
    
def main():
    """
    The main function for getting the link to the CSV that has realtime 1 hour and
    5 minute performance data. Parses the CSV for the latest 1 hour and 5 minute 
    data. Then, reads formatted data values to a CSV.
    """
    url = 'http://denkiyoho.hepco.co.jp/area_forecast.html'
    base_url = 'http://denkiyoho.hepco.co.jp/'
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('Failed to load page {}'.format(url))
    page = BeautifulSoup(r.text, 'html.parser')
    relative_link = page.find('a', {'class':'ic_csv'}).get('href')
    csv_url = base_url + relative_link   
    
    r = requests.get(csv_url)
    data = r.text.split('\n')
    data_position = get_data_pos(data)
    
    latest_hourly_perf = get_data_values(data, data_position[0], 24)
    latest_five_min_perf = get_data_values(data, data_position[1], 288)        
    latest_data = format_data(latest_hourly_perf) + format_data(latest_five_min_perf)
    write_to_csv(latest_data)              
    
if __name__ == '__main__':
    main()