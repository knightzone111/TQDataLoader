# TQDataLoader
TQ DataLoader API Wrapper. Built on tqsdk.     
A robust tool for streamlining the financial data processing, downloading, and visualization.   
The goal is to develop a data platform that aggregates useful financial data for alpha researching.    
https://github.com/shinnytech/tqsdk-python    

数据下载，数据可视化，数据分析工具。 

## Requirements  
tqsdk 1.8  

## Features
Data visualization is built on dash module. Dash is a great package in python dealing with web-based charts and interactive plots.  
1. Chinese Futures Data downloading and udpating periodically.   
2. Single product klines and volume display. 
3. 3D surface term structure plot. 
4. Automated data loading. 

## Usage 
Use `download_data` function to create tasks and downloading data.  
Obtain data in pandas dataframe format using `read_data` function.   
symbol has format "{0}.{1}{2}{3}".format(exchange, root, yy, mm), like "SHFE.rb2010".   
start_date, end_date are generally in string format "yyyy-mm-dd", though can be in other date format as  well.     
The freq is one of the following: "tick", "s", "min", "5min", "h", "D"    
'Data' is the folder for storing downloaded csv data.  

Example:  
```python
    data_task = download_data(["SHFE.rb2010"], "2020-06-01", "2020-06-02", 'tick', 'Data')
    df = read_data('SHFE.rb2010', 'tick')
```

## Available Exchange and Contracts   
- SHFE 上海期货交易所
    - rb,hc,ni镍,bu沥青,
- DCE 大连商品交易所  
    - j焦炭, jm 焦煤, p, pg 液化石油气, 
- CZCE  郑州商品交易所  
    - MA 甲醇
- INE 上海能源中心  
    - sc 原油
- KQ 快期（所有主连合约，指数)  
- SSWE 上期所仓单  
- SSE 上海证券交易所   
- SZSE 深圳证券交易所  


