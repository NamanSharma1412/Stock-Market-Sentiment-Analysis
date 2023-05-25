import base64
import sentiment_mod as s
import pandas as pd
from datetime import datetime
import Stock_Market_web_scraper as getData
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
def plotter(stock_name):
    df,df_price = getData.get_stock_data(stock_name)
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
    for news in tqdm(df['news'],desc = 'Applying Sentiment Analysis'):
        sentiment.append(s.sent(news))
    df['sentiment'] = sentiment

    plot_data = df.groupby('dates',as_index=False).mean()

    fig, (ax1, ax2, ax3) = plt.subplots(figsize=(14, 20), nrows=3, ncols=1)
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
    np.set_printoptions(suppress=True)
    print('Correlation matrix:- ')
    print(df_data.corr())
    
    
    plt.subplots_adjust(hspace=0.5)
    add = './temp/graph_%s.png'%stock_name
    plt.savefig(add)
    
    # with open('./temp/graph_%s.png'%stock_name, "rb") as image_file:
    #     encoded_string = base64.b64encode(image_file.read())
    #     encoded_string = encoded_string.decode('utf-8')
    #     encoded_string = str(encoded_string)
    #     encoded_string = 'data:image/png;base64,'+encoded_string

    
#     plt.suptitle(stock_name)
    return add,stats.pearsonr(df_data['Close'],df_data['sentiment'])[0],stats.spearmanr(df_data['Close'],df_data['sentiment'])[0]