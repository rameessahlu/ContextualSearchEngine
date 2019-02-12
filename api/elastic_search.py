from elasticsearch import Elasticsearch
from elasticsearch import helpers
from pprint import pprint
import json

class FileIndex:
    constants = None
    
    def __init__(self, es, constants):
        self.es = es
        self.constants = constants

    def create_indice(self):
        #create index in elasticsearch
        self.es.indices.create(index=self.constants.CSEindex, ignore=400, body={"mappings" : {"file_meta_data" : {"properties" : {"text_content" : { "type" : "nested" }}}}})
        print('Indice "CSE" created!')

    def create_mapping(self):
        #if we are not satisfied with the auto mapping done by the elasticsearch
        self.es.indices.put_mapping(
            index= self.constants.CSEindex,
            doc_type= 'file_meta_data',
            body={"mappings" : {"_doc" : {"properties" : {"text_content" : { "type" : "nested" }}}}}
        )

    def get_mapping(self):
        result = self.es.indices.get_mapping(index=self.constants.CSEindex, doc_type='file_meta_data')
        pprint(result)

    def delete_indice(self):
        self.es.indices.delete(index=self.constants.CSEindex)

    def file_metadocs_insertion(self, file_name):
        with open(file_name) as f:
            data = json.load(f)
            #pprint(data)
        helpers.bulk(self.es, data, request_timeout=30)
        return

    def match_search(self, tc_name_keyword):
        res = self.es.search(index=self.constants.CSEindex, body={'from': 0, 'size': 0, 'query':{'match': {'name': tc_name_keyword}} })
        return res

    def tag_search(self, list_of_term_query_with_clause):
        res = self.es.search(index=self.constants.CSEindex, body={'query' :{'constant_score' : {'filter' : { "bool" : list_of_term_query_with_clause}}}})
        return res

    def context_search(self, _query):
        res = self.es.search(index=self.constants.CSEindex, doc_type="file_meta_data", body={ "query": { "nested": { "path": "text_content", "query": { "bool": { "must": [{ "match": { "text_content.content":  _query}}]}},"inner_hits":{}}}})
        return res

    def match_phrase_search(self, name_keyword):
        res = self.es.search(index=self.constants.CSEindex, body={'from': 0, 'size': 0, 'query':{'match_phrase': {'name': name_keyword}} })
        return res

    def match_term_search(self, name_keyword):
        res = self.es.search(index=self.constants.CSEindex, body={'from': 0, 'size': 0, 'query':{'term': {'name': name_keyword}} })
        return res