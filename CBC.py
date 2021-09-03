
#Extracting CBC news title, full text and publishing date using Beautifulsoup and selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
import pandas as pd


class CBCScraping:
        def __init__(self, page_number):
                
                chrome_options = Options()
                #Open an empty browser
                self.driver = webdriver.Chrome(executable_path=str('./chromedriver'), options=chrome_options)

                #Go to CBC cite
                self.driver.get("https://www.cbc.ca/")

                #WebDriver wait for 5 seconds to load the page
                self.driver.implicitly_wait(5)

                #Find the search bar
                search_Button = self.driver.find_element_by_id("searchButton").click() 
                time.sleep(1)

                #Type in the search term
                search_input = self.driver.find_element_by_class_name("searchInput")
                search_input.send_keys("Covid-19") 
                #Find the search button
                search_btn = self.driver.find_element_by_class_name("searchButton") 
                search_btn.click()
                time.sleep(5)

                #Record the first page
                html = [self.driver.page_source]
                i=1
                while i<page_number:
                        try:
                                Next = self.driver.find_element_by_class_name('loadMore')
                                time.sleep(5) 
                                self.driver.execute_script("arguments[0].click();", Next)
                                print('Button Clicked Successfully')
                                i=i+1
                                html.append(self.driver.page_source)
                        except TimeoutException:
                                print("Time out!")
                                break

                time.sleep(2) 

                
                self.get_dataframe()
        
        #Get news links
        def get_links(self):
                links = self.driver.find_elements_by_class_name('card')
                self.link_urls = [link.get_attribute('href') for link in links]
                #link_urls = link_urls[15:20]

        #Get date time
        def get_date(self):
                find_time = self.driver.find_elements_by_class_name('timeStamp')
                date_time = [time.get_attribute('datetime') for time in find_time]
                self.date_time = [i.split('T')[0] for i in date_time] 

        #Get head and description
        def get_head_desc(self):
                self.head = []
                self.Desc = []
                for links in self.link_urls:
                        #Get the HTML code
                        page = requests.get(links)
                        soup = BeautifulSoup(page.content, 'html.parser')
                        
                        Description1 = soup.find_all(id = 'MainContentDescription')
                        Description2 = soup.find_all(class_ = 'story')
                        Description3 = soup.find_all(class_ = 'detailPageDescription embeddedHtml')

                        if Description1 != None:
                                for i in Description1:
                                        a = i.text
                                        self.Desc.append(a)

                        if Description2 != None:
                                for i in Description2:
                                        a = i.text
                                        self.Desc.append(a)
                        
                        if Description3 != None:
                                for i in Description3:
                                        a = i.text
                                        self.Desc.append(a)

                        
                        heading1 = soup.find(id='MainContentTitle')     
                        heading2 = soup.find(class_='detailHeadline')
                        heading3 = soup.find(class_='ule-pid-current-item-title')

                        if heading1 != None:
                                heading = heading1.text
                                self.head.append(heading)
                        
                        if heading2 != None:
                                heading = heading2.text
                                self.head.append(heading)
                        
                        if heading3 != None:
                                heading = heading3.text
                                self.head.append(heading)
        
        #Convert data to dataframe
        def get_dataframe(self):
                self.get_links()
                self.get_date()
                self.get_head_desc()
                
                dataframe = {'Date': self.date_time, 'Headline': self.head, 'Content': self.Desc ,'Link': self.link_urls}
                data = pd.DataFrame(dataframe)
                data.to_csv('CBC.csv')


if __name__== "__main__":
        CBC = CBCScraping(20)
