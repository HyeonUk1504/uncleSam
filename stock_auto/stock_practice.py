import pandas as pd
from pandas import DataFrame, Series
import stock_data
from stock_data import *
import datetime
import sys
import os
import datetime
from datetime import *
import numpy




def work(file_name):
    path = os.getcwd() + '\\'
    stock_work_book = pd.read_excel(path + str(file_name), header = 0 ,thousands = ',', dtype = object, usecols=[0,1,2,3,4,5,6]) #거래일자,거래종류,종목명,수량,거래금액,수수료,통화
    stock_work_book =  stock_work_book.dropna( subset = ['거래일자','종목명','수량'])

    #워크북의 Timestamp형 자료를 String으로 강제 변환
    # 여러가지 날짜 입력 변수를 전처리
    for i in range(len(stock_work_book.index)):
        stock_trade_time = str(stock_work_book.iloc[i][0])

        try:
            stock_trade_time = stock_trade_time.strftime('%m-%d-%Y %I:%M:%S')
            stock_trade_time = str(stock_trade_time)
            stock_trade_time = stock_trade_time.split(' ')
            stock_trade_time = stock_trade_time[0]
            stock_trade_time = stock_trade_time.replace('-','')
        except:
            pass
        
        try:
            if stock_trade_time[:2] == '20':
                stock_trade_time = stock_trade_time.replace('.','')
                stock_trade_time = stock_trade_time.replace('-','')
                stock_trade_time = stock_trade_time.replace('/','')
                temp_form_stock_trade_time = stock_trade_time[4:6] + stock_trade_time[6:8] + stock_trade_time[:4]
                stock_trade_time = temp_form_stock_trade_time
            else:
                stock_trade_time = stock_trade_time.replace('.','')
                stock_trade_time = stock_trade_time.replace('-','')
        except:
            pass
        stock_trade_time = str(int(stock_trade_time))
        
        if len(stock_trade_time) == 8:
            stock_trade_time = str(stock_trade_time)
        else:
            stock_trade_time = '0' + str(stock_trade_time)
        stock_work_book.iat[i,0] = stock_trade_time
    # stock_work_book['총거래금액'] = stock_work_book['거래금액']  #+ stock_work_book['수수료']
    # stock_work_book.drop(['거래금액', '수수료'], axis = 1,inplace = True)
    stock_work_book = stock_work_book[['거래일자', '거래종류','종목명','수량','거래금액','통화']]
    print(stock_work_book)
    #한행씩 읽어 오면서 큐에 넣는다...
    #무슨 통화로 거래했는지 알아야한다....


    stock_queue = {}
    result_stock = pd.DataFrame()
    need_info_stock = pd.DataFrame()
    for i in range(len(stock_work_book.index)):
        stock = stock_work_book.iloc[i]
        stock = list(stock)
        stock[2] = stock[2].strip()

        

    #해당 주식 구매
    #해당 주식이 원래 갖고 있는 주식과 동일한 주식인지 dict내에 확인
    #노드를 만들어서 구매일, 수량, 단가 정보를 넣는다.
    #갖고 있다면 해당 주식의 queue에 삽입, 이때 해당날짜가 그 당시의단가 및 환율 저장
    #갖고 있지 않다면 dict에 해당 주식이름을 key로 삽입하고 ,해당 주식을 위한 new queue를 생성 및 value에 삽입 해야함, 이때 해당날짜가 그 당시의 환율 자료를 저장   
    # stock = ['거래일자', '거래종류','종목명','수량','총거래금액','통화']
        flag = True
        print(stock)
    #--------------------------------------------------주식구매-----------------------------------------------------------------
        if '매수' in stock[1]:
            #동일 주식큐가 없는 경우, 새 queue를 만든다
            if stock[2] not in stock_queue:
                stock_queue[stock[2]] = stock_data.Queue()
                print(stock)
                stock_queue.get(stock[2]).enqueue(stock[2], stock[0], stock[3], stock[4], stock[5])
            #동일 주식 큐가 있는 경우, 기존의 큐에 삽입한다.
            else:
                print(stock)
                stock_queue.get(stock[2]).enqueue(stock[2], stock[0], stock[3], stock[4], stock[5])

        #----------------------------------------------------주식판매--------------------------------------------------------------------
        elif '매도' in stock[1]:  #################판매할 때 엑셀에 Node를 기록을 해야한다. type이 L인지 S인지도 결정해야 한다.... profit을 계산할 때 거리비용을 차감할 것인지도...
            #판매수량과 Node의 quantity양 비교
            #sold_stock = [종목명,보유기간,매수일,매도일,매도가격,매수가격,양도차익,양도소득세,통화]
            print(stock)
            while flag:
                if stock[3] == 0:
                    break

                try:                
                    if stock_queue.get(stock[2]).stock_quantity_check() == None:
                        print(stock[2]+'에 매도에 매칭되는 매수정보가 없습니니다.1')
                        stock = pd.Series([stock[0],stock[1],stock[2],stock[3],stock[4],stock[5]], index=['거래일자', '거래종류','종목명','수량','거래금액','통화'])
                        need_info_stock = need_info_stock.append(stock, ignore_index = True)
                        flag = False
                        continue
                except:
                    print(stock[2]+'에 매도에 매칭되는 매수정보가 없습니니다.1')
                    stock = pd.Series([stock[0],stock[1],stock[2],stock[3],stock[4],stock[5]], index=['거래일자', '거래종류','종목명','수량','거래금액','통화'])
                    need_info_stock = need_info_stock.append(stock, ignore_index = True)
                    flag = False
                    continue
                else:
                    if int(stock[3]) == 0:
                        break
                    #판매수량이 Node,quantity보다 많은 경우
                    elif stock[3] >= stock_queue.get(stock[2]).stock_quantity_check():
                        while True:
                            if stock[3] == 0:
                                break
                            elif stock[3] < int(stock_queue.get(stock[2]).stock_quantity_check()):
                                break
                            temp_Node = stock_queue.get(stock[2]).dequeue()
                            if temp_Node == None:
                                print(stock[2]+'에 매도에 매칭되는 매수정보가 없습니니다.1')
                                stock = pd.Series([stock[0],stock[1],stock[2],stock[3],stock[4],stock[5]], index=['거래일자', '거래종류','종목명','수량','거래금액','통화'])
                                need_info_stock = need_info_stock.append(stock, ignore_index = True)
                                flag = False
                                break
                            else:
                                holding_period = date_difference(stock[0],temp_Node.date_acquired)
                                temp_sold_stock_procced = stock[4]*(temp_Node.quantity/stock[3])
                                stock[4] = stock[4]-temp_sold_stock_procced
                                stock_name = str(temp_Node.quantity) + ' sh. ' + str(temp_Node.en_name)
                                sold_stock = pd.Series([stock_name,holding_period,temp_Node.date_acquired,stock[0], temp_sold_stock_procced, temp_Node.cost, temp_sold_stock_procced - temp_Node.cost, None, stock[5]], index = ['종목명','보유기간','매수일','매도일','매도가격','매수가격','양도차익','양도소득세','통화'])
                                sold_stock = pd.Series([stock_name,holding_period,temp_Node.date_acquired,stock[0], temp_sold_stock_procced, temp_Node.cost, temp_sold_stock_procced - temp_Node.cost, None, stock[5]], index = ['종목명','보유기간','매수일','매도일','매도가격','매수가격','양도차익','양도소득세','통화'])
                                stock[3] -= temp_Node.quantity            # stock = ['거래일자', '거래종류','종목명','수량','총거래금액','통화']                                                                                                                                                                          
                                result_stock = result_stock.append(sold_stock, ignore_index = True)

                    #판매수량이 Node.quantity보다 적은 경우
                    elif stock_queue.get(stock[2]).stock_quantity_check() > stock[3]:
                        temp_Node = stock_queue.get(stock[2]).dequeue()
                        if temp_Node == None:
                            print(stock[2]+'에 매도에 매칭되는 매수정보가 없습니니다.2')
                            stock = pd.Series([stock[0],stock[1],stock[2],stock[3],stock[4],stock[5]], index=['거래일자', '거래종류','종목명','수량','거래금액','통화'])
                            need_info_stock = need_info_stock.append(stock, ignore_index = True)
                            flag = False
                            break
                        else:
                            temp_quantity = temp_Node.quantity
                            temp_cost = float(temp_Node.cost *(stock[3]/temp_Node.quantity))
                            temp_Node.cost = float(temp_Node.cost *(1 - stock[3]/temp_Node.quantity))
                            temp_Node.quantity = temp_Node.quantity - stock[3]
                            stock_queue.get(stock[2]).insert_front(temp_Node)

                            holding_period = date_difference(stock[0],temp_Node.date_acquired)
                            stock_name = str(stock[3]) + ' sh. ' + str(temp_Node.en_name)
                            sold_stock = pd.Series([stock_name, holding_period, temp_Node.date_acquired, stock[0], stock[4], temp_cost, stock[4]-temp_cost, None, stock[5]], index = ['종목명','보유기간','매수일','매도일','매도가격','매수가격','양도차익','양도소득세','통화'])
                            stock[3] = 0
                            result_stock = result_stock.append(sold_stock, ignore_index = True)
        else:
            continue
    result_stock = result_stock[['종목명','보유기간','매수일','매도일','매도가격','매수가격','양도차익','양도소득세','통화']]
    result_stock.to_excel('선입선출로 정리된 주식.xlsx')
    need_info_stock.to_excel('매수정보가 부족한 주식.xlsx')


    #해당 주식 판매
    #dequeue 맨앞의 데이터를 peek을 통해서 수량 확인
    #만약 판매수량이 head.Node보다 많다면, 하나 빼내고 현재 판매 할때의 날짜와 환율를 계산한 매매가에서 매수가를 뺀다. 양도차익은 해당 큐에 저장시킨다 ????
    #남은 판매 수량은 위와 아래의 작업을 반복(while문이 좋을 거 같다....)
    #만약 판매수량이 head.Node보다 적다면, 하나를 빼내서 Node의 수량을 판매수량 만큼 뺀 뒤, insert_front를 통해 다시 삽입, 양도차익은 해당 큐에 저장시킨다 ????

