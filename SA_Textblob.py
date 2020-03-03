# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 17:00:13 2020

@author: hp
"""

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import pandas as pd
#def sentiment(polarity):
#    if blob.sentiment.polarity < 0:
#        print("Negative")
#    elif blob.sentiment.polarity > 0:
#        print("Positive")
#    else:
#        print("Neutral")
data = pd.read_excel("G:\Semester 2\Text Analytics\Movies.xlsx")

text = data.Text

for var in text:
    ans = TextBlob(var,  analyzer = NaiveBayesAnalyzer())
    print(ans.sentiment)

blob = "The movie is not that interesting!"

ans = TextBlob(blob,  analyzer = NaiveBayesAnalyzer())
print(ans.sentiment)

#sentiment(ans.sentiment.polarity)