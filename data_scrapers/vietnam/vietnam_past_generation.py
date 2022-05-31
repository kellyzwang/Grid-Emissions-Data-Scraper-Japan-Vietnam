# This script scrapes from pdfs for total monthly generation in Vietnam
# Generation is converted from millions of kWh to MWh 
# PDF files were manually downloaded into the 'Vietnam_data' folder, may 
# need to change directory path to load pdf.

from pdfminer.high_level import extract_text
from datetime import datetime
import re
import glob
import pandas as pd

def get_pdf_files(file_path):
    """
    Gets all of the pdf files in the given directory.
    :param file_path: the path of the folder where all pdfs are located
    :return: a list of the pdf files to scrape from
    """
    pdf_dir = file_path
    pdf_files = glob.glob("%s/*.pdf" % pdf_dir)
    return pdf_files

def get_generation(file):
    """
    Parses a pdf file, gets the date and generation data and returns
    a dictionary of formatted data points. 
    :param file: the pdf file to scrape from 
    :return: a dictionary of data points
    """
    data = {}
    key_list = ['Year', 'Month', 'Country', 'Generation', 'Unit']
    text1 = extract_text(file)
    
    # get year and month
    date = re.findall(r'\d+\/\d+', text1)[0]
    date_obj = datetime.strptime(date, '%m/%Y')
    data[key_list[0]] = date_obj.year
    data[key_list[1]] = date_obj.month
    
    # get generation data, convert from million kWh to MWh
    generation = re.findall(r'\d+\,\d+', text1)
    generation = generation[0].replace(',', '.')
    generation = float(generation) * 1_000
    data[key_list[3]] = generation
    
    # add country
    data[key_list[2]] = 'Vietnam'
    # add unit 
    data[key_list[4]] = 'MWh'
    
    return data

def main():
    """
    This is the main function for getting total generation data from each pdf file
    and reading it to a single csv file.
    """
    list_of_data = []
    pdf_files = get_pdf_files("Vietnam_data")
    
    for file in pdf_files:
        data = get_generation(file)
        list_of_data.append(data)
        
    df = pd.DataFrame(list_of_data, index=None).sort_values(by=['Year', 'Month'], ascending=False)
    df.to_csv('Vietnam_generation_data.csv', index=None)
    
if __name__ == '__main__':
    main()