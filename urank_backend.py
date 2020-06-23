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
  bookmark_indexes = []
  bookmarkes = []
  list_of_terms = []
  pdf_dict = {}
  topic = None
  found_pdfs = {}
  pdfs_with_most_occured_words = {}
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
    self.bookmark_indexes = []
    self.list_of_terms = []
    self.pdf_indexes = {}
    self.found_pdfs = {}
    self.pdfs_with_most_occured_words = {}
    self.topic = None
    self.list_of_found_words = []

  #----------------new implementation------------------------------------------------#

  def clear_searched_words(self, keyword):
    temp_found_pdfs = {}
    for file_name, value in self.found_pdfs.items():
      for keyword_it, values in value.items():
        for word, count in values.items():
          if(word != keyword):
            if(file_name not in temp_found_pdfs.keys()):
              temp_dict = {file_name: {'keywords': {}}}
              temp_dict[file_name]['keywords'] = {word: count}
              temp_found_pdfs.update(temp_dict)
            else:
              temp_found_pdfs[file_name]['keywords'][word] = count

    self.found_pdfs = temp_found_pdfs

  def clear_bookmarks_indices(self):
    for bookmark in  self.bookmark_indexes:
      self.es.delete(id = bookmark, index=bookmark, doc_type='my_type')
      self.es.indices.delete(index=bookmark, ignore=[400, 404])
      self.bookmarkes = []
      self.bookmark_indexes = []

  def init_bookmarks(self):
    self.bookmarkes, self.bookmark_indexes = self.get_all_bookmarks()


  def get_all_bookmarks(self):
    bookmarks = []
    bookmarks_indexes = []
    if not(self.check_first_index()):
      return [], []
    else:
      last = False
      count = 1
      while (not last):
        current_index = "bookmark_index_" + str(count)
        if (self.es.indices.exists(index=current_index)):
          doc = self.es.get(index=current_index, id=current_index)
          json_string = json.loads(doc['_source']['attachment']['content'])
          bookmarks.append(json_string['bookmark'])
          #print(doc['_source']['attachment']['content'])
          bookmarks_indexes.append(current_index)
          count = count + 1
        else:
          last = True

    return bookmarks, bookmarks_indexes

  def index_bookmark(self, bookmark):
    if (self.check_first_index()):
      index_value = self.get_last_index()
      #print(index_value)
    else:
      index_value = 1

    content = {"bookmark": bookmark}
    json_data = json.dumps(content)
    bytes_string = bytes(json_data, 'utf-8')
    data = base64.b64encode(bytes_string).decode('ascii')

    new_index = 'bookmark_index_' + str(index_value)
    self.bookmark_indexes.append(new_index)
    self.bookmarkes.append(bookmark)
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


  def search_files(self, keyword):

    temp_dictionary = {}
    #for keyword in self.list_of_terms:
    for file_name, current_index in self.pdf_indexes.items():
      self.es.indices.refresh(index=current_index)
      search = self.es.search(index=current_index, doc_type='my_type', q=keyword)
      if(search['hits']['max_score'] != None):
        doc = self.es.get(index=current_index, doc_type='my_type', id=current_index)
        word_count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(keyword), doc['_source']['attachment']['content'], re.IGNORECASE))
        if(word_count != 0):
          temp_dict = self.set_output(word_count, file_name, keyword)
          temp_dictionary.update(temp_dict)
          if keyword not in self.list_of_found_words:
              self.list_of_found_words.append(keyword)


    #self.set_most_occured_words(temp_dictionary, keyword, word_count)

    #print("top pdfs: ")
    #print(self.pdfs_with_most_occured_words)


  def set_output(self, word_count, file_name, keyword):
    temp_dict = {file_name: {'keywords': {}}}
    if(len(self.found_pdfs) == 0):
        temp_dict[file_name]['keywords'] = {keyword: word_count}
        self.found_pdfs.update(temp_dict)
    else:
        if(file_name in self.found_pdfs):
            self.found_pdfs[file_name]['keywords'][keyword] = word_count
            temp_dict[file_name]['keywords'] = {keyword: word_count}
        else:
            temp_dict[file_name]['keywords'] = {keyword: word_count}
            self.found_pdfs.update(temp_dict)

    return temp_dict

  def set_most_occured_words(self, temp_dictionary, keyword, word_count):
    if (len(temp_dictionary) > 0):
      temporary_dictionary, file_key = self.find_most_occured_words(temp_dictionary)
      if (len(temporary_dictionary) > 0):
        if (file_key in self.pdfs_with_most_occured_words.keys()):
          self.pdfs_with_most_occured_words[file_key]['keywords'][keyword] = word_count
        else:
          self.pdfs_with_most_occured_words.update(temporary_dictionary)


  def find_most_occured_words(self, temp_dict):

    word_to_insert = None
    count_to_insert = None
    file_to_insert = None

    prev_count = 0
    for pdf, pdf_key in temp_dict.items():
      for keywords, values in pdf_key.items():
        for word, count in values.items():
          if(count > prev_count):
            word_to_insert = word
            count_to_insert = count
            file_to_insert = pdf
            prev_count = count

    temp_dict = {file_to_insert: {'keywords': {}}}
    temp_dict[file_to_insert]['keywords'] = {word_to_insert: count_to_insert}
    return temp_dict, file_to_insert


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
          #print(path_to_file)
          pdf = pdfplumber.open(path_to_file)
          list_of_words = self.extract_and_print_text(pdf)
          self.pdf_dict.update({file: list_of_words})
        except:
          print("[ERROR] loading " + file)

  def extract_words(self, path_to_file):
    pdf = pdfplumber.open("topics/gpu/" + path_to_file)
    list_of_words = self.extract_and_print_text(pdf)
    return list_of_words
  #################################################################################