from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap
import completer
from PyQt5.QtCore import Qt, QTimer,QThread,pyqtSignal
from PyQt5 import uic
import completer
import qdarkstyle
from Plotter import plotter as plot
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
import base64
import sentiment_mod as s
import pandas as pd
from datetime import datetime
from tqdm.auto import tqdm
import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image
import seaborn as sns
import scipy.stats as stats
months_dict = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

class MyGUI(QDialog):
    
    def __init__(self):
        super(MyGUI,self).__init__()
        self.resize(1600,800)
        uic.loadUi('./ui/MyGUI.ui',self)
        self.show()
        self.progressBar.setVisible(False)
        self.progressBar_2.setVisible(False)
        self.progressBar_3.setVisible(False)
        stock_names = completer.stock_lists
        completer__ = QCompleter(stock_names)
        self.lineEdit.setCompleter(completer__)
        self.lineEdit.textChanged.connect(self.on_text_changed)
        self.pushButton_2.clicked.connect(self.toggle_progressBar)
        self.pushButton_2.clicked.connect(self.plots)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda: self.delayed_text_changed(stock_names))
        # self.image_window = ImageWindow()
    
    def plots(self):
        text = self.lineEdit.text()
        

        # Create a worker thread for executing the plot function
        self.worker = PlotWorker(text)
        self.worker.progress.connect(self.reportProgress)
        self.worker.progress_2.connect(self.reportProgress2)
        self.worker.len_of_df.connect(self.get_len)
        self.worker.progress_3.connect(self.reportProgress3)
        self.worker.finished.connect(self.show_image)
        self.worker.finished.connect(self.worker.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.close_bar)
        self.worker.start()
    
    def close_bar(self,str):
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)
        self.progressBar.setStyleSheet(qdarkstyle.load_stylesheet())
        self.progressBar_2.setValue(0)
        self.progressBar_2.setVisible(False)
        self.progressBar_2.setStyleSheet(qdarkstyle.load_stylesheet())
        self.progressBar_3.setValue(0)
        self.progressBar_3.setVisible(False)    
        self.progressBar_3.setStyleSheet(qdarkstyle.load_stylesheet())
    def get_len(self,i):
        self.progressBar_3.setMaximum(i-1)
    def reportProgress(self,i):
        if(i==self.progressBar.maximum()):
            self.progressBar.setStyleSheet("QProgressBar::chunk { background-color: green; }")
        self.progressBar.setValue(i) 
    def reportProgress2(self,i):
        if(i==self.progressBar_2.maximum()):
            self.progressBar_2.setStyleSheet("QProgressBar::chunk { background-color: green; }")
        self.progressBar_2.setValue(i)
    def reportProgress3(self,i):
        if(i==self.progressBar_3.maximum()):
            self.progressBar_3.setStyleSheet("QProgressBar::chunk { background-color: green; }")
        self.progressBar_3.setValue(i)
        
    def toggle_progressBar(self):
        self.progressBar.setVisible(not self.progressBar.isVisible())  
        self.progressBar.setMaximum(200-1)
        self.progressBar_2.setVisible(not self.progressBar_2.isVisible())
        self.progressBar_2.setMaximum(1200-1)
        self.progressBar_3.setVisible(not self.progressBar_3.isVisible())          
                
    def on_text_changed(self, text):
        self.timer.start(500)  # Adjust the delay (in milliseconds) according to your needs
    
    def delayed_text_changed(self, stock_names):
        text = self.lineEdit.text()
        if text == "":
            self.pushButton_2.setText('Analyze')
            self.pushButton_2.setEnabled(False)
        elif text in stock_names:
            self.pushButton_2.setEnabled(True)
            self.pushButton_2.setText('Analyze')
            self.change_button_style('green')
        else:
            self.pushButton_2.setEnabled(False)
            self.pushButton_2.setText('Invalid!')
            self.change_button_style('red')
            
    def change_button_style(self, color):
        self.pushButton_2.setStyleSheet('')
        if color == 'green':
            self.pushButton_2.setStyleSheet("background-color: green")
        elif color == 'red':
            self.pushButton_2.setStyleSheet("background-color: red")

    def show_image(self,image_path):
        self.image_window = ImageWindow(image_path)
        # self.image_window.show()
        # self.worker.stop()

class ImageWindow(QDialog):
    def __init__(self, image_path):
        super().__init__()
        
        # Load the image using QPixmap
        pixmap = QPixmap(image_path)
        
        # Create a QLabel to display the image
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        
        # Create a QScrollArea and set the image label as its widget
        scroll_area = QScrollArea()
        scroll_area.setWidget(image_label)
        
        # corr = QLabel()
        # Set the layout for the window
        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        # layout.addWidget(corr)
        self.setLayout(layout)
        
        # Set the window properties
        self.setWindowTitle('Sentiment Analysis Report')
        self.resize(1920,1080)
        self.show()

