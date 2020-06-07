import os
import pdfplumber
import base64
import subprocess
import os
from elasticsearch import Elasticsearch


CURRENT_LIMIT_OF_PAGES = 50
STARTING_PAGE = 21


class UserInput:
  list_of_terms = []
  pdf_dict = {}

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
    self.list_of_terms = []
    self.pdf_indexes = {}
    self.found_pdfs = {}

  #----------------new implementation------------------------------------------------#

  def parse_pdf(self, filename):
    try:
      content = subprocess.check_output(["pdftotext", '-enc', 'UTF-8', filename, "-"])
    except subprocess.CalledProcessError as e:
      print('Skipping {} (pdftotext returned status {})'.format(filename, e.returncode))
      return None
    return base64.b64encode(content).decode('ascii')

  def index_files(self, topic):
    directory = "topics/" + topic
    input_dir = os.path.join(os.getcwd(), directory)

    index_value = 0

    for file in os.listdir(input_dir):
      content = self.parse_pdf(directory + "/" + file)
      index_value = index_value + 1
      new_index = 'my_index_' + str(index_value)
      current_index = self.es.index(index=new_index, doc_type='my_type', pipeline='attachment', refresh=True, body={'data': content})
      self.pdf_indexes.update({file: current_index})

  def search_files(self):
    for keyword in self.list_of_terms:
      for file_name, content in self.pdf_indexes.items():
        self.es.indices.refresh(index=content['_index'])
        search = self.es.search(index=content['_index'], doc_type='my_type', q=keyword)
        if(search['hits']['max_score'] != None):
          self.found_pdfs.update({file_name: self.extract_words(file_name)})


        #print(file_name)
        #print(search['hits']['max_score'])

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
    return words_from_text

  def open_file(self, topic_directory):
    # topic_directory = "topics\\" + topic_directory
    input_dir = os.path.join(os.getcwd(), topic_directory)
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
    pdf = pdfplumber.open("topics/tema1/" + path_to_file)
    list_of_words = self.extract_and_print_text(pdf)
    return list_of_words
  #################################################################################
