# Stock-Market-Sentiment-Analysis
A Program to scrape and analyze financial news and perform sentiment analysis to understand and capture public sentiment

![image](https://github.com/NamanSharma1412/Stock-Market-Sentiment-Analysis/assets/73564310/a28d2903-1f85-4ba4-808b-d3f40e9f50fe)

### File Structure:- 
1) Pickled_algos_tfidf:- contains the main pipeline made from the trained model and fitted tfidf object used for sentiment analysis
2) VAULT :- contains a zip file consisting of previous pipeline versions used to test the model's performance
3) data :- contains the financial news data used for training the model
4) output:- contains the output plot of the program
5) temp:- contains a single example plot 
6) ui:- ui.py contains the program, to run the program on your local device, run the porgram and the stock name/ticker to analyze, the program runs and outputs
a plot of the mean sentiment value of the stock against the stock price movement of the stock

![image](https://github.com/NamanSharma1412/Stock-Market-Sentiment-Analysis/assets/73564310/8fad2d62-2092-4205-9f21-34dca6b1f6dd)

The numbers beneath the title of the plot represent the pearson's and spearman's correlation respectively between the sentiment value of the stock and stock price movement
