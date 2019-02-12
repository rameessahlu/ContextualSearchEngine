import json, os, random
import time, datetime
from classifier import PreProcessor as pp
from . import common as c

class ContextSearch:
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
    
    def context_based_query(self):
     while True:
        query = input('Enter a string for query: ')
        _relavance_score = self.fi_obj.context_search(query)
        self.log_es_response(_relavance_score)
        #print(self.fi_obj.tag_search(sub_query_list))
