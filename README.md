# UW Data Scrapers 5 – Japan and Vietnam

This project scrapes from multiple sources to obtain archived and real-time electricity grid data from the countries Japan and Vietnam.

Sources we found:
1. Tokyo: https://www.tepco.co.jp/en/forecast/html/index-e.html
2. Hokuriku: https://www.rikuden.co.jp/nw/denki-yoho/index.html
3. Kansai: https://www.kansai-td.co.jp/denkiyoho/index.html
4. Kyushu: https://www.kyuden.co.jp/td_power_usages/pc.html
5. Shikoku: https://www.yonden.co.jp/nw/denkiyoho/index.html
6. Tohoku: https://setsuden.nw.tohoku-epco.co.jp/graph.html
7. Chugoku: https://www.energia.co.jp/nw/jukyuu/
8. Chubu: https://powergrid.chuden.co.jp/denkiyoho/
9. Hokkaido: http://denkiyoho.hepco.co.jp/area_forecast.html
10. Japan system price: http://www.jepx.org/english/index.html  
11. Past Japan supply/demand for all regions: https://www.renewable-ei.org/en/statistics/electricity/#demand
12. Vietnam monthly generation: https://www.evn.com.vn/c3/pages-c/Thi-truong-dien-6-15.aspx
13. Vietnam load and price: https://www.nldc.evn.vn

## Tokyo
`japan_tokyo.py` scrapes for all available past hourly demand data (from 2016-April, 2022). Supply data is not available. We noticed that there is already an existing scraper for real-time performance data by WattTime for this source, so we only scraped for past demand data.



## Hokuriku
`japan_hokuriku.py` downloads all past hourly demand and supply data (broken down by fuel types). The script will write demand and supply data to different CSVs.
Demand CSVs contain values for the following columns: Date_time, Region, Unit, and Area_Demand.
Supply CSVs contain values for the following columns: Date_time, Region, Unit, Fuel_Type, and Supply.

`japan_hokuriku_realtime_scraper.py` scrapes for real time data from a CSV link on the main page. The CSV gets updated every 5-minute with new performance data. The script will scrape and write to a CSV the actual hourly performance, estimated hourly performance, hourly usage rate, hourly supply, 5-minute performance, and 5-minute solar performance data.
Data will have the following columns: Date_Time, Region, Data_Type, Unit, and Value

*(Note: data for other regions in Japan will also have the same formatting with the same columns.)*



## Kansai
`japan_kansai.py` downloads all past hourly demand and supply data (broken down by fuel types).

`japan_kansai_realtime_scraper.py` scrapes for real time data from a CSV link on the main page. The CSV gets updated every 5-minute with new performance data. The script will scrape and write to a CSV the actual hourly performance, estimated hourly performance, hourly usage rate, hourly supply, 5-minute performance, and 5-minute solar performance data.



## Kyushu
`japan_kyushu.py` downloads all past hourly demand and supply data (broken down by fuel types).

`japan_kyushu_realtime_scraper.py` scrapes for real time data from a CSV link on the main page. The CSV gets updated every 5-minute with new performance data. The script will scrape and write to a CSV the actual hourly performance, estimated hourly performance, hourly usage rate, hourly reserve rate, hourly supply, 5-minute performance, and 5-minute solar performance data.



## Shikoku
`japan_shikoku.py` downloads all past hourly demand and supply data (broken down by fuel types).

`japan_shikoku_realtime_scraper.py` scrapes for real time data from a CSV link on the main page. The CSV gets updated every 5-minute with new performance data. The script will scrape and write to a CSV the actual hourly performance, estimated hourly performance, hourly usage rate, hourly supply, 5-minute performance, and 5-minute solar performance data.



## Tohoku
`japan_tohoku.py` downloads all past hourly demand and supply data (broken down by fuel types).

`japan_tohoku_realtime_scraper.py` scrapes for real time data from a CSV link on the main page. The CSV gets updated every 5-minute with new performance data. The script will scrape and write to a CSV the actual hourly performance, estimated hourly performance, hourly usage rate, hourly supply, 5-minute performance, 5-minute solar performance, and 5-minute wind performance data.



## Chugoku
`japan_chugoku.py` downloads all past hourly demand and supply data (broken down by fuel types).

`japan_chugoku_realtime_scraper.py` scrapes for real time data from a CSV link on the main page. The CSV gets updated every 5-minute with new performance data. The script will scrape and write to a CSV the actual hourly performance, estimated hourly performance, hourly usage rate, hourly supply, 5-minute performance, and 5-minute solar performance data.



## Chubu
`japan_chubu.py` downloads all past hourly demand and supply data (broken down by fuel types).

`japan_kyushu_realtime_scraper.py` scrapes for real time data from a CSV link on the main page. The CSV gets updated every 5-minute with new performance data. The script will scrape and write to a CSV the actual hourly performance, estimated hourly performance, hourly usage rate, hourly supply, 5-minute performance, and 5-minute solar performance data.



## Hokkaido
`japan_hokkaido.py` downloads all past hourly demand and supply data (broken down by fuel types).

`japan_hokkaido_realtime_scraper.py` scrapes for real time data from a CSV link on the main page. The CSV gets updated every 5-minute with new performance data. The script will scrape and write to a CSV the actual hourly performance, estimated hourly performance, hourly usage rate, hourly reserve rate, hourly supply, 5-minute performance, and 5-minute solar performance data.



## Japan system price
This source has data on system price and area electricity price for all regions in Japan. System price is the day-ahead price at which electricity is traded. `japan_archived.py` should download all pricing data from 2005 to the most recent day’s data. `japan_daily_scraper.py` scrapes for only the latest daily data and write it to a CSV.



## Past Japan supply/demand for all regions
This source has an API for accessing past hourly demand/supply data from 2016 - March, 2022. Supply data is provided by power types. There are demand/supply and JEPX system price data for individual regions in Japan.



## Vietnam monthly generation
`vietnam_past_generation.py` scrapes from all pdfs located in the ‘Vietnam_data’ folder. The pdfs were manually downloaded from the EVN’s website. We were only able to get data from October, 2020 to February, 2022 because other records of data are in the form of videos instead of pdfs.

The pdfs contain data on total monthly generation, which we scraped for. The pdfs also contain data on accumulation of generation (by power type) since the beginning of each year, but the format of the pdfs is inconsistent and some have missing data, so we did not scrape for this.  

The columns of the final csv include: Year, Month, Generation, Country, Unit



## Vietnam load and price
This source has an API for accessing real time electricity load and price data. Load is measured in MW and price is measured in Vietnam dong per kwh.
