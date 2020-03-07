import os
import sys
import json
import shutil
from elasticsearch import Elasticsearch
from api import elastic_search
from metadata import CSEfiles_scanner as cse
from classifier import pre_processor as pp
from metadata import constants
import nltk
import time


class MetaMonitor:
    meta_folder = ''
    jfile_path = ''
    data_folder = ''
    img_dir = ''
    CSEindex = 'cse'
    CSEdoc_type = 'file_meta_data'

    def __init__(self, meta_folder, jfile, data, img_dir):
        self.meta_folder = meta_folder
        self.img_dir = img_dir
        self.jfile_path = jfile
        self.data_folder = data

    def scanMetaFile(self):

        try:
            extension_list = [".pdf", ".doc", ".docx", ".csv", ".xls", ".xlsx", ".txt", ".pptx"]

            with open(self.jfile_path, 'r') as jfile:
                flist = json.load(jfile)

            for (path, dirs, files) in os.walk(self.data_folder):
                for fe in files:
                    if os.path.splitext(fe)[1] in extension_list and r'~' not in fe:
                        # ele = {"wholepath": os.path.join(path, f), "mtime": os.path.getmtime(os.path.join(path, f))}

                        fpath = os.path.join(path, fe);
                        # addnew = False
                        # for f in flist:
                        #     if fpath == flist[f]['abs_path']:
                        #         addnew = False
                        #         break
                        #     else:
                        #         addnew = True
                        if self.getFilteredPath(fpath, False) not in flist:
                            flist[self.getFilteredPath(fpath, False)] = {'abs_path': fpath, 'filename': fe,
                                                                         'modified_time': os.path.getmtime(fpath)}
                            # flist.append(f)
            templist = []
            index = 0
            for f in flist:
                print("Working on: %s" % flist[f]['abs_path'])
                if os.path.exists(flist[f]['abs_path']):
                    # print(self.meta_folder + "\\" + self.getFilteredPath(f['wholepath']))
                    if os.path.exists(self.meta_folder + "\\" + self.getFilteredPath(flist[f]['abs_path'])):
                        stime = flist[f]['modified_time']
                        mtime = os.path.getmtime(flist[f]['abs_path'])
                        if stime == mtime:
                            continue
                        else:
                            print("Updating File: %s" % flist[f]['abs_path'])
                            flist[f]['modified_time'] = os.path.getmtime(flist[f]['abs_path'])
                            if not self.updateJFile(flist[f]):
                                print("Error occurred while updating")
                    else:
                        print("Updating: %s" % flist[f]['abs_path'])
                        if not self.updateJFile(flist[f]):
                            print("Error occurred while updating")
                else:
                    print("Deleting: %s" % flist[f]['abs_path'])
                    self.deleteJFile(flist[f])
                    # flist.pop([f])
                    templist.append(f)

            for f in templist:
                del flist[f]

            with open(self.jfile_path, 'w') as jFile:
                json.dump(flist, jFile)

            self.reinitialization()
        except FileNotFoundError as e:
            print(str(e))

    def updateJFile(self, file):
        # extension_list = {".pdf": readPDF, ".doc": readDOCX, ".docx": readDOCX, ".csv": readCSV, ".xls": readEXCEL,".xlsx": readEXCEL, ".txt": readTXT, ".pptx": readPPTX}
        extension_list = [".pdf", ".doc", ".docx", ".csv", ".xls", ".xlsx", ".txt", ".pptx"]
        jfile = dict()

        jfile['_index'] = self.CSEindex
        jfile['_type'] = self.CSEdoc_type
        jfile['id'] = self.getFilteredPath(os.path.splitext(file['abs_path'])[0], False)

        source = dict()
        source['filename'] = file['filename']
        source['abs_path'] = file['abs_path']
        source['modified_time'] = file['modified_time']

        if os.path.splitext(file['abs_path'])[1].lower() in extension_list and r'~' not in file['abs_path']:
            source['extension'] = os.path.splitext(file['abs_path'])[1]

            text_content = self.read_file(file['abs_path'], os.path.splitext(file['abs_path'])[1])
            _tokenized_text_content = nltk.sent_tokenize(text_content)
            count = 0
            sentence_list = []
            for tc in _tokenized_text_content:
                sentence_list.append({'section': count, 'content': tc})
                count = count + 1

            source['tags'] = pp.getFilteredContent(text_content)

            source['text_content'] = sentence_list
            source['images'] = self.extractImages(file['abs_path'], os.path.splitext(file['abs_path'])[1],
                                                  self.meta_folder, self.img_dir)
            jfile['_source'] = source

            with open(os.path.join(self.meta_folder, self.getFilteredPath(file['abs_path'])), 'w') as jFile:
                json.dump([jfile], jFile)
            return True
        return False

    def deleteJFile(self, file):
        file_path = os.path.join(self.meta_folder, self.getFilteredPath(file['abs_path']))
        img_meta_folder = os.path.join(self.img_dir, self.getFilteredPath(file['abs_path'], False))
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
            else:
                print("File Not Found : %s" % file_path)
            if os.path.exists(img_meta_folder):
                shutil.rmtree(img_meta_folder)
            else:
                print('Folder Not Found : %s' % img_meta_folder)
        except Exception as e:
            print(str(e))

    def createSession(self):
        es = Elasticsearch(scheme="http", port=9200, )
        return elastic_search.FileIndex(es, constants)

    def reinitialization(self):
        main_pkg_dir = os.path.dirname(os.path.realpath(__file__))
        output_dir = os.path.join(main_pkg_dir, 'output')
        metadata_dir = os.path.join(output_dir, 'metadatas')
        fi_obj = self.createSession()
        fi_obj.delete_indice()
        fi_obj.create_indice()
        print(constants.CSEdoc_type)
        for (root, dirs, filenames) in os.walk(metadata_dir):
            for fname in filenames:
                print(os.path.join(metadata_dir, fname))
                fi_obj.file_metadocs_insertion(os.path.join(metadata_dir, fname))
            break

    def read_file(self, file_path, extension):
        method_map = {".pdf": cse.readPDF, ".doc": cse.readDOCX, ".docx": cse.readDOCX, ".xls": cse.readEXCEL,
                      ".xlsx": cse.readEXCEL, ".csv": cse.readCSV, ".txt": cse.readTXT, ".pptx": cse.readPPTX}
        return '{} {}'.format(method_map[extension](file_path), file_path)

    def extractImages(self, file_path, extension, output_dir, img_dir):
        method_map = {".pdf": cse.extractPDFImages, ".docx": cse.extractDOCXandPPTXImages,
                      ".pptx": cse.extractDOCXandPPTXImages,
                      ".xls": cse.extractXLS, ".xlsx": cse.extractXLSX}
        return method_map[extension](file_path, output_dir, img_dir)

    def getFilteredPath(self, file_name, ext=True):

        symbol = (os.sep, '\/', ':', '*', '?', '\"', '<', '>', '|', '.', ' ', '-')

        for s in symbol:
            file_name = file_name.replace(s, '_')

        if ext:
            return file_name + ".json"
        else:
            return file_name


if __name__ == "__main__":
    main_pkg_dir = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.join(main_pkg_dir, "output")
    monitor = MetaMonitor(os.path.join(output_dir, "metadatas"),
                          os.path.join(output_dir, "fList.json"),
                          os.path.join(main_pkg_dir, "data"),
                          os.path.join(output_dir, "img_dir"))
    for i in range(0,10):
        monitor.scanMetaFile()
        time.sleep(5*60)
