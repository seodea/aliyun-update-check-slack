# Alibaba Cloud Update Code

This code send a Alibaba Cloud Update list to Slack channel. If you set up the code in scheduler, It's automatically send it. This code only run the window server. Because We have to use the chrome for mining the website.


## Prerequisites
- Windows Server or client

- Application
	1. Python 3.7.x
	2. chromedriver

- package
	1. Beautifulesoup4
	2. Selenium
	3. slacker

- Save list encoding
	1. csv file and encoding **ANSI**

## Download Python 3.7.x

The Python 3.7.x version can download. please using the this [download URL](https://www.python.org/downloads/)

## Download Chromedrive.exe

The Chromedrive.exe can download from URL. Please download the correct version that you installed chrome version. [download URL](https://chromedriver.chromium.org/downloads)

## Install Packages

    pip3 install beautifulsoup4
	pip3 install --upgrade bs4 	*(update bs4 after install)*
    pip3 install selenium
    pip3 install slacker

## Create csv file

This script use the **update-list.csv** for csv file name or download the csv file in my repository.

## Edit code line

You have to edit the code line.

### First Change the Slack channel token
you have to change the third code line. If you don't change it, You can't receive a notification in slack.

1.  Create the ***slack app***
2. Copy the ***token***
3. Add the ***App in your notification channel***

I attached the [Refer URL](https://jisun-rea.tistory.com/entry/Slack-API-Slack-Bot-%EB%A7%8C%EB%93%A4%EA%B3%A0-Slack-%EB%A9%94%EC%84%B8%EC%A7%80-%EB%B3%B4%EB%82%B4%EA%B8%B0-Scopes-slacker) for setting **slack app(bot)**.

After, Changing the Code line 

	# Posting to a Slack channel
	def send_message_to_slack(attachments):
	token = "YOUR SLACK CHANNEL TOKEN"
	slack = Slacker(token)
	slack.chat.post_message(channel="#YOUR SLACK CHANEL", text=None, attachments=attachments)


For example :

    token = 'xoxp-710146843840-755212373527-71352123258-0exxxxxxxxx'
    slack = Slacker(token)
    slack.chat.post_message(channel="#ali_update", text=None, attachments=attachments)

## How to use the code line

 1. Import the module


	    from bs4 import BeautifulSoup
	    from selenium import webdriver
	    import csv
	    import os
	    from time import sleep
	    from slacker import Slacker



2. Read, write csv Function

	This Function is Read, write CSV file. 

		# Read csvfile into dictionary
		def ReadCSVasDict(csv_file):
			 log=[]
	
			# It's working. csv fie incode is ANSI.
	
			with open(csv_file, newline='',encoding='UTF-8-sig') as csvfile:
				reader = csv.DictReader(csvfile)
				for row in reader:
					log.append(dict(row))
			return log

		def WriteDictToCSV(csv_file,csv_columns,dict_data):
			
			# It's working. csv fie incode is ANSI.
			
			with open(csv_file, 'w', newline='',encoding='UTF-8') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
				writer.writeheader()
				for data in log:
					writer.writerow(data)
			return
3. Send slack function

	This code will be used the **Edit Code Line**

		# Posting to a Slack channel
	    def send_message_to_slack(attachments):
		    token = 'YOUR SLACK CHANNEL TOKEN'
		    slack = Slacker(token)
		    slack.chat.post_message(channel="#YOUR SLACK CHANEL", text=None, attachments=attachments)

4. Running code

	First Running the Chromedriver  and mining start.


	    driver = webdriver.Chrome('./chromedriver.exe')
	    sleep(1)
	    
	    driver.get("https://www.alibabacloud.com/news/product")
	    sleep(1)
	    
	    html = driver.page_source
	    sleep(1)
	    
	    soup = BeautifulSoup(html, "html.parser")
	    sleep(1)


5. searching the update list
	
	This line is searching the update list in mining json file.
	

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

6. Compare update lists from CSV with mining update lists
	
	This line is compare update lists from csv with mining update lists.
	
	    ###### Check ######
    
    	count = []
      	basic_count = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    	for i in range(0,len(title)):
		    for line in log:
			    if (title[i].text.split('/n'))[0][:-2] in line['title']:
				    if i in count:
					    'ok'
				    elif i not in count:
					    count.append(i)
    
		    	else :
		    	   	True
    
    	new_list = list(set(basic_count).difference(count))
    
 
 7. Update the new update list

	If there is new update list, this line will be update it.

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
    
 8. Sending the massage and write the update lists in csv file

	  This line is send the update list massages to slack channel.
	
	 
    	# Sending the massage to Slack
       	attachments_dict = dict()
       	attachments_dict['pretext'] = ("Product Update : {0}".format(Ali_label))
       	attachments_dict['title'] = ("Product 항목 : {0}".format(Ali_title))
       	attachments_dict['title_link'] = "https://www.alibabacloud.com/news/product"
     	attachments_dict['fallback'] = ("Product Update : {0}, 업데이트 설명 : {1}".format(Ali_title,Ali_des))
     	attachments_dict['text'] = ("자세한 내용 : {0},적용 날짜 : {1}".format(Ali_detail, Ali_date))
     	attachments_dict['mrkdwn_in'] = ["text", "pretext"] # 마크다운을 적용시킬 인자들을 선택합니다.
       	attachments = [attachments_dict]
    
    	send_message_to_slack(attachments)
    
    	# write csv log
    
    	csv_columns = ['title','label','description','detail','date']
    
       	print('writting csv file')
       	WriteDictToCSV(csv_file,csv_columns,dict_data)

9. Kill all of program

	This line will be kill the program(chrome and driver) themselves.

	    # kill Web browser
	    browserExe = "chrome.exe"
	    os.system("taskkill /f /im "+browserExe)
	    browserdriver = "chromedriver.exe"
	    os.system("taskkill /f /im "+browserdriver)

# Finally

If you did it well, You can receive the slack massage such as below picture.
Also you can refer the detail update content to click blue content.

<img width="657" alt="slack_update" src="https://user-images.githubusercontent.com/46041493/96417032-c69cf180-122b-11eb-8736-4d22d299c87a.png">
