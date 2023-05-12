import pandas as pd
import numpy as np

import re
import unicodedata
import nltk
from nltk.corpus import stopwords

import acquire


def basic_clean(some_string):
    '''
    basic_clean will take in a single string as an argument,
    apply unicode normalization and ascii encoding,
    then decode and use regex to replace anything thats not a letter, number,
    or whitespace
    
    return: a cleaned version of some_string
    '''
    some_string = unicodedata.normalize('NFKD', some_string).encode('ascii', 'ignore').\
    decode('utf-8').lower()
    return re.sub(r'[^a-z0-9\s]', '', some_string)


def tokenize(some_string):
    '''
    Tokenize will take in a single argument (a string) and 
    return: a single tokenized string version of the input string
    '''
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(some_string, return_str=True)


def stem(some_string):
    '''
    stem will take in a single string instance and stem the contents
    it will return a single string
    '''
    # make my stemmer object
    stemmer = nltk.porter.PorterStemmer()
    # return the joined back together version of
    # the list comprehension that contains the list of every word
    #from the contents of your document stemmed
    return ' '.join([stemmer.stem(word) for word in some_string.split()])


def lemmatize(some_string):
    '''
    lemmatize will take in the contents of a single string,
    split up the contents with split()
    use the split contents as a list to apply a lemmatizer to
    each word,
    and return a single string of the lemmatized words joined
    with a single instance of whitespace (' '.join())
    '''
    lemmatizer = nltk.WordNetLemmatizer()
    return ' '.join(
        [lemmatizer.lemmatize(word,'v'
                             ) for word in some_string.split()])


def remove_stopwords(some_string, extra_words=[], keep_words=[]):
    '''
    remove stopwords will take in a single document as a string
    and return a new string that has stopwords removed
    '''
    stopwords_custom = set(stopwords.words('english')) - \
    set(keep_words)
    stopwords_custom = list(stopwords_custom.union(extra_words))
    return ' '.join([word for word in some_string.split()
                     if word not in stopwords_custom])


def transform_data(df):
    df = df.rename(columns={'content':'original'})
    # df['clean'] = cleaned and tokenized version with stopwords removed
    df['clean'] = df['original'].apply(basic_clean
                                      ).apply(tokenize
                                             ).apply(remove_stopwords)
    # df['stemmed'] = stemmed version of clean data
    df['stemmed'] = df['clean'].apply(stem)
    # df['lemmatized'] = lemmatized version of clean data
    df['lematized'] = df['clean'].apply(lemmatize)
    return df