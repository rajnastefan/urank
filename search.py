import os
import pdfplumber

CURRENT_LIMIT_OF_PAGES = 50
STARTING_PAGE = 21


class UserInput:
  list_of_terms = []
  pdf_dict = {}


  def __init__(self):
    self.list_of_terms = []
    #self.pdf_dict = []

  def select_topic(self, topics):
    self.topics = topics
    self.list_of_terms = []
    self.open_file(topics)

  def fill_term_list(self, keywords):
    self.list_of_terms.append(keywords)
    #print("List " + self.list_of_terms)

  def extract_and_print_text(self, pdf):
    counter = STARTING_PAGE
    while counter < CURRENT_LIMIT_OF_PAGES:
      page = pdf.pages[counter]
      text = page.extract_text()
      words_from_text = text.split()
      # print(words_from_text)
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
