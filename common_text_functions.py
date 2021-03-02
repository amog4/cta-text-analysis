import pandas as pd 
import numpy as np 
import nltk
#import spacy as spacy
#import seaborn 
#import matplotlib.pyplot as plt
import collections
import math
import re
from enum import Enum
from collections import Counter
from nltk import FreqDist
import ast

def file_path(path:str):
    """
    :param str path: The file path 
    :return: file path
    """
    return path


def simple_read(file_path:str,file_name:str,file_type:str,sheet_name=None, enc = None):
    """
    :param str file_path: file path 
    :param str file_name: file name 
    :param str file_type: csv or excel
    :param str sheet_name: if excel then sheet_name 
    :return: dataframe 
    """
    if file_type == 'csv' and enc == None:
        return pd.read_csv(file_path+file_name )
    elif file_type == 'csv' and enc is not None:
        return pd.read_csv(file_path+file_name , encoding=enc)
    elif file_type == 'excel':
        return pd.read_excel(file_path+file_name,sheet_name)
    else:
        print("File Type Not Found")



class platform(Enum):
    """
    :param Enum: Iterates over the items below
    """
    Facebook = 1
    Twitter = 2
    Instagram = 3
    Youtube = 4




def wordtokenize(sentence:str,type:str,df,column = None,lower=False):

    """
    Tokenize words for given sentence or dataframe
    :param sentence str: Takes single sentence
    :param type str: sentence or dataframe
    :param df : Takes data frame 
    :param column: data frame column for tokenization
    :param lower boolean: Lower the words in set to true
    :return: sentence or dataframe 
    """
    try:
        if type == 'sentence':
            tokens = nltk.tokenize.word_tokenize(sentence)
            return tokens
        elif type == 'df':
            if lower == False:
                df['words_tokenzie'] = df[column].apply(lambda sentence: nltk.tokenize.word_tokenize(sentence))
            else:
                df['words_tokenzie'] = df[column].apply(lambda sentence: [word.lower() for word in nltk.tokenize.word_tokenize(sentence) ])
            return df
        else:
            print("Type not applicable")
            
    except Exception as e:
        print(f"error is about {e}")



   
def word_frequency_df(df,column:str):
    """
    New word frequency df
    :param  df: dataframe
    return: A new dataframe with words & Frequency
    """
    list_words = [word for sent_word in df[column] for word in sent_word]
    freq = pd.DataFrame.from_dict(FreqDist(list_words),orient='index',columns = ['Freq']).reset_index().rename(columns={'index':'Word'}).sort_values(by='Freq',ascending=False).reset_index(drop=True)
    freq['Word'] = freq['Word'].apply(lambda x: ' '.join(x) if isinstance(x,tuple) else x)
    return freq


def stop_words(type:str,stop:set,sentence,df,sentence_type,column=None):
    """
    :param sentence str: Takes single sentence
    :param type str: sentence or dataframe
    :param df : Takes data frame 
    :param column: data frame column for tokenization
    :param stop set: containes all the stop words
    """
    if type == 'df' and sentence_type == 'str':
        df['stop_words_removed']  = df[column].apply(lambda x : 
                                [ word for word in x.split() if word not in stop ])

        return df

    elif type == 'df' and sentence_type == 'list':
        df['stop_words_removed']  = df[column].apply(lambda x : 
                                [ word for word in x if word not in stop ])


        return df
    else:
        return  [ word for word in sentence.split() if word not in stop ]




def bigram_trigram(df,column,bigram=False,trigram=False):

    if bigram == True:

        df['bi_grams'] = df[column].apply(lambda word_list : list(nltk.bigrams(word_list )) )
        #df['bi_grams'] = df['bi_grams'].apply(lambda x: ' '.join( ))

    if trigram == True:
        df['tri_grams'] = df[column].apply(lambda word_list : list(nltk.trigrams(word_list )) )
        #df['tri_grams'] = df['tri_grams'].apply(lambda x: ' '.join([w for sub in x for w in sub] ))

    return df


def mk_dir(directory):

    try:
        os.mkdir(directory)
    except:
        print("Directory exists")
        pass 

