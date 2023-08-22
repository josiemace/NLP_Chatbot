# -*- coding: utf-8 -*-
"""NLP_Chatbot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r-nxxU5hI7XAY6uplWoxWzDvT0W3Xmih
"""

#Refrences https://github.com/parulnith; https://en.wikipedia.org/wiki/Natural_language_processing;
#https://en.wikipedia.org/wiki/Lemmatisation; https://en.wikipedia.org/wiki/Stemming;
#https://en.wikipedia.org/wiki/Natural_Language_Toolkit;


#Importing libraries
import io
import random
import string
import warnings
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

#NLTK
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import texttiling
nltk.download('popular')
nltk.download('wordnet')



#Reading in corpus
with open('corpus_test.txt','r', encoding='utf8', errors ='ignore') as fin:
    txt = fin.read().lower()

#Tokenisation
sentences = nltk.sent_tokenize(txt)
words = nltk.word_tokenize(txt)

# Preprocessing
lemmatizer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmatizer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Handling Introductions
introductions = ("hello", "hi", "hello there","hey", "hi there")
responses = ["hello", "hi", "hello there", "nice to meet you", "hi! what can I help you with today"]

def intro(sentence):
    for word in sentence.split():
        if word.lower() in introductions:
            return random.choice(responses)


# Generating response
def response(user_response):
    blank_response=''
    sentences.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sentences)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        blank_response=blank_response+"I'm sorry, I don't have an understanding of that"
        return blank_response
    else:
        blank_response = blank_response+sentences[idx]
        return blank_response


flag=True
print("NLP_CB: I am a chatbot, I can answer questions you have about Natural Language Processing (NLP). Type 'Done' to exit ")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='done'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("NLP_CB: You are welcome!")
        else:
            if(intro(user_response)!=None):
                print("NLP_CB: "+intro(user_response))
            else:
                print("NLP_CB: ",end="")
                print(response(user_response))
                sentences.remove(user_response)
    else:
        flag=False
        print("NLP_CB: Thank you, goodbye!")