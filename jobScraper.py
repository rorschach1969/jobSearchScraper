from lxml import html, etree
import requests
import re
import os
import sys
import unicodecsv as csv
import argparse
import json
from random import *
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import urllib.request

jobDescriptionURL = []
secondListURL = []
formattedURL = []
theBiggestList = []
absoluteURL = 'http://glassdoor.com'

#change the user agent so that we dont get a 403 error
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

#These are the google credentials and links for connecting to the sheets API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# #name of sheet in my google sheets
sheet = client.open('glassdoor Jobs')

urlChi = "https://www.glassdoor.com/Job/chicago-software-developer-jobs-SRCH_IL.0,7_IC1128808_KO8,26.htm"
theURLChi = "https://www.glassdoor.com/Job/chicago-software-developer-jobs-SRCH_IL.0,7_IC1128808_KO8,26_IP"
urlAustin = "https://www.glassdoor.com/Job/austin-software-developer-jobs-SRCH_IL.0,6_IC1139761_KO7,25.htm"
theUrlAustin = "https://www.glassdoor.com/Job/austin-software-developer-jobs-SRCH_IL.0,6_IC1139761_KO7,25_IP"
urlSF = "https://www.glassdoor.com/Job/san-francisco-software-developer-jobs-SRCH_IL.0,13_IC1147401_KO14,32.htm"
theURLsf = "https://www.glassdoor.com/Job/san-francisco-software-developer-jobs-SRCH_IL.0,13_IC1147401_KO14,32_IP"
urlNY = "https://www.glassdoor.com/Job/new-york-software-developer-jobs-SRCH_IL.0,8_IC1132348_KO9,27.htm"
theURLny = "https://www.glassdoor.com/Job/new-york-software-developer-jobs-SRCH_IL.0,8_IC1132348_KO9,27_IP"
urlSEA = "https://www.glassdoor.com/Job/seattle-software-developer-jobs-SRCH_IL.0,7_IC1150505_KO8,26.htm"
theURLsea = "https://www.glassdoor.com/Job/seattle-software-developer-jobs-SRCH_IL.0,7_IC1150505_KO8,26_IP"
urlLA = "https://www.glassdoor.com/Job/los-angeles-software-developer-jobs-SRCH_IL.0,11_IC1146821_KO12,30.htm"
theURLla = "https://www.glassdoor.com/Job/los-angeles-software-developer-jobs-SRCH_IL.0,11_IC1146821_KO12,30_IP"
urlDEN = "https://www.glassdoor.com/Job/denver-software-developer-jobs-SRCH_IL.0,6_IC1148170_KO7,25.htm"
theURLden = "https://www.glassdoor.com/Job/denver-software-developer-jobs-SRCH_IL.0,6_IC1148170_KO7,25_IP"
urlDetroit = "https://www.glassdoor.com/Job/detroit-software-developer-jobs-SRCH_IL.0,7_IC1134644_KO8,26.htm"
theURLdetroit = "https://www.glassdoor.com/Job/detroit-software-developer-jobs-SRCH_IL.0,7_IC1134644_KO8,26_IP"
urlDC = "https://www.glassdoor.com/Job/washington-software-developer-jobs-SRCH_IL.0,10_IC1138213_KO11,29.htm"
theURLdc = "https://www.glassdoor.com/Job/washington-software-developer-jobs-SRCH_IL.0,10_IC1138213_KO11,29_IP"


locationUrl = [theUrlAustin, theURLChi, theURLny, theURLsf, theURLsea, theURLla, theURLden, theURLdetroit,theURLdc]
urlList = [urlAustin,urlChi,urlSF,urlNY, urlSF, urlSEA, urlLA, urlDEN,urlDetroit,urlDC]



count = 2
for url in locationUrl:
	for x in range (0,20): #here brute force many pages of glassdoor using the list append function
		urlList.append((url + str(count) + '.htm')) #there should be a better way of doing this, but I don't know right now
		count +=1 #you can print out the list of urls if it looks like its not getting them properly
	count = 2
