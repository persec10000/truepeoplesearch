from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import csv
import time
import sys

driver = webdriver.Chrome()


def scrape(l):
    #driver.get(l)
    time.sleep(0.5)
    driver.get(l[0:len(l)-8])
    #driver.get("https://www.truepeoplesearch.com/details?name=ALIX%20ASTER%20SAAKES")
    time.sleep(2.1)
    while 'Captcha' in driver.title:
        time.sleep(0.5)
        continue
    #print ( l[32:] )
    #print ('//div[@data-detail-link="'+l[32:]+'"]')
    
    try:
    	report2=driver.find_element_by_xpath('//div[@data-detail-link="'+l[32:]+'"]')
    	report2.click()
    	time.sleep(2.1)
    except Exception as e:
    	print ('Invalid Url')
    	pass
    finally:
    	pass
    	
    	

    
    while 'Captcha' in driver.title:
        time.sleep(0.5)
        continue

    if 'Access denied' in driver.title:
        print("Access denied, please switch VPN or try again after 30 minutes")
        sys.exit()

    name, age, address, phone_nums = ['', '', '', []]
    driver.set_page_load_timeout(5)
    try:
        element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="personDetails"]/div[1]/div/span[1]')))
        name = driver.find_element_by_xpath('//*[@id="personDetails"]/div[1]/div/span[1]').text
        age = driver.find_element_by_xpath('//*[@id="personDetails"]/div[1]/div/span[2]').text
        address = driver.find_element_by_xpath('//*[@id="personDetails"]/div[4]/div[2]/div[2]/div[1]/div/a').text.replace('\n', ', ')
        phone_span = driver.find_element_by_xpath('//*[@id="personDetails"]/div[6]/div[2]')
        phone_nums = [i.get_attribute('href')[-10:] for i in phone_span.find_elements_by_tag_name("a")]
    except:
        pass
    return [name, age, address, phone_nums]


def adjust(data, x):
    nums = data[-1] + ['', '', '', '', '']
    temp = []
    for i, num in enumerate(nums):
        if i == x:
            break
        temp.append(num)

    data[-1] = temp
    return data


reader = pd.read_csv('test.csv', names=['name', 'link1', 'link2'])
reader = reader.fillna(0)
rows = reader.shape[0]

begin = time.time()
with open('output_test1.csv', 'w') as f:
    writer = csv.writer(f)
    for index, row in reader.iterrows():
        start = time.time()
        data1 = adjust(scrape(row['link1']), 3)
        data = data1
        if row['link2']:
            data2 = adjust(scrape(row['link2']), 2)
            data = [
                ' - '.join([data1[0], data2[0]]),
                ' - '.join([data1[1], data2[1]]),
                ' - '.join([data1[2], data2[2]]),
                data1[3] + data2[3]
            ]
        data = adjust(data, 5)
        data = [data[0], *data[-1], data[1], data[2]]
        print(index + 1, data)
        writer.writerow(data)
        end = time.time()
        duration = (end - start)
        print("Estimated seconds remaining: ", int(duration * (rows - index + 1)))

driver.quit()
finish = time.time()
print(f'Total time elapsed: {(finish-begin)//60} minutes.')