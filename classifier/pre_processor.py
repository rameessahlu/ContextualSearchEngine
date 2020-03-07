#!/usr/bin/env python
# coding: utf-8

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.util import ngrams


def getTokens(data):
    try:
        tokens = word_tokenize(data)
        bigrams = list(nltk.bigrams(data.split()))#[" ".join(bi_gram) for bi_gram in ngrams(tokens, 2)]
        bigrams = [ "%s %s" % x for x in bigrams ]#[" ".join(bi_gram) for bi_gram in ngrams(tokens, 2)]
        tokens.extend(bigrams)#[" ".join(bi_gram) for bi_gram in ngrams(tokens, 2)]
        return tokens
    except StopIteration:
        return null

def processStemming(data):
    ps = PorterStemmer()
    wordStemed = []

    for word in data:
        if type(word) is tuple:
            wordStemed.append((ps.stem(word[0]), ps.stem(word[1])))
        else:
            wordStemed.append(ps.stem(word))
    return wordStemed  # [:500]returning only 500 words


def removeStopWords(data):
    stopWords = set(stopwords.words('english'))
    wordsFiltered = ''

    for w in data.split():
        if (w not in stopWords):
            wordsFiltered = wordsFiltered +' {}'.format(w)
    return wordsFiltered


def removeSpecialChar(data):
    slist = (
    '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '{', '}', '[', ']', '|', '\\', ':', '"', "'",
    ';', '<', '>', ',', '.', '?', '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0')

    for s in slist:
        data = data.replace(s, '')
    return data

def getFilteredContent(data):
    data = removeSpecialChar(data)
    data = removeStopWords(data)
    if data != '':
      data = getTokens(data)
    data = processStemming(data)
    return data
