import pdfplumber
import subprocess
import os
import re
import PyPDF2
import base64
import json
from elasticsearch import Elasticsearch
from tika import parser

CURRENT_LIMIT_OF_PAGES = 50
STARTING_PAGE = 21


class UserInput:
  bookmarkes = []
  list_of_terms = []
  pdf_dict = {}
  topic = None
  found_pdfs = {}
  pdf_indexes = {}
  es = Elasticsearch([{'host':'localhost','port':9200}])
  print(es.cat.health())

  body = {
    "description": "Extract attachment information",
    "processors": [
      {
        "attachment": {
          "field": "data"
        }
      }
    ]
  }
  es.index(index='_ingest', doc_type='pipeline', id='attachment', body=body)


  def __init__(self):
    self.bookmarkes = []
    self.list_of_terms = []
    self.pdf_indexes = {}
    self.found_pdfs = {}
    self.topic = None

  #----------------new implementation------------------------------------------------#
  def get_all_bookmarks(self):
    print("test")
    bookmarks = []
    if not(self.check_first_index()):
      return []
    else:
      last = False
      count = 1
      while (not last):
        print(count)
        current_index = "bookmark_index_" + str(count)
        if (self.es.indices.exists(index=current_index)):
          doc = self.es.get(index=current_index, doc_type='my_type', id=current_index)
          bookmarks.append(doc['_source']['attachment']['content'])
          count = count + 1
        else:
          last = True

    return bookmarks

  def index_bookmarks(self, bookmark):
    if (self.check_first_index()):
      index_value = self.get_last_index()
      print(index_value)
    else:
      index_value = 1

    content = {"bookmark": bookmark}
    json_data = json.dumps(content)
    bytes_string = bytes(json_data, 'utf-8')
    data = base64.b64encode(bytes_string).decode('ascii')

    new_index = 'bookmark_index_' + str(index_value)
    print(new_index)
    self.es.index(id=new_index, index=new_index, doc_type='my_type', pipeline='attachment', refresh=True, body = {'data': data})



  def check_first_index(self):
    if(self.es.indices.exists(index="bookmark_index_1")):
      return True
    else:
      return False

  def get_last_index(self):
    last = False
    count = 1
    while (not last):
      if (self.es.indices.exists(index="bookmark_index_" + str(count))):
        count = count + 1
      else:
        last = True

    return count


  def pdf_operations(self, filename):
      pdf_text = parser.from_file(filename)

      # create a JSON string from the dictionary
      json_data = json.dumps(pdf_text)
      #print(json_data)

      # convert JSON string to bytes-like obj
      bytes_string = bytes(json_data, 'utf-8')

      # convert bytes to base64 encoded string
      return base64.b64encode(bytes_string).decode('ascii')


  def parse_pdf(self, filename):
    try:
      content = subprocess.check_output(["pdftotext", '-enc', 'UTF-8', filename, "-"])
    except subprocess.CalledProcessError as e:
      print('Skipping {} (pdftotext returned status {})'.format(filename, e.returncode))
      return None
    return base64.b64encode(content).decode('ascii')

  def index_files(self):
    themes = [ f.path for f in os.scandir("topics") if f.is_dir() ]

    for theme in themes:
      input_dir = os.path.join(os.getcwd(), theme)
      index_value = 0

      for file in os.listdir(input_dir):
        content = self.pdf_operations(os.path.join(theme, file))
        index_value = index_value + 1
        new_index = theme.split(theme[6])[1] + '_index_' + str(index_value)
        self.es.index(id = new_index, index=new_index, doc_type='my_type', pipeline='attachment', refresh=True, body={"data": content})

  def prepare_indexes_for_searching(self, topic):
    self.topic = topic
    directory = "topics/" + topic
    input_dir = os.path.join(os.getcwd(), directory)

    index_number = 0
    for file in os.listdir(input_dir):
      index_number = index_number + 1
      index = topic + "_index_" + str(index_number)
      self.pdf_indexes.update({file: index})


  def search_files(self):
    for keyword in self.list_of_terms:
      for file_name, current_index in self.pdf_indexes.items():
        self.es.indices.refresh(index=current_index)
        search = self.es.search(index=current_index, doc_type='my_type', q=keyword)
        if(search['hits']['max_score'] != None):
          doc = self.es.get(index=current_index, doc_type='my_type', id=current_index)
          word_count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(keyword), doc['_source']['attachment']['content'], re.IGNORECASE))
          if(word_count != 0):
            self.set_output(word_count, file_name, keyword)

    print("found pdfs: ")
    print(self.found_pdfs)
  def set_output(self, word_count, file_name, keyword):
    if(len(self.found_pdfs) == 0):
        temp_dict = {file_name: {'keywords': {}}}
        temp_dict[file_name]['keywords'] = {keyword: word_count}
        self.found_pdfs.update(temp_dict)
    else:
        if(file_name in self.found_pdfs):
            self.found_pdfs[file_name]['keywords'][keyword] = word_count
        else:
            temp_dict = {file_name: {'keywords': {}}}
            temp_dict[file_name]['keywords'] = {keyword: word_count}
            self.found_pdfs.update(temp_dict)

  #################################################################################


  #---------------old implementation------------------------------#
  def select_topic(self, topics):
    self.topics = topics
    self.list_of_terms = []
    self.open_file(topics)

  def fill_term_list(self, keywords):
    self.list_of_terms.append(keywords)
    #print("List " + self.list_of_terms)

  def extract_and_print_text(self, pdf):
    counter = STARTING_PAGE
    all_words = []
    while counter < CURRENT_LIMIT_OF_PAGES:
      page = pdf.pages[counter]
      text = page.extract_text()
      words_from_text = text.split()
      # print(words_from_text)
      all_words.append(words_from_text)
      counter = counter + 1
    return all_words

  def open_file(self, topic_directory):
    input_dir = os.path.join(os.getcwd(),  "topics",  topic_directory)
    for file in os.listdir(input_dir):
      if file[-4:] == ".pdf":
        try:
          path_to_file = os.path.join(input_dir, file)
          print(path_to_file)
          pdf = pdfplumber.open(path_to_file)
          list_of_words = self.extract_and_print_text(pdf)
          self.pdf_dict.update({file: list_of_words})
        except:
          print("[ERROR] loading " + file)

  def extract_words(self, path_to_file):
    pdf = pdfplumber.open("topics/thema1/" + path_to_file)
    list_of_words = self.extract_and_print_text(pdf)
    return list_of_words
  #################################################################################
