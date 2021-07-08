import pandas as pd
from pandas import DataFrame, Series

stock_data = pd.read_excel('주식 업로드 템플릿(아직 사이트에는 반영중, 당장 업로드는 불가).xls',header = 9,usecols = [1,4,5,6,7,8,11], thousands = ',', dtype = object)
#converters= {'(b)\nDate acquired mmddyyyy': pd.to_datetime, '(c) \nDate sold or disposed of mmddyyyy':pd.to_datetime}
print(stock_data.head())
stock_data.to_excel('test1.xlsx')
stock_data = stock_data.drop(index = 0, axis = 0)
stock_data.reset_index(drop = True, inplace = True)
stock_data.columns = ['Description', 'Type', 'Date Acquired', 'Date Sold', 'Proceeds', 'Cost', 'currency']
stock_data = stock_data[['Description', 'Date Acquired', 'Date Sold', 'Type', 'Proceeds', 'Cost', 'currency']]
print(stock_data.head())

