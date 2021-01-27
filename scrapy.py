import csv
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
def getdata(link, s):
    data = requests.get(link).text
    soup = BeautifulSoup(data, 'lxml')
    data = []
    try:
        name = soup.find(class_='h2').text.strip()
    except:
        
        driver.get(link)

        time.sleep(2)
        if soup.text.strip().startswith('Just'):
            time.sleep(15)
        # driver.navigate.refresh()
        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        if not soup.text.strip().startswith('TruePeopleSearch.com'):
            input('Skip the captcha, then press enter:')
            page = driver.page_source
            soup = BeautifulSoup(page, 'lxml')
        #driver.close()
        try:
            name = soup.find(class_='h2').text.strip()
        except:
            driver.get(link)
            time.sleep(5)
            if soup.text.strip().startswith('Just'):
                time.sleep(15)
            page = driver.page_source
            soup = BeautifulSoup(page, 'lxml')
            if not soup.text.strip().startswith('TruePeopleSearch.com'):
                input('Skip the captcha, then press enter:')
                page = driver.page_source
                soup = BeautifulSoup(page, 'lxml')
            #driver.close()
            name = soup.find(class_='h2').text.strip()

    name_age = soup.find(class_='row pl-md-2').text.split('\n')
    while '' in name_age:
        name_age.remove('')

    name, age = name_age
    name = name.strip()
    age = age.strip()
    data.append(name)

    address = soup.find(class_='col-12 col-sm-11').text.split('\n')
    while '' in address:
        address.remove('')
    while 'Map' in address:
        address.remove('Map')
    if 'Current Address' in address:
        address.remove('Current Address')

    # data.append(' '.join(address))

    phone = []
    for link in soup.find_all('a', href=True):
        if link['href'].startswith('/resultphone?phoneno'):
            phone.append(link['href'][21:])
    if len(phone) > s:
        phone = phone[:s]
    for each in phone:
        data.append(each)

    for i in range(s + 1 - len(data)):
        data.append('')

    data.append(age)
    data.append(''.join(address))

    return data


count = 1
with open('test.csv', 'r') as f:
    with open('output_test1.csv', 'w',newline='') as w:
        writer = csv.writer(w)
        reader = csv.reader(f)
        for line in reader:
            # print(line)
            name, link1, link2 = line
            data1 = getdata(link1, 3)
            if link2:
                data = []
                data2 = getdata(link2, 2)

                try:
                    data.append(data1[0] + ' - ' + data2[0])
                except:
                    pass

                try:
                    for i in data1[1:4]:
                        data.append(i)
                    for i in data2[1:3]:
                        data.append(i)
                except:
                    pass

                try:
                    data.append(data1[-2] + ' - ' + data2[-2])
                except:
                    pass

                try:
                    data.append(data1[-1] + ' - ' + data2[-1])
                except:
                    pass

            else:
                data = data1
                data.insert(4, '')
                data.insert(5, '')
            print(data)
            if data:
                writer.writerow(data)
                # print(count)
                print(f'\nWRITTEN: {count}\n')
            time.sleep(5)
            count += 1
