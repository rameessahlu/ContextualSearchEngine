## ContextualSearchEngine
Context based search Engine –  A context based search engine which can accept things from user and search the document, pdfs and provide closest description with highest matching values
![Design](https://github.com/rameessahlu/ContextualSearchEngine/blob/master/design.PNG)

Requirements:
* doc2text
* docx2txt
* PyMuPDF
* minecart
* xlrd
* pywin32
* nltk
* python-pptx
* flask_cors
* elasticsearch

Quick Instruction:
* install java-9
* install elasticsearch and set credential
* place documents of your choice on data folder
* on the command line, enter:
```console
   C:\Users\<user>\workspace>bin/elasticsearch.bat
   C:\Users\<user>\workspace>python initialize_search_index.py
   C:\Users\<user>\workspace>python web_service.py
```
* open /static_files/index.html
* Now it's ready to query!

Authors:
* Ramees Sahlu
* Abhishek Kumar
