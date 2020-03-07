from metadata import metadata_generator
from metadata import constants
from classifier import create_naive_bayes_model as NBM
from indexing import tag_search
from indexing import context_search
from api import elastic_search
import os, sys
import nltk
from elasticsearch import Elasticsearch

class Initialize:
    main_pkg_dir = ''
    output_dir = ''
    metadata_dir = ''
    data_dir = ''
    
    def __init__(self, main_pkg_dir):
        self.main_pkg_dir = main_pkg_dir
        self.output_dir =  os.path.join(main_pkg_dir, 'output')
        self.data_dir = os.path.join(main_pkg_dir, 'data')
        self.metadata_dir = os.path.join(self.output_dir, 'metadatas')
        self.es_response_dir = os.path.join(self.output_dir, 'es_response')
        self.img_dir = os.path.join(self.output_dir, 'img_dir')
        if not os.path.exists(self.es_response_dir):
            os.makedirs(self.es_response_dir)
        if not os.path.exists(self.metadata_dir):
            os.makedirs(self.metadata_dir)
        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)
        try:
            nltk.download('averaged_perceptron_tagger')
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            nltk.download("stopwords")

    
    def es_indexing(self, fi, es):
        if not es.indices.exists(index=constants.CSEindex):
            fi.create_indice()
        else:
          while True:
              choice = input('Would you like to clean the es and a fresh start?{Y or N}')
              if(choice == 'Y'):
                break
              elif(choice == 'N'):
                return
              else:
                print('Wrong input!')
        fi.delete_indice()
        fi.create_indice()
        #sys.exit(0)
        for (root, dirs, filenames) in os.walk(self.metadata_dir):
            count = 0
            print('total metadata to upload: {}'.format(len(filenames)))
            for fname in filenames:
                print(count)
                fi.file_metadocs_insertion(os.path.join(self.metadata_dir, fname))
                count = count+1
            break
        #fi.create_mapping()
        #pprint(fi.es.search(index='cse',  doc_type='file_meta_data',
    
    def metadata_creation(self):
        md_c = metadata_generator.MetadataGenerator(self.output_dir, self.data_dir, self.metadata_dir, self.img_dir)
        if not os.listdir(self.metadata_dir): 
            md_c.generate_files_metadata()
    
    def _tag_search(self, es_obj):
        ts = tag_search.TagSearch(es_obj, self.es_response_dir)
        ts.tag_query()
    
    def _context_search(self, es_obj):
        ts = context_search.ContextSearch(es_obj, self.es_response_dir)
        ts.context_based_query()
    
    def model_creation():
        pass

if __name__ == '__main__':
    main_pkg_dir = os.path.dirname(os.path.abspath(__file__))
    init = Initialize(main_pkg_dir)
    init.metadata_creation()
    
    es = Elasticsearch(
        scheme="http",
        port=9200,
        http_auth=(constants.es_username, constants.es_password)
    )
    fi = elastic_search.FileIndex(es, constants)
    init.es_indexing(fi, es)
    #init._tag_search(fi)
    init._context_search(fi)
