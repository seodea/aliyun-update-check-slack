# pip3 install beautifulsoup4
# pip install --upgrade bs4
# pip3 install selenium
# pip install slacker


from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import os
from time import sleep
from slacker import Slacker

########

# Read csvfile into dictionary

def ReadCSVasDict(csv_file):

    log=[]

    # It's working. csv fie incode is ANSI.
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            log.append(dict(row))

    return log

def WriteDictToCSV(csv_file,csv_columns,dict_data):

    # It's working. csv fie incode is ANSI.
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in log:
            writer.writerow(data)

    return


# Posting to a Slack channel
def send_message_to_slack(attachments):

    token = 'YOUR SLACK CHANNEL TOKEN'
    slack = Slacker(token)
    slack.chat.post_message(channel="#YOUR SLACK CHANEL", text=None, attachments=attachments)


########


# 1. chrome이나 firefox가 설치가 되어있어야한다.
# 2. chromedriver나 geckodriver의 파일이 python과 같은 위치에 있거나, 혹은 OS의 PATH에 등록되어 쉘에서 실행 가능한 경로여야한다.
#    혹은 driver = webdriver.Chrome('/path/to/chromedriver')의 절대경로로 해도 된다.

driver = webdriver.Chrome('./chromedriver.exe')
sleep(1)
driver.get("https://www.alibabacloud.com/news/product")
sleep(1)
html = driver.page_source

sleep(1)

soup = BeautifulSoup(html, "html.parser")
sleep(1)

#############################
### finding sub...in soup ###
#############################

# 제목
title = soup.find_all("span",{"class": "title-inner"})

#description
des = soup.find_all("div",{"class":"description"})

# 디테일한 내용
detail_info = soup.find_all('div',{"class": "release-item-detail"})

# 날짜
day = soup.find_all('div',{"class": "date-wrap"})

# label
label = soup.find_all('span',{"class": "label-style"})



###################
### Reading CSV ###
###################

# Read CSV

csv_file = './update-list.csv'

log = ReadCSVasDict(csv_file)


###### Check ######
count = []
basic_count = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

for i in range(0,len(title)):
    #print(i)
    for line in log:
        
        if (title[i].text.split('/n'))[0][:-2] in line['title']:

            if i in count:
                'ok'
            elif i not in count:
                count.append(i)
            
        else :
            True

new_list = list(set(basic_count).difference(count))

##### Loging and messaging #####
# 2020.04.28 change the if sentence == 0 to != []

if new_list != [] : 
    for i in new_list:

        # title
        ii = title[i].text.split('/n')
        Ali_title = ii[0][:-2]

        # description
        ii = des[i].get_text()
        Ali_des = ii

        # detail
        ii = detail_info[i].get_text()
        Ali_detail = ii

        # date
        ii = day[i].get_text()
        Ali_date = ii

        # label
        ii = label[i].get_text()
        Ali_label = ii[:-1]

        dict_data = {
            'title': Ali_title, 'label': Ali_label, 'description': Ali_des, 'detail': Ali_detail, 'date': Ali_date
            }

        # save the values in log.
        log.append(dict_data)

        # Sending the massage to Slack
        attachments_dict = dict()
        attachments_dict['pretext'] = ("Product Update : {0}".format(Ali_label))
        attachments_dict['title'] = ("Product 항목 : {0}".format(Ali_title))
        attachments_dict['title_link'] = "https://www.alibabacloud.com/news/product"
        attachments_dict['fallback'] = ("Product Update : {0}, 업데이트 설명 : {1}".format(Ali_title,Ali_des))
        attachments_dict['text'] = ("자세한 내용 : {0},적용 날짜 : {1}".format(Ali_detail, Ali_date))
        attachments_dict['mrkdwn_in'] = ["text", "pretext"]  # 마크다운을 적용시킬 인자들을 선택합니다.
        attachments = [attachments_dict]
        
        send_message_to_slack(attachments)


        # write csv log

        csv_columns = ['title','label','description','detail','date']

        print('writting csv file')
        WriteDictToCSV(csv_file,csv_columns,dict_data)
    

# kill Web browser
browserExe = "chrome.exe"
os.system("taskkill /f /im "+browserExe)
browserdriver = "chromedriver.exe"
os.system("taskkill /f /im "+browserdriver)
