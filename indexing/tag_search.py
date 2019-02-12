import json, os, random
import time, datetime
from classifier import PreProcessor as pp
from . import common as c

class TagSearch:
    fi_obj = None
    def __init__(self, fi, es_response_dir):
        self.fi_obj = fi
        self.es_response_dir = es_response_dir
    
    def log_es_response(self, _relavance_score):
        log_file_name = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
        salt  = str(random.randint(1, 1000))
        print('DEBUG# random_no: {}'.format(salt))
        with open(os.path.join(self.es_response_dir, log_file_name + salt + r'.json'), "w") as file:
            file.write(json.dumps(_relavance_score, sort_keys=True, indent=4))
        return
    
    def tag_query(self):
     while True:
        query = input('Enter a string for query: ')
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
            sub_query_list = c.createSubQueryList(tokens, tt_n_c[0], tt_n_c[1])
            if len(sub_query_list[tt_n_c[1]]) != 0:
                _relavance_score = self.fi_obj.tag_search(sub_query_list)
                if len(_relavance_score['hits']['hits']) > 0:
                    self.log_es_response(_relavance_score)
                    break
        #print(self.fi_obj.tag_search(sub_query_list))
