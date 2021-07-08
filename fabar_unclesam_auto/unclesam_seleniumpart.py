import selenium
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


# time.sleep(1)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome('./driver/chromedriver.exe',chrome_options=options)
url = 'https://us114.net/index.html'
driver.get(url)
driver.implicitly_wait(time_to_wait=3)

wait = WebDriverWait(driver,30)
def isNaN(num):
    return num == num

def login(login_id,login_pwd):

    # driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div[3]/div/ul/li[1]/a").click()
    driver.find_element_by_link_text("로그인").click()
    
    try:
        driver.find_element_by_name("user_id").send_keys(login_id)
        driver.find_element_by_name("user_passwd").send_keys(login_pwd)
        driver.find_element_by_name("submit_OK").click()
    except:
        print("아이디 또는 비밀번호가 잘못 되었습니다.")
    driver.get(url)

    #팝업창 끄기
    try:
        # driver.find_element_by_name("chepopup_33").click()
        # driver.find_element_by_partial_link_text("#;").click()
        driver.find_element_by_xpath('//*[contains(@name, "chepopup_")]').click()
    except:
        pass
    print("login")

#-----------------------------------------------------------------------------------------------------------------------------
def seleni_insert(personal_info, year,num_account, signal_flag):
# personal_info = [[First_name, Last_name, Middle_name, Suffix,], birth_day, ssn, country, address]

    First_name = personal_info[0][0]
    Middle_name = personal_info[0][2]
    Last_name = personal_info[0][1]
    Suffix= personal_info[0][3]
    birth_day = personal_info[1]
    ssn = str(personal_info[2])
    country = personal_info[3]
    address = personal_info[4]
    flag_value = signal_flag ####SDOP or SFOP인지 996, 997, 998###################################################################################


    button = driver.find_element_by_xpath('//*[@id="visual-contents"]/div/div[*]/div/a')
    driver.execute_script("arguments[0].click();", button)

    driver.find_element_by_class_name('btnIntroNext').click()

    #신고 유형 선택 (개인신고 or 법인신고)
    # driver.find_element_by_xpath("//*[@id='TCBOARD_fbar_WRITE_index16728']/div/div/ul/li/div/div[2]/table/tbody/tr[2]/td[1]/input").click()
    temp_button = driver.find_elements_by_css_selector("input[type='submit'][name='submit_OK']")
    temp_button[0].click()
    select = Select(driver.find_element_by_name('a_nonage_child'))
    select.select_by_value(value="N")
    select = Select(driver.find_element_by_name('a_tax_year_year'))
    select.select_by_value(value=str(year))

    if year == 2020:
        driver.find_element_by_css_selector("input[type='radio'][value='C']").click()
        button = driver.find_element_by_name('submit_OK')
        driver.execute_script("arguments[0].click();", button)
    else:
        driver.find_element_by_css_selector("input[type='radio'][value='B']").click()
        button = driver.find_element_by_name('submit_OK')
        driver.execute_script("arguments[0].click();", button)
        select = Select(driver.find_element_by_name("a_late_reason"))
        select.select_by_value(value = str(flag_value))

        time.sleep(1)
        button = driver.find_element_by_name('submit_OK')
        driver.execute_script("arguments[0].click();", button)
        temp_button = driver.find_elements_by_class_name('btnIntroNext')
        temp_button[1].click()
    #다음 중 신고대상자에 해당되는 상황을 모두 선택하세요 설문지
    # driver.find_element_by_xpath("//*[@id='a_account_own_type_2']").click()
    driver.find_element_by_css_selector("input[type='checkbox'][value='C']").click()
    button = driver.find_element_by_name('submit_OK')
    driver.execute_script("arguments[0].click();", button)

    #다음 중 해당되는 상황을 모두 선택하세요 설문지
    if num_account >= 25:
        # driver.find_element_by_xpath("//*[@id='a_account_separately_0']").click()
        driver.find_element_by_xpath("//*[@id='a_account_separately_2']").click()
    else:
        driver.find_element_by_xpath("//*[@id='a_account_separately_2']").click()
    
    time.sleep(1) #너무 빠르게 클릭되어 오류 날 수 있음.

    button = driver.find_element_by_name('submit_OK')
    driver.execute_script("arguments[0].click();", button)

    temp_button = driver.find_elements_by_class_name('btnIntroNext')
    temp_button[1].click()
#-----------------------------personal info insert--------------------------------------

    driver.find_element_by_name("a_first_name").send_keys(First_name)
    if Middle_name:
        driver.find_element_by_name("a_middle_name").send_keys(Middle_name)
    if Suffix:
        driver.find_element_by_name("a_suffix").send_keys(Suffix)
    driver.find_element_by_name("a_last_name").send_keys(Last_name)

    select = Select(driver.find_element_by_name("a_birthday_year"))
    select.select_by_value(value=birth_day[0])
    select = Select(driver.find_element_by_name("a_birthday_month"))
    select.select_by_value(value=birth_day[1])
    select = Select(driver.find_element_by_name("a_birthday_day"))
    select.select_by_value(value=birth_day[2])

    driver.find_element_by_name("a_id_number_us").send_keys(ssn)
    driver.find_element_by_name("a_id_number_us_re").send_keys(ssn)

