import time 
import requests
import pandas as pds
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

url = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20"

option = Options()
option.headless = True
driver = webdriver.Chrome()
driver.get(url)

time.sleep(3)
#fecha pop-up
popup = driver.find_element(By.XPATH, "//*[@id='onetrust-accept-btn-handler']")

if(popup.is_displayed):
    popup.click()

time.sleep(3)

#pega os ultimos driver.find_element(By.XPATH,"//*[@id='__next']/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/thead/tr/th[9]").click()

element = driver.find_element(By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table")
html_content = element.get_attribute("outerHTML")

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')

df_full = pds.read_html(str(table))[0].head(10)
df = df_full[['Unnamed: 0', 'Player', 'Team', 'PTS']]
df.columns = ['pos', 'jogador', 'time', 'pontos']

top10ranking = {}

top10ranking['points'] = df.to_dict('records')

json_object = json.dumps(top10ranking)
fp = open('rankingNBA.json', 'w')
fp.write(json_object)
fp.close()


driver.quit()


