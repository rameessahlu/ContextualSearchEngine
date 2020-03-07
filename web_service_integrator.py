import os, json, random
import re
import docx2txt
import fitz
import zipfile
import PyPDF2
import minecart
import base64
import shutil
import xlrd
import csv
import win32com.client
import  random
from elasticsearch import Elasticsearch
from api import elastic_search
from classifier import pre_processor as pp
from metadata import constants
#from image_classifier import img_classifier as ic

def createSubQueryList(tokens, token_type='bigram', clause_type='must'):
        sub_query_list = []
        for token in tokens:
            if token is not None and token_type == 'bigram' and len(token.split()) == 2:
                sub_query_list.append({'term' : {'tags' : token}})
            elif (token is not None and token_type == 'unigram' and len(token.split()) == 1):
                sub_query_list.append({'term' : {'tags' : token}})
        sub_query_list = {clause_type: sub_query_list}
        print('DEBUG# Token:{} Clause:{} subQuery:{}'.format(token_type, clause_type, str(sub_query_list)))
        return sub_query_list

def createSession():
    es = Elasticsearch(
        scheme="http",
        port=9200,
        http_auth=(constants.es_username, constants.es_password)
    )
    return elastic_search.FileIndex(es, constants)

def context_query(query):
    fi_obj = createSession()
    _relavance_score = fi_obj.context_search(query)
    return _relavance_score

def classify_image(image_path):
    return ic.label_image(image_path)

def reinitialization():
    output_dir =  os.path.join(main_pkg_dir, 'output')
    metadata_dir = os.path.join(output_dir, 'metadatas')
    fi_obj = createSession()
    fi_obj.delete_indice()
    fi_obj.create_indice()
    for (root, dirs, filenames) in os.walk(metadata_dir): 
        for fname in filenames:
            fi_obj.file_metadocs_insertion(os.path.join(metadata_dir, fname))
        break

def tag_query(query):
    fi_obj = createSession()
    tokens = pp.getFilteredContent(query)
    hit_count = 0
    token_type_and_clause = [('bigram', 'must'),('bigram', 'should'), ('unigram', 'must'),('unigram', 'should')]
    '''
    bigram exactMatch(must_clause)
    bigram partialMatch(should_clause)
    unigram exactMatch(must_clause)
    unigram partialMatch(should_clause)
    '''
    for tt_n_c in token_type_and_clause:
        sub_query_list = createSubQueryList(tokens, tt_n_c[0], tt_n_c[1])
        if len(sub_query_list[tt_n_c[1]]) != 0:
            _relavance_score = fi_obj.tag_search(sub_query_list)
            print(_relavance_score)
            if len(_relavance_score['hits']['hits']) > 0:
                return _relavance_score