#주소찾기--------------------------------------------------------------------------------------------------------------- 

    if country == 'Korea':
        driver.find_element_by_id("a_address_type_0").click()
        driver.find_element_by_name("user").click()
        
        wait.until(expected_conditions.frame_to_be_available_and_switch_to_it((driver.find_element_by_xpath("//*[@id='__daum__layer_1']/iframe"))))
        wait.until(expected_conditions.frame_to_be_available_and_switch_to_it((driver.find_element_by_xpath("//*[@id='__daum__viewerFrame_1']"))))
        
        time.sleep(1)
        driver.find_element_by_id("region_name").send_keys(address[0])
        driver.find_element_by_class_name("btn_search").click()
        driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul/li[1]/dl/dd[2]/span/button/span[2]").click()

        driver.switch_to.default_content()
        # driver.find_element_by_id("btnCloseLayer").click()
        driver.find_element_by_id("a_address_etc").send_keys(address[1])
        time.sleep(1)

    else:
        driver.find_element_by_id("a_address_type_1").click()
        driver.find_element_by_id("a_address").send_keys(address[0]) #도로주소
        # driver.find_element_by_name("a_address_etc").send_keys(address[3]) #동/호수

        driver.find_element_by_id("a_city").send_keys(address[1]) #도시
        select = Select(driver.find_element_by_id("a_state"))
        try:
            select.select_by_visible_text(address[2].title()) #주
        except:
            select.select_by_value(address[2].upper()) # 주의 대문자만 적었을 경우 ex) New York = NY
        select = Select(driver.find_element_by_id("a_country"))
        select.select_by_visible_text(country) #나라
        driver.find_element_by_id("a_postcode").send_keys(address[3]) #우편번호

        
############################### 미국 주소 와 다른 나라 주소 구분해야함

    # button = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div/div/div/form/div/div[3]/div/input[1]')
    # driver.execute_script("arguments[0].click();", button)
    button = driver.find_element_by_name('submit_OK')
    driver.execute_script("arguments[0].click();", button)
    # driver.find_element_by_name("submit_OK").click()
    # driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div/div/form/div/div[5]/a[2]/span").click()
    # button = driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div/div/form/div/div[5]/a[2]/span")
    # driver.execute_script("arguments[0].click();", button)
    button = driver.find_elements_by_class_name('btnIntroNext')
    driver.execute_script("arguments[0].click();", button[1])
    # temp_button[1].click()

#계좌입력------------------------------------------------------------------------------------------------------------------
def seleni_insert_account(merged_data, year,i,col):
    # personal_info = [[First_name, Middle_name, Suffix, Last_name], birth_day, ssn, country, address]

    typeOfaccount = merged_data.iloc[i][0]
    account_num = str(merged_data.iloc[i][12])
    account_num = str(account_num.replace('-','')).strip()
    account_num = str((account_num))
    currency = merged_data.iloc[i][13]
    institution_flag = False
    if isNaN(merged_data.iloc[i][6]):
        institution_flag = True
    institution_name = merged_data.iloc[i][1]
    if merged_data.iloc[i][col] == '-':
        merged_data.iat[i][col] = 0
    else:
        print('--------------------------------')
        print(merged_data.iloc[i][col])
        print(type(merged_data.iloc[i][col]))
        print('--------------------------------')
        account_value=str(round(int(float(merged_data.iloc[i][col]))))
    time.sleep(1)
    # button = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/div/div/div/form/div/div[2]/div[2]/a/span")
    # driver.execute_script("arguments[0].click();", button)
    button = driver.find_element_by_class_name("AB_btn_dialog_write")
    driver.execute_script("arguments[0].click();", button)
    
#계좌입력 창
# wait.until(expected_conditions.frame_to_be_available_and_switch_to_it((driver.find_element_by_xpath("/html/body/iframe"))))
    wait.until(expected_conditions.frame_to_be_available_and_switch_to_it((driver.find_element_by_id("global_dialog_ifrm"))))
    time.sleep(1)

    # select = Select(driver.find_element_by_xpath("/html/body/div/div/form/div/div[2]/div[1]/div[2]/table/tbody/tr[1]/td/select"))
    select = Select(driver.find_element_by_name("account_type"))
    if typeOfaccount == 'Bank':
        select.select_by_value(value = "1")
    elif typeOfaccount == 'Securities':
        select.select_by_value(value = "2")
    else:
        select.select_by_value(value = "999")
        select = Select(driver.find_element_by_name("other_account"))
        if typeOfaccount == 'Insurance':
            select.select_by_value(value = "Insurance")
        elif typeOfaccount == 'Pension':
            select.select_by_value(value = "Pension")
        else:
            select.select_by_value(value = "ETC")
            driver.find_element_by_name("other_account_input").send_keys(str(typeOfaccount))

    if institution_flag:
        driver.find_element_by_xpath("/html/body/div/div/form/div/div[2]/div[1]/div[2]/table/tbody/tr[2]/td/div[1]/input[2]").click()
    else:
        select = Select(driver.find_element_by_name("relation_serial_2"))
        select.select_by_visible_text(institution_name)

    driver.find_element_by_name("account_num").send_keys(account_num)

    select = Select(driver.find_element_by_name("currency_in"))
    select.select_by_value(value = currency)

    driver.find_element_by_name("max_value").send_keys(account_value)

    if currency != 'USD':
        driver.find_element_by_xpath("/html/body/div/div/form/div/div[2]/div[1]/div[2]/table/tbody/tr[7]/td/span").click()
    # driver.find_element_by_name("submit_OK").click()
    # button = driver.find_element_by_xpath('/html/body/div/div/form/div/div[2]/div[2]/div/input[1]')
    button = driver.find_element_by_css_selector("input[type='submit'][name='submit_OK']")
    
    driver.execute_script("arguments[0].click();", button)

#HOME으로 돌아가기
def escape():
    # driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/ul/li[1]/a").click()
    driver.find_element_by_link_text("HOME").click()

def finish():
    driver.quit()
    