class PlotWorker(QThread):
    finished = pyqtSignal(str)
    progress = pyqtSignal(int)
    progress_2 = pyqtSignal(int)
    progress_3 = pyqtSignal(int)
    len_of_df = pyqtSignal(int)
    corr = pyqtSignal(str)
    
    def __init__(self,text):
        super().__init__()
        self.text = text
        self._is_running = True
    
    def get_stock_data(self,stock_name):
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
            self.progress.emit(i)
            try:
                while not target_element.is_displayed():
                    try:
                        wd.execute_script("arguments[0].scrollIntoView();", target_element)
                        wd.switch_to.window(wd.window_handles[0])
                    except NoSuchElementException:
                        break
                try:
                    load_more_button.click()
    #                 wd.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
                except NoSuchElementException:
                    break
            except StaleElementReferenceException:
                break
            wd.switch_to.window(wd.window_handles[0])
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
            self.progress_2.emit(i)
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
            
        
        return df_news,df_price,ticker_name

        # df = get_stock_news('reliance')

    
        
    def plot(self,stock_name):
        df,df_price,ticker_name = self.get_stock_data(stock_name)
        curr_month = datetime.now().month
        
        months_labels = []
        for i in range(1,13):
            months_labels.append(curr_month-i)
        months_dict_temp = {}
        for i,month in zip(months_labels,months_dict.values()):
            months_dict_temp[i] = month
        
        def remove_this_week(text):
            if ('day' in text) or ('week' in text) or ('hour' in text) or ('minute' in text):
                return months_dict[datetime.now().month]
            elif('year' in text):
                return pd.NA
            else:
                month = int(text.split()[0])
                
                if month<datetime.now().month:
                    return months_dict_temp[month]
                else:
                    month = month-12
                    return months_dict_temp[month]
                
        df['dates'] = df['dates'].apply(remove_this_week)
        df.dropna(inplace=True)
        sentiment = []
        i=0
        self.len_of_df.emit(len(df))
        for news in tqdm(df['news'],desc = 'Applying Sentiment Analysis'):
            self.progress_3.emit(i)
            sentiment.append(s.sent(news))
            i+=1
        df['sentiment'] = sentiment

        plot_data = df.groupby('dates',as_index=False).mean()

        fig, (ax1, ax2, ax3) = plt.subplots(figsize=(14, 20), nrows=3, ncols=1)
        plt.suptitle('Sentiment Analysis Report of %s'%ticker_name)
        order = list(df['dates'].unique())
        order.reverse()
        ax30 = sns.pointplot(plot_data, x='dates', y='sentiment', order=order, ax=ax1)
        ax4 = sns.barplot(plot_data, x='dates', y='sentiment', ax=ax1, order=order)
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
        ax1.set_title('Sentiment Plot')

        df_price['dates'] = df_price['dates'].map(months_dict)
        ax5 = sns.pointplot(df_price, x='dates', y='Close', order=list(df_price['dates']), ax=ax2)
        ax6 = sns.barplot(df_price, x='dates', y='Close', order=list(df_price['dates']), ax=ax2)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
        ax2.set_title('Mean stock price plot')

        df_data = pd.DataFrame()
        df_data = pd.merge(plot_data,df_price,on='dates',how='left')
        
        ax300 = sns.lineplot(df_data,x='sentiment',y='Close',ax=ax3)
        ax3.set_title('Stock Price vs Sentiment')
        print('Pearsons correlation:- ',end='')
        print(stats.pearsonr(df_data['Close'],df_data['sentiment'])[0])
        print('Spearmans correlation:- ',end='')
        print(stats.spearmanr(df_data['Close'],df_data['sentiment'])[0])
        res_string = f"{stats.pearsonr(df_data['Close'],df_data['sentiment'])[0]} {stats.spearmanr(df_data['Close'],df_data['sentiment'])[0]}"
        plt.suptitle(f'''Sentiment Analysis Report of {ticker_name}
                             {res_string}''')
        np.set_printoptions(suppress=True)
        print('Correlation matrix:- ')
        print(df_data.corr())
        # plt.text(0,0,res_string,bbox=dict(facecolor='red', alpha=0.5))
        # self.corr.emit(res_string)
        
        plt.subplots_adjust(hspace=0.5)
        add = './temp/graph_%s.png'%stock_name
        plt.savefig(add)
        
        # with open('./temp/graph_%s.png'%stock_name, "rb") as image_file:
        #     encoded_string = base64.b64encode(image_file.read())
        #     encoded_string = encoded_string.decode('utf-8')
        #     encoded_string = str(encoded_string)
        #     encoded_string = 'data:image/png;base64,'+encoded_string

        
    #     plt.suptitle(stock_name)
        return add
    
    
    
    def run(self):
        graph = self.plot(self.text)
        self.finished.emit(graph)  
        # self.thread.quit()
        
    # def stop(self):
    #     self._is_running = False
    

def main():
    app = QApplication([])
    window = MyGUI()
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    app.exec_()

if __name__ == '__main__':
    main()
