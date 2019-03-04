#! python3 -i FLgTransactions.py
# a script that opens SHORT SEASON minor league transactions.

import re,time,urllib.request,pyperclip,sys
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime as dt


TXL = ''
CAL = ''
SOU = ''
PCL = ''
EAS = ''
SAL = ''
INT = 'http://www.milb.com/milb/stats/stats.jsp?t=l_trn&lid=117&sid=l117'
MWL = ''
AFL = ''
APP = ''
AZL = ''
CRL = ''
FSL = ''
GCL = ''
MEX = ''
NWL = ''
NYP = ''
PIO = ''
DSL = ''
DWL = ''
XWL = ''
PRL = ''
VWL = ''

#ALL LEAGUE TRANSACTIONS
ALgTransactions = [TXL,CAL,SOU,PCL,EAS,SAL,INT,MWL,AFL,APP,AZL,
                      CRL,FSL,GCL,MEX,NWL,NYP,PIO,DSL,DWL,XWL,PRL,
                      VWL]
# REGULAR SEASON TRANSACTIONS
RLgTransactions = [TXL,CAL,SOU,PCL,EAS,SAL,INT,MWL,AFL,APP,AZL,
                      CRL,FSL,GCL,MEX,NWL,NYP,PIO,DSL]

#SHORT SEASON LEAGUE TRANSACTIONS
SLgTransactions = [APP,AZL,GCL,NWL,NYP,PIO,DSL]

#FULL SEASON LEAGUE TRANSACTIONS
FLgTransactions = [TXL,CAL,SOU,PCL,EAS,SAL,INT,MWL,CRL,FSL,MEX,]

#Driveline Example
FLgTransactions = [INT,]


#WINTER LEAGUE TRANSACTIONS
WLgTransactions = [AFL,DWL,XWL,PRL,VWL]

def FLgTransact():
    for x in FLgTransactions:
        try:
            start = dt.datetime.now()
            strStart = start.strftime('%b, %d | %H:%M:%S %p')
            print('-'*70+' \nStart Time: '+strStart + '\n'+'-'*70)
            LgFile = urllib.request.urlopen(x)
            LgHTML = LgFile.read()
            LgFile.close()
            driver= webdriver.Chrome()
            driver.get(x) ## INSTRUMENTAL IN RETRIEVING THE TABLE.

            soup = BeautifulSoup(driver.page_source, 'lxml')
            table = soup.table # first table, a tag
            tbody = table.tbody # table first body, a tag
            tr = tbody.tr # body first row, a tag
            trows = tbody('tr') # returns a ResultSet
            tdRS = tbody('td') # returns tr as ResultSet
            trEven = tbody('tr',class_='dataRow even') # returns a ResultSet
            trOdd = tbody('tr',class_='dataRow odd')
        ##        print(trOdd, trEven)
        ##        print(table.prettify())
            a = trows
            pyperclip.copy('Copied is '+str(a)+'.')
        ##        ma = re.findall(r'">([123\D]+?)</',str(a))
        ##        b = len(ma)
        ##        print(TrLogFindDate)
        ####        print(ma)
        ##        for x in range(b):    
        ##            print(ma[x])

            TrLogFindDate = re.findall(r'\d{2}/\d{2}/\d{4}',str(a))# date

            # a Regex that finds the headers
            ma = re.findall(r'">(\D+?)</',str(a))[:5]
            b = len(ma)

        #a Regex that finds the transactions cells
            ma2 = re.findall(r'">([123\D]+?)</',str(a))[6:] # will always be a multiple of 4 i.e. 4,8,12,16,24,28,32,36,40
            c = len(ma2)
            d = len(TrLogFindDate)

            m=0
            e = len(TrLogFindDate[m])
            f = e+15
            g = f+15
            print('-'*70)
            print('TRANSACTIONS FOR '+ma[0]+'. \nLink: '+x)
            now = dt.datetime.now().strftime('%b, %d | %H:%M:%S %p')
            print(now)
            print('-'*70)          
            print('DATE'.rjust(e,' '),end='')
            print('LEAGUE TRANSACTIONS'.rjust((f),' '),end='')
            print('TRANSACTIONS DESCRIPTION'.rjust(g,' '))
            for x in range(3,c,4):   
                print(TrLogFindDate[m],end=" | ")
                print(ma[0]+' | ',end='')
                print(ma2[x])
                m+=1
            end=dt.datetime.now()
            strEnd = end.strftime('%b, %d | %H:%M:%S %p')
            strTTime =str(end-start)
            print('-'*70+' \nEnd Time: '+strEnd + '\n'+'-'*70)
            print('\nTotal Time: '+strTTime)
        except AttributeError:
            print('-'*70)
            print('NO TRANSACTIONS FOR LINK: '+x)
            print('-'*70)
            continue
        finally:
            """ closes the webbrowser"""
            driver.close()
FLgTransact()
