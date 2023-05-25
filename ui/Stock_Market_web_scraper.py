import time
import requests 
import io
import hashlib
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
import goto
from PIL import Image, ImageDraw
import pandas as pd
from datetime import timedelta,datetime,date
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from tqdm.auto import tqdm
import yfinance as yf
from dateutil.relativedelta import relativedelta
pd.options.mode.chained_assignment = None  # Suppress the warning

def get_stock_data(stock_name):
    wd = webdriver.Chrome(executable_path="C:\\Python\\scraping\\chromedriver.exe")

    def scroll_to_bottom(wd):
        scroll_count=0
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    search_url = 'https://www.tickertape.in/'
    wd.get(search_url)
    search_bar = wd.find_element_by_xpath('//*[@id="search-stock-input"]')
    search_bar.send_keys(stock_name)
    time.sleep(0.8)
    search_bar.send_keys(Keys.ENTER)
    time.sleep(0.8)
    news_url = str(wd.current_url)+'/news?checklist=basic&type=news'
    wd.get(news_url)

    # progress_bar_1 = tqdm(total=200, desc='Extracting Headlines', unit='iteration')
    ticker_name = wd.find_element_by_xpath('//*[@id="app-container"]/div/div/div[1]/div/div[1]/div[2]/span')
    ticker_name = ticker_name.text

    load_more_button = wd.find_element_by_css_selector('#load-more > button')
    target_element = load_more_button
    for i in tqdm(range(0,200),desc='Extracting Headlines'):
        # scroll_to_bottom(wd)
        try:
            while not target_element.is_displayed():
                try:
                    wd.execute_script("arguments[0].scrollIntoView();", target_element)
                    wd.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
                except NoSuchElementException:
                    break
            try:
                load_more_button.click()
#                 wd.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
            except NoSuchElementException:
                break
        except StaleElementReferenceException:
            break
        time.sleep(0.04)
    # progress_bar_1.close()

    # progress_bar_2 = tqdm(total=1000, desc='Adding Headlines', unit='iteration')
    news_list = []
    dates_list = []
    pub_list = []

    news = wd.find_elements_by_class_name('shave-root')
    dates = wd.find_elements_by_class_name('jsx-3953764037.typography-body-regular-xs.news-info.text-tertiary')
    # wd.quit()
    # dates = wd.find_elements_by_class_name('jsx-3953764037')
    # data = wd.find_elements_by_class_name('jsx-3440134818 news-description')
    # dates = dates_1.extend(dates)

    for i in tqdm(range(0,1200),desc = 'Adding Headlines and Dates'):
        date_text = str(dates[i].text)
        if('year' in date_text):
            continue
        news_list.append(news[i].text)
        dates_list.append(date_text.split('•')[0])
        pub_list.append(date_text.split('•')[1])
    # progress_bar_2.close()

    # import pandas as pd
     
    def calculate_average_stock_price_per_month(start_date, end_date):
        # Create an empty DataFrame to store the stock prices
        df = pd.DataFrame()
        ticker = ticker_name+'.NS'
        stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False)

        df = stock_data

        # Reset the index and keep only the 'Date' and 'Close' columns
        df.reset_index(inplace=True)
        df = df[['Date', 'Close']]

        # Convert the 'Date' column to datetime type
        df['Date'] = pd.to_datetime(df['Date'])

        # Extract the year and month from the 'Date' column
        df['dates'] = df['Date'].dt.to_period('M')

        # Calculate the average stock price per month
        average_prices = df.groupby('dates',as_index=False)['Close'].median()
        average_prices['dates'] = average_prices['dates'].apply(lambda x:x.month)
        return average_prices


    stock_dict = {'news':news_list,'dates':dates_list,'publisher':pub_list}
    df_news = pd.DataFrame.from_dict(stock_dict)
    time_data = list(df_news['dates'])
    time_data.reverse()
    for i in time_data:
        if 'month' in i:
            diff = i.split()[0]
            break
    end_date = date.today()
    start_date =  end_date - relativedelta(months=int(diff)) 

    df_price = calculate_average_stock_price_per_month(start_date,end_date)    
        
      
    return df_news,df_price

    # df = get_stock_news('reliance')
