import pandas as pd
from pandas import *
import find_currency
from find_currency import *
import sys
import os
import datetime
from datetime import *
import numpy

def work(file_name):
    path = os.getcwd() + '\\'
    stock_data = pd.read_excel(path + str(file_name),header = 9,usecols = [1,4,5,6,7,8,11], thousands = ',', dtype = object)
    #converters= {'(b)\nDate acquired mmddyyyy': pd.to_datetime, '(c) \nDate sold or disposed of mmddyyyy':pd.to_datetime}
    stock_data = stock_data.drop(index = 0, axis = 0)
    stock_data.reset_index(drop = True, inplace = True)
    stock_data.columns = ['Description', 'Type', 'Date Acquired', 'Date Sold', 'Proceeds', 'Cost', 'currency']
    stock_data = stock_data[['Description', 'Date Acquired', 'Date Sold', 'Type', 'Proceeds', 'Cost', 'currency']]
    stock_data = stock_data.dropna(subset = ['Description', 'Date Acquired'])
    temp = pd.DataFrame(columns =  ['TSJ', 'F', 'State', 'City', 'Form 8949 Check Box','Ordinary'] )
    # 'AMT Cost Basis','Accrued Discount','Wash Sale Loss','US Real Property','Adj 1 Code','Adj 1 Amount','Adj 1 AMT Amount','Adj 2 Code','Adj 2 Amount','Adj 2 AMT Amount','Adj 3 Code','Adj 3 Amount','Adj 3 AMT Amount','Fed W/H','Loss Not Allowed','Collectibles','QSBS Code','QSBS Amount','State','State ID #','State Tax W/H','State 2','State 2 ID #','State Tax W/H','State Use Code','State Adjustment','State Cost/Basis','LLC Number'])
    for i in range(len(stock_data.index)):
        stock_data.iat[i,3] = stock_data.iloc[i][3][0]

    for i in range(len(stock_data.index)):
        print(i)
        if pd.notnull(stock_data.iloc[i][6]):
            if stock_data.iloc[i][6] not in ['USD', 'usd', 'us', 'US', 'USA', 'usa'] :

                acquired_data = exchange_currency(stock_data.iloc[i][1], stock_data.iloc[i][5], stock_data.iloc[i][6])
                alist = acquired_data.find_exchange_currency()
                if alist[1] == 'divi':
                    stock_data.iat[i,5] = round(stock_data.iloc[i][5]/alist[0])
                    stock_data.iat[i,1] = acquired_data.date
                else:
                    stock_data.iat[i,5] = round(stock_data.iloc[i][5]*alist[0])
                    stock_data.iat[i,1] = acquired_data.date

                sold_data = exchange_currency(stock_data.iloc[i][2], stock_data.iloc[i][4], stock_data.iloc[i][6])
                slist = sold_data.find_exchange_currency()
                if slist[1] == 'divi':
                    stock_data.iat[i,4] = round(stock_data.iloc[i][4]/slist[0])
                    stock_data.iat[i,2] = sold_data.date
                else:
                    stock_data.iat[i,4] = round(stock_data.iloc[i][4]*slist[0])
                    stock_data.iat[i,2] = sold_data.date
            else:
                pass
        else:
            stock_data.iat[i,5] = round(stock_data.iat[i,5])
            stock_data.iat[i,4] = round(stock_data.iat[i,4])
            continue
            
    stock_data.drop(columns = ['currency'], axis = 1, inplace = True)

    merged_data = pd.concat([stock_data, temp], axis = 1)
    merged_data = merged_data[['TSJ', 'F','State','City','Form 8949 Check Box','Description','Date Acquired','Date Sold','Type','Ordinary','Proceeds','Cost']]
    #'AMT Cost Basis','Accrued Discount','Wash Sale Loss','US Real Property','Adj 1 Code','Adj 1 Amount','Adj 1 AMT Amount','Adj 2 Code','Adj 2 Amount','Adj 2 AMT Amount','Adj 3 Code','Adj 3 Amount','Adj 3 AMT Amount','Fed W/H','Loss Not Allowed','Collectibles','QSBS Code','QSBS Amount','State','State ID #','State Tax W/H','State 2','State 2 ID #','State Tax W/H','State Use Code','State Adjustment','State Cost/Basis','LLC Number']]
    merged_data['Form 8949 Check Box'] = 3
    # for i in range(len(merged_data.index)):
    #     merged_data.iloc[i][6] = merged_data.iloc[i][6].astype(numpy.int64)
    #     print(merged_data.iloc[i][6])
    #     print(type(merged_data.iloc[i][6]))
    #     merged_data.iloc[i][7] = merged_data.iloc[i][7].astype(str)
    #     if len(str(merged_data.iloc[i][6])) == 7:
    #         merged_data.iat[i,6] = '0' + str(merged_data[i][6])
    #     if len(str(merged_data.iloc[i][7])) == 7:
    #         merged_data.iat[i,7] = '0' + str(merged_data[i][7])
    merged_data.to_excel('excel_drake.xlsx', index = False)
    
# 판매 연도 마다 새 엑셀 파일에 주식 거래를 저장해서 추출해야 한다.