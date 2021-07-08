import pandas as pd
from pandas import DataFrame,Series
# import numpy as np
# import xlrd
# import openpyxl
import csv
import unclesam_seleniumpart
from unclesam_seleniumpart import *
import os



def isNaN(num):
    return num == num

class data_process:

    def __init__(self,login_id,login_pwd,file_name,signal_flag):
        self.login_id = str(login_id)
        self.login_pwd = str(login_pwd)
        self.file_name = str(file_name)
        self.signal_flag = signal_flag





    def work(self):
        path = os.getcwd()+'\\'
        try:
            client_data = pd.read_excel(path + self.file_name, usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29], header = 6, sheet_name = 'C. 금융계좌 및 투자소득_주신고인', thousands = ',')
            #2,3,4 = [], 27,28,29
            client_data = client_data[['금융기관', '계좌번호', '계좌통화', '계좌 개설연도', '계좌 해지연도','2014 계좌잔액', '2014 계좌연중최고잔액', '2015 계좌잔액',
                '2015 계좌연중최고잔액', '2016 계좌잔액', '2016 계좌연중최고잔액', '2017 계좌잔액',
                '2017 계좌연중최고잔액', '2018 계좌잔액', '2018 계좌연중최고잔액', '2019 계좌잔액',
                '2019 계좌연중최고잔액', '2020 계좌잔액', '2020 계좌연중최고잔액', '소득발생여부', '이자/배당소득',
                '이자배당소득 \n원천징수 세액', '이자/배당소득.1', '이자배당소득 \n원천징수 세액.1', '이자/배당소득.2',
                '이자배당소득 \n원천징수 세액.2', '이자/배당소득.3', '이자배당소득 \n원천징수 세액.3', '계좌종류', '위탁계좌여부']]
            client_data = client_data.dropna(subset = ['계좌번호','금융기관'])
            client_data_info = pd.read_excel(path + self.file_name, sheet_name = 'A. 고객기본정보')
            client_data_info = pd.DataFrame(client_data_info)
            with open('reference_file\엉클샘_금융기관정보_3.csv','r', encoding = 'utf-8') as f:
                file_data = csv.reader(f)
                file_data = list(file_data)
        except FileNotFoundError: #해당파일이 존재하지 않을때
            print('해당 파일를 찾을 수 없습니다.')
            
        #---------------------------------개인정보 입력---------------------------------------------
        
        customer_name = client_data_info.iloc[8][7]
        customer_name_list = customer_name.split('-')


        First_name = customer_name_list[0]
        Last_name = customer_name_list[1]
        Middle_name = None
        Suffix = None
        if len(customer_name_list) >= 3:
            Middle_name = customer_name_list[2]
            if len(customer_name_list) >= 4:
                Suffix = customer_name_list[3]
        birth_day = str(client_data_info.iloc[10][7]).split(' ')[0].split('-')
        ssn = str(client_data_info.iloc[13][7]).replace('-','').strip()
        country = None
        address = None

        if isNaN(client_data_info.iloc[17][7]):
            country = 'Korea'
            address = str(client_data_info.iloc[17][7])
            address = address.split("/")
        else:
            country = 'United States of America'
            address = str(client_data_info.iloc[18][7])
            address = address.split("/")

        personal_info = [[First_name, Last_name, Middle_name, Suffix], birth_day, ssn, country, address]



        #------------------------------------------------------------------------------------------------------

        # alist = []
        # for i in client_data['계좌번호']:
        #     try:
        #         i = str(i).replace('-','').strip()
        #         if i.isdigit():
        #             alist.append(i)
        #         else:
        #             alist.append(i)
        #     except AttributeError: #직접입력 계좌번호가 string타입이 아닌 정수일 경우
        #         alist.append(i)
        
        # # print(alist)

        # # #워크북 자료 다듬기
        # client_data.loc[:,'계좌번호'] = alist
        # client_data = client_data.dropna(subset = ['계좌번호','금융기관'])
        client_data = client_data.replace('클릭하여 선택', '')

        client_data['계좌종류'] = client_data['계좌종류'].str.replace('(','/')
        client_data['계좌종류'] = client_data['계좌종류'].str.replace(')','')
        client_data['계좌종류'] = client_data['계좌종류'].str.replace(' ','')

        client_data[['계좌종류_1','계좌종류_2']] = client_data['계좌종류'].str.split('/', n = 1, expand = True)
        client_data = client_data.drop(['계좌종류', '계좌종류_1'], axis = 1)
        client_data = client_data.rename({'계좌종류_2' : '계좌종류'}, axis =1)

        #금융기관정보(영문) 필요정보만 뽑는 과정
        reference_data = pd.DataFrame(file_data, columns = ['계좌종류',	'금융기관', '금융기관명(영문)','도로주소', '도시','국가'])
        reference_data.drop(0, axis = 0 , inplace = True)
        reference_data = reference_data.drop(1, axis = 0)
        reference_data['계좌종류'] = reference_data['계좌종류'].str.replace('/',',')
        reference_data['계좌종류'] = reference_data['계좌종류'].str.replace('(','/')
        reference_data['계좌종류'] = reference_data['계좌종류'].str.replace(')','')
        reference_data['계좌종류'] = reference_data['계좌종류'].str.replace(' ','')

        reference_data.reindex()
        reference_data[['계좌종류_1','계좌종류_2']] = reference_data['계좌종류'].str.split('/', n = 1, expand = True)
        reference_data = reference_data.drop(['계좌종류', '계좌종류_1'], axis = 1)
        reference_data = reference_data.rename({'계좌종류_2' : '계좌종류_2'}, axis =1)

        #직접 입력한 계좌 부분 추출
        direct_insert_bank_name = []
        flag = False
        for bank_name_index in range(len(client_data.index)):
            for bank_name_info_index in range(len(reference_data.index)):
                if client_data.iloc[bank_name_index][0] == reference_data.iloc[bank_name_info_index][0]:
                    flag = True
                    break
            if flag == False:
                direct_insert_bank_name.append(bank_name_index)
            else:
                flag = False


        if len(direct_insert_bank_name) != 0:
            direct_insert_client_data = client_data.iloc[direct_insert_bank_name]
            client_data.drop(client_data.index[direct_insert_bank_name])
            direct_insert_client_data = direct_insert_client_data.rename({'금융기관' : '금융기관명(직접입력)'}, axis = 1)
            direct_insert_client_data['도로주소(직접입력)'] = None
            direct_insert_client_data['도시(직접입력)'] = None
            direct_insert_client_data['주(직접입력)'] = None
            direct_insert_client_data['국가(직접입력)'] = None
            direct_insert_client_data['우편번호(직접입력)'] = None
        else:
            direct_insert_client_data = pd.DataFrame()
            direct_insert_client_data['금융기관명(직접입력)'] = None
            direct_insert_client_data['도로주소(직접입력)'] = None
            direct_insert_client_data['도시(직접입력)'] = None
            direct_insert_client_data['주(직접입력)'] = None
            direct_insert_client_data['국가(직접입력)'] = None
            direct_insert_client_data['우편번호(직접입력)'] = None

        merge_data = pd.merge(client_data, reference_data, on='금융기관')
        
        # merge_data.to_excel('test_9.xlsx')

        num = []
        for i in range(len(merge_data.index)):
            if merge_data.iloc[i][29] not in merge_data.iloc[i][34]:
                num.append(i)

        #금융기관정보와 워크북 매칭
        merge_data = merge_data.drop(merge_data.index[num])
        merge_data = merge_data.drop(['계좌종류_2'], axis = 1)
        merge_data = merge_data.drop_duplicates(['금융기관','계좌번호'], keep = 'first', ignore_index= True)
        merge_data.to_excel('data_confirm.xlsx')

        #직접입력한 계좌 합병
        if len(direct_insert_bank_name) != 0:
            merged_data = pd.merge(merge_data, direct_insert_client_data, how = 'outer')
        else:
            merged_data = pd.concat([merge_data, direct_insert_client_data])

        merged_data = merged_data[['계좌종류','금융기관','금융기관명(영문)','도로주소','도시','국가','금융기관명(직접입력)','도로주소(직접입력)','도시(직접입력)','주(직접입력)','국가(직접입력)','우편번호(직접입력)','계좌번호','계좌통화','위탁계좌여부','소득발생여부','이자/배당소득','2014 계좌잔액',
       '2014 계좌연중최고잔액', '2015 계좌잔액', '2015 계좌연중최고잔액', '2016 계좌잔액',
       '2016 계좌연중최고잔액', '2017 계좌잔액', '2017 계좌연중최고잔액', '2018 계좌잔액',
       '2018 계좌연중최고잔액', '2019 계좌잔액', '2019 계좌연중최고잔액', '2020 계좌잔액',
       '2020 계좌연중최고잔액','계좌 개설연도','계좌 해지연도']]


        #연도별로 계좌 등록하기
        num_account = len(merged_data.index)
        data_count = merged_data.count()

        login(self.login_id,self.login_pwd)
        for col in range(18,32,2):
            if col == 18:
                year = 2014
                if data_count[str(year) + ' 계좌연중최고잔액'] != 0:
                    seleni_insert(personal_info,year,num_account,self.signal_flag)
                    for i in range(num_account):
                        if isNaN(merged_data.iloc[i][col]):
                            seleni_insert_account(merged_data,year,i,col)
                        else:
                            continue
                    escape()
            elif col == 20:
                year = 2015
                if data_count[str(year) + ' 계좌연중최고잔액'] != 0:
                    seleni_insert(personal_info,year,num_account,self.signal_flag)
                    for i in range(num_account):
                        if isNaN(merged_data.iloc[i][col]):
                            seleni_insert_account(merged_data,year,i,col)
                        else:
                            continue
                    escape()
            elif col == 22:
                year = 2016
                if data_count[str(year) + ' 계좌연중최고잔액'] != 0:
                    seleni_insert(personal_info,year,num_account,self.signal_flag)
                    for i in range(num_account):
                        if isNaN(merged_data.iloc[i][col]):
                            seleni_insert_account(merged_data,year,i,col)
                        else:
                            continue
                    escape()
            elif col == 24:
                year = 2017
                if data_count[str(year) + ' 계좌연중최고잔액'] != 0:
                    seleni_insert(personal_info,year,num_account,self.signal_flag)
                    for i in range(num_account):
                        if isNaN(merged_data.iloc[i][col]):
                            seleni_insert_account(merged_data,year,i,col)
                        else:
                            continue
                    escape()
            elif col == 26:
                year = 2018
                if data_count[str(year) + ' 계좌연중최고잔액'] != 0:
                    seleni_insert(personal_info,year,num_account,self.signal_flag)
                    for i in range(num_account):
                        if isNaN(merged_data.iloc[i][col]):
                            seleni_insert_account(merged_data,year,i,col)
                        else:
                            continue
                    escape()
            elif col == 28:
                year = 2019
                if data_count[str(year) + ' 계좌연중최고잔액'] != 0:
                    seleni_insert(personal_info,year,num_account,self.signal_flag)
                    for i in range(num_account):
                        if isNaN(merged_data.iloc[i][col]):
                            seleni_insert_account(merged_data,year,i,col)
                        else:
                            continue
                    escape()
            elif col == 30:
                year = 2020
                if data_count[str(year) + ' 계좌연중최고잔액'] != 0:
                    seleni_insert(personal_info,year,num_account,self.signal_flag)
                    for i in range(num_account):
                        if isNaN(merged_data.iloc[i][col]):
                            seleni_insert_account(merged_data,year,i,col)
                        else:
                            continue
                    escape()
        finish()
        print("모든 작업이 끝났습니다.")

    #한국의 경우
    #address 입력 순서 : 도로주소-동/호수-시/군 (호수에 한글이 입력되어 있으면 안된다.)
    #미국의 경우
    #address 입력 순서 : 도로주소-도시-주(state)-우편번호 (호수에 한글이 입력되어 있으면 안된다.)
    #birthday 입력 순서 : 1993-04-26
    #name 입력 순서 : Firstname_Lastname_Middlename_Suffix

    #금융기관 직접 입력의 경우, 금융기관의 주소를 입력받아야 함