print('the number of unique urls is: ' + str(len(urlList))) #check to make sure that there is a reasonable amount of links
print (urlList)

headers = {'User-Agent':user_agent} #apply the user agent here

def masterFunction(): #make the soup creation a function so that we can use the list of URLs instead of a hard coded url
	for urlPoint in urlList:
		request = urllib.request.Request(urlPoint,None,headers)
		response = urllib.request.urlopen(request)
		data = response.read() #this is the raw html in case it's needed
		soup = BeautifulSoup(data, "lxml")
		soup.prettify()
		for soupHTML in soup.findAll('a', href = re.compile('/partner+')):
			jobDescriptionURL.append(soupHTML['href'])
			print(jobDescriptionURL)

#masterFunction()

def cleanFunction():
	for appendStep in jobDescriptionURL:
		secondListURL.append(absoluteURL + appendStep)
	for cleaned in secondListURL:
		stuff = cleaned.strip()
		formattedURL.append(stuff)
		print('\n')
		print(formattedURL)

#cleanFunction()

for x in urlList:
	print (x)
	count +=1
print('There are: ',count, ' total URLs')	
print('\n\n\n\n\n')

XPATH_NAME = './/a/text()'
XPATH_COMPANY = './/div[@class="flexbox empLoc"]/div/text()[1]'
XPATH_LOC = './/span[@class="subtle loc"]/text()'
XPATH_SALARY = './/span[@class="green small"]/text()[1]'

# XPATH_NAME = './/*[@class="jobViewJobTitleWrap"]/text()'
# XPATH_COMPANY = './/*[@class="strong ib"]/text()'
# XPATH_LOC = './/*[@class="subtle ib"]/text()'
# XPATH_SALARY = ".//*[@class='salEst']/text()"
XPATH_EVERYTHING = '//li[@class="jl"]'
XPATH_RATING = './/span[@class="compactStars "]/text()'

# sessions = HTMLSession()
count = 0
for this_url in urlList:
	if (count == 10):
		time.sleep(randint(5,10))
		count = 0
	# response = sessions.get(this_url)
	response = requests.post(this_url,headers = headers)
	print(response)
	tree = html.fromstring(response.content)
	everything = tree.xpath(XPATH_EVERYTHING)
	count+=1;
	for item in everything:
		name = item.xpath(XPATH_NAME)
		company = item.xpath(XPATH_COMPANY)
		rating = item.xpath(XPATH_RATING)
		salary = item.xpath(XPATH_SALARY)
		location = item.xpath(XPATH_LOC)

		name_clean = ''.join(name).strip('-') if name else None
		company_clean = ''.join(company).replace('\u2013', '-')
		company_clean.encode('UTF-8')
		company_cleaned = company_clean[0:company_clean.find('-')-1]
		rating_clean = ''.join(rating).strip()
		salary_clean = ''.join(salary).strip()
		if 'per hour' in salary_clean:
			salary_clean = ''
		print(salary_clean)
		low_salary = salary_clean[0+1:salary_clean.find('k')]
		high_salary = salary_clean[salary_clean.find('-')+2:-1]
		average_salary = ''

		if low_salary != '':
			average_salary = str((int(low_salary) + int(high_salary)) / 2)


		location_clean = ''.join(location).strip('-')

	#print(name, '\n',company, '\n',rating, '\n',salary, '\n',location, '\n')
		myDict = {
			"Name" : name_clean,
			"Company" : company_cleaned,
			"Min Salary" : low_salary,
            "Max Salary" : high_salary,
            "Average Salary" : average_salary,
			"Location" : location_clean,
			"Rating" : rating_clean
		}
		theBiggestList.append(myDict)	

with open('testJobResults.csv', 'wb') as myfile:
    fieldnames = ['Name', 'Company', 'Min Salary', 'Max Salary', 'Average Salary', 'Location', 'Rating']
    writer = csv.DictWriter(myfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for data in theBiggestList:
        writer.writerow(data)
csv = open('testJobResults.csv', 'r')
finalcsv = csv.read().encode(encoding = 'UTF-8', errors='strict')
client.import_csv(sheet.id, finalcsv) 
