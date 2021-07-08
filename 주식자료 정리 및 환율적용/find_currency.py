import pandas as pd
from pandas import DataFrame, Series
import datetime

class exchange_currency:
    def __init__(self, date, money, country):
        kr_currency = pd.read_excel('ExchangeUSD.xlsx', header = 0,thousands = ',')
        kr_currency_2 = pd.read_excel('ExchangeKRW.xlsx', header = 0,thousands = ',')
        kr_currency.index = ['일본','유럽','영국','캐나다','호주','뉴질랜드','중국','홍콩']
        kr_currency_2.index = ['한국']

        if date == 'various':
            date = '20200000'
            self.date = date[4:6] + date[6:] + date[:4]
        else:
            try:
                date = date.strftime('%m-%d-%Y %I:%M:%S')
                date = str(date)
                date = date.split(' ')
                date = date[0]
                date = date.replace('-','')
            except:
                pass

            date = str(int(date))
            if len(date) == 8:
                self.date = str(date)
            else:
                self.date = '0' + str(date)

        self.money = money
        self.country = None
        self.operater = None
        country = country.strip().upper()

        if country in ['JP','JAPAN','JPY']:
            self.country = '일본'
            self.operater = 'divi'
        elif country in ['EU','EUR']:
            self.country = '유럽'
            self.operater = 'mult'
        elif country in ['UK','GBP']:
            self.country = '영국'
            self.operater = 'mult'
        elif country in ['CAD','CANADA']:
            self.country = '캐나다'
            self.operater = 'divi'
        elif country in ['CHINA','CNY']:
            self.country = '중국'
            self.operater = 'divi'
        elif country in ['AUD']:
            self.country = '호주'
            self.operater = 'mult'
        elif country in ['NZD']:
            self.country = '뉴질랜드'
            self.operater = 'mult'
        elif country in ['HKD']:
            self.country = '홍콩'
            self.operater = 'divi'
        elif country in ['KRW','KR','WON']:
            self.country = '한국'
            self.operater = 'divi'
        self.kr_currency = kr_currency
        self.kr_currency_2 = kr_currency_2


    def find_exchange_currency(self):
        year = int(self.date[4:])
        month = int(self.date[:2])
        day = int(self.date[2:4])
        result_2 = self.find_exchange_date(year,month,day)
        return [result_2, self.operater]


    def find_exchange_date(self, year, month, day):
        if month == 0:
            temp_time = str(year) + '/' + str(month) + '/' + str(day)
            result = self.kr_currency_2.loc[self.country][str(temp_time)]
            self.date = 'various'
            return result
        else:
            find_columns = datetime.date(year, month, day)
            while True:
                try:
                    temp_time = str(find_columns).replace('-','/')
                    if self.country != '한국':
                        result = self.kr_currency.loc[self.country][str(temp_time)]
                    else:
                        result = self.kr_currency_2.loc[self.country][str(temp_time)]

                    break
                except:
                    find_columns = find_columns - datetime.timedelta(days=1)
                    continue
            return result