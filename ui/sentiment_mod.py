#File: sentiment_mod.py
import joblib
# import sentiment_mod as s
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import spacy
from nltk.corpus import stopwords
sw_nltk = stopwords.words('english')
import re
import string
nlp = spacy.load('en_core_web_lg')
from nltk.tokenize import word_tokenize
# Autosaving every 60 seconds

def cleaner(text):
    text = remove_emojis(text)
    text = remove_html(text)
    text = remove_numbers(text)
    text = remove_lemma(text)
    text = text.lower()
    text = remove_pos(text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = [word for word in text.split(' ') if word not in sw_nltk]
    return " ".join(words)
    

def remove_numbers(string):
    return ''.join([i for i in string if not i.isdigit()])


def remove_pos(text):
    result_str = ''
    doc = nlp(text)
    allowed_pos = ['ADJ','ADV','VERB','ADP','NOUN']
    for token in doc:
        if token.pos_ in allowed_pos:
            result_str +=str(token) + ' '
    return result_str

def remove_lemma(text):
    doc = nlp(text)
    lemma = []
    result_str = ''
    for token in doc:
        if token.lemma_ not in lemma:
            lemma.append(token.lemma_)
            result_str +=str(token.lemma_)+' '
    return result_str

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)
    
def remove_html(text): 
    clean = re.compile(r'<.*?>')
    return re.sub(clean,'',text)


def final_processing(text):
    while "  " in text:
        text = text.replace("  ", " ")
    # words = word_tokenize(text)

    # string = ''
    # for word in words:
    #     lemma = lemmatizer.lemmatize(str(word),'a')
    #     string+=lemma+' '

    # unique = set()
    # for word in string.split():
    #     unique.add(word)
    return text


def open_and_load(address):
    address = 'Pickled_algos_tfidf/'+str(address)
    file_f = open(address,'rb')
    file = joblib.load(file_f)
    file_f.close()
    return file


pipeline = open_and_load('pipeline.pkl')

def sent(text):
    text = cleaner(text)
    text = final_processing(text)
    text_list = [text]
    sentiment = pipeline.predict(text_list)
    if sentiment==1:
        return 1
    else:
        return -1
# txt = input()
# print(sent(txt))
