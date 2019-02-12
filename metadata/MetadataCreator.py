#!/usr/bin/env python
# coding: utf-8

import os, json
from . import CSEfilesScanner as cse
from . import constants
from classifier import PreProcessor as pp
import nltk

class MetadataCreator:
    output_directory = ''
    output_filename = 'fList.json'
    data_directory = ''
    metadata_directory = ''
    img_dir = ''
    
    def __init__(self, output_directory, data_directory, metadata_directory, img_dir):
        self.output_directory = output_directory
        self.data_directory = data_directory
        self.metadata_directory = metadata_directory
        self.img_dir = img_dir
    
    def read_file(self, file_path, extension):
        method_map = {".pdf" : cse.readPDF, ".doc" : cse.readDOCX, ".docx" : cse.readDOCX, ".xls" : cse.readEXCEL,
                      ".xlsx" : cse.readEXCEL, ".csv" : cse.readCSV, ".txt" : cse.readTXT, ".pptx" : cse.readPPTX}
        return '{} {}'.format(method_map[extension](file_path), file_path)
    
    def extractImages(self, file_path, extension, output_dir, img_dir):
        method_map = {".pdf" : cse.extractPDFImages, ".docx" : cse.extractDOCXandPPTXImages, ".pptx" : cse.extractDOCXandPPTXImages,
                      ".xls" : cse.extractXLS, ".xlsx" : cse.extractXLSX}
        return method_map[extension](file_path, output_dir, img_dir)

    def write_json(self, file_path, data_dict, **json_properties):
        with open(file_path, "w") as file:
            file.write(json.dumps(data_dict, **json_properties))
    
    def generate_files_metadata(self):
        extension_list = [".pdf", ".doc", ".docx", ".csv", ".xls", ".xlsx", ".pptx"]
        metadata = {}
        for (path, dirs, files) in os.walk(self.data_directory):
            for file in files:
                extension = os.path.splitext(file)[1].lower()
                if extension in extension_list and r'~' not in file:
                    abs_path = os.path.join(path, file)
                    underscored_abs_path = abs_path.replace(os.sep, "_").replace(':', '_').replace(' ', '_').replace('-', '_').replace('.', '_')
                    #os.path.splitext(abs_path)[0]
                    print('metadata created for {}!'.format(file))
                    metadata[underscored_abs_path] = {"abs_path" : abs_path, "filename" : file, "modified_time" : os.path.getmtime(abs_path)}
                    text_content = self.read_file(abs_path, extension)
                    _tokenized_text_content = nltk.sent_tokenize(text_content)
                    count = 0
                    sentence_list = []
                    for tc in _tokenized_text_content:
                        sentence_list.append({'section' : count, 'content': tc})
                        count = count + 1
                    file_metadata = {**metadata[underscored_abs_path], "extension" : extension, "tags" : pp.getFilteredContent(text_content), "text_content" : sentence_list, "images": self.extractImages(abs_path, extension, self.output_directory, self.img_dir)}
                    file_metadata = {"_index": constants.CSEindex, "_type": constants.CSEdoc_type, "id": underscored_abs_path, "_source": file_metadata}
                    self.write_json(os.path.join(self.metadata_directory, underscored_abs_path + ".json"), [file_metadata], sort_keys=True, indent=4)
        self.write_json(os.path.join(self.output_directory, self.output_filename), metadata, sort_keys=True, indent=4)