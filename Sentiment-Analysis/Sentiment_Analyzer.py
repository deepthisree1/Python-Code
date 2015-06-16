# -*- coding: utf-8 -*-
"""
Created on Sun May 31 23:02:29 2015

@author: 'deepthi'
"""
from Tkinter import Tk
from tkFileDialog import askopenfilename
import re
#import datetime
from nltk.corpus import stopwords
from textblob import TextBlob
import pandas as pd

emoticons_str = r"""
(?:
    [:=;] # Eyes
    [oO\-]? # Nose (optional)
    [D\)\]\
    (\]/\\OpP] # Mouth
)"""

custom_stops = set(["'",",","Thu","Wed","Fri","Tue","May","RT",":",".",";"])

regex_str = [
emoticons_str,
r'<[^>]+>', # HTML tags
r'(?:@[\w_]+)', # @-mentions
r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '/Users/deepthi/Downloads/data preprocessing.py:157
r'(?:[\w_]+)', # other words
r'(?:\S)' # anything else
]
tweets_without_stop={}
get_sentiments={}
store_polarity={}

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
tweets={}
new_data=[]
def read_inputfile():
    Tk().withdraw()
    filename = askopenfilename()
    new =open(filename,"r")
    line = new.read()
    data=re.split(r"\+0000 2015\n", line)
    new.close
    return data
    
def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    stop = stopwords.words('english')
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    datu = [unicode(toks, 'ascii', 'ignore') for toks in tokens if toks not in custom_stops if toks not in stop if toks.isdigit() !=True]
    return datu

def sentiment_analyze(token_for_sentiments):
    for key,value in token_for_sentiments.iteritems():
        token_to_text =""
        for tokens in value:
            newvalue_withspace=""
            newvalue_withspace = str(tokens) + " "
            token_to_text += newvalue_withspace
        print token_to_text
        blob = TextBlob(token_to_text)
        n=0
        sumup=0
        for sentence in blob.sentences:
            print sentence.sentiment.polarity
            sumup += sentence.sentiment.polarity
            n=n+1 
        print "The value of sum:  "+str(sumup)
        if sumup == 0:
            store_polarity[key]="Neutral"
        elif sentence.sentiment.polarity > 0:
            store_polarity[key]="Positive"
        else:
            store_polarity[key]="Negative"
    #print store_polarity
    return store_polarity
    

def main_function():
    read_tweets_newfile=read_inputfile()
    for lines in read_tweets_newfile:
        tweets_without_stop[lines] = preprocess(lines)
    tweets_frame = pd.DataFrame(tweets_without_stop.items())
    print tweets_frame
    #print tweets_without_stop
    get_sentiments = sentiment_analyze(tweets_without_stop)
    sentiment_frame = pd.DataFrame(get_sentiments.items())
    print sentiment_frame
    sentiment_frame.to_csv("your csv file")
    #print get_sentiments
    
