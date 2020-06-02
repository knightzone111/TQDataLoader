# TQDataLoader
TQ DataLoader API Wrapper. Built on tqsdk.    
https://github.com/shinnytech/tqsdk-python   

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

## TO DO  
- Add in GUI to make it easier for data downloading and data visualization: use dash? (web ui?)  
https://dash.plotly.com/ 
- a dropdown list of contracts grouped by exchange or market  
- Add features to display prices, volume, etc...

 
