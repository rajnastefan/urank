import os
import PyPDF2 as p2
import dash
import dash_core_components as dcc
import dash_html_components as html
import pdfplumber
# from search import UserInput
from dash.dependencies import Input, Output
import base64
import fitz
import io

from pdf2image import convert_from_path, convert_from_bytes



app = dash.Dash()
app.title = "uRank"

pdf_dict = {}
# indexer_and_searcher = UserInput()

lista = {
  "c++ guide": {
    # "pdfs"
    "keywords": {
      "C++": 300,
      "sql": 0,
      "nvidia": 50,
      "testna rijec": 290
    }
  },
  "sql guide": {
    "keywords": {
      "C++": 300,
      "sql": 1,
      "nvidia": 50,
      "testna rijec": 290
    }
  },
  "nvidia gpu": {
    "keywords": {
      "C++": 300,
      "sql": 5,
      "nvidia": 50,
      "testna rijec": 290
    }
  }
}

only_keywords = []
frequency_of_keywords = []
topics = ['Doc 1', 'Doc 2', 'Doc 3', 'Doc 4', 'Doc 5']

for x, y in lista.items():
  only_keywords = y.get('keywords')

for x, y in only_keywords.items():
  frequency_of_keywords.append(y)


def highlight_text_in_pdf(filename, words):
  doc = fitz.open(filename)
  for page in doc:
    for word in words:
      text_instance = page.searchFor(word)
      if (text_instance):
        for inst in text_instance:
          highlight = page.addHighlightAnnot(inst)

  doc.save(os.path.join(filename.split("/")[0], filename.split("/")[1], "output_" + filename.split("/")[2]), garbage=4, deflate=True, clean=True)


def select_topics(topic):
  # indexer_and_searcher.select_topic(topic)
  # print('test: ', indexer_and_searcher.pdf_dict)

  indexer_and_searcher.index_files(topic)


def add_new_keyword(keyword):
  indexer_and_searcher.fill_term_list(keyword)
  indexer_and_searcher.search_files()
  print("found results: ")
  print(indexer_and_searcher.found_pdfs)


def search_based_on_keyword():
  print("usla sam ?")
  for keyword in indexer_and_searcher.list_of_terms:
    print("usla sam 2?")
    for x, y in indexer_and_searcher.pdf_dict.items():
      print("usla sam 3?")

      print("keyword: " + keyword)
      print("y: " + str(y))
      if keyword in y:
        print('Ime fajla ->', x)


for x, y in pdf_dict.items():
  #    test.fill_term_list(y)
  print(x, y)


def choose_words(value):
  print(value)
  if value == 'nVidia GPU':
    return [
      {'label': 'C++ Books', 'value': 'C++ Books'},
      {'label': 'SQL Books', 'value': 'SQL Books'},
      {'label': 'nVidia GPU', 'value': 'nVidia GPU'}
    ]
  else:
    return []



#######################
# FRONTEND
#######################
print("")
app.layout = \
  html.Div(className="big_container", children=[
    html.Title("uRank"),
    html.Div(className="words", children=[
      html.P('Choose a topic'),
      # html.Br(),
      # html.Br(),
      dcc.Dropdown(
        id='topic-dropdown',
        options=[
          {'label': 'C++ Books', 'value': 'C++ Books'},
          {'label': 'SQL Books', 'value': 'SQL Books'},
          {'label': 'nVidia GPU', 'value': 'nVidia GPU'}
        ],
        style=dict(
                    horizontalAlign="left",
                    verticalAlign="middle"
                )
      ),
      html.P('Choose a words'),
      dcc.Input(
        id="input_search",
        type="search",
        value="nvidia",
        placeholder="input word",
      ),
      html.Button('Submit', id='submit-val', n_clicks=0),
    ]),

    html.Div(className="middle_field", children=[
      html.Div(id="test1"),
      html.Div(id="histogram", className="results", children=[
        dcc.Tabs([
              dcc.Tab(label=topics[0], children=[
                dcc.Graph(
                  figure={
                    'data': [
                      dict(
                        x=4,
                        y=[y],
                        type='bar',
                        text=name,
                        name=name
                      ) for y, name in zip(frequency_of_keywords, only_keywords.keys())
                    ],
                    'layout': {
                      'title': 'C++'
                    }
                  }
                ),
                html.Button('View', id='view_' + topics[0], n_clicks=0),
              ]),
          dcc.Tab(label=topics[1], children=[
            dcc.Graph(
              figure={
                'data': [
                  dict(
                    x=4,
                    y=[y],
                    type='bar',
                    text=name,
                    name=name
                  ) for y, name in zip(frequency_of_keywords, only_keywords.keys())
                ],
                'layout': {
                  'title': 'C++'
                }
              }
            ),
            html.Button('View', id='view_' + topics[1], n_clicks=0),
          ]),
          dcc.Tab(label=topics[2], children=[
            dcc.Graph(
              figure={
                'data': [
                  dict(
                    x=4,
                    y=[y],
                    type='bar',
                    text=name,
                    name=name
                  ) for y, name in zip(frequency_of_keywords, only_keywords.keys())
                ],
                'layout': {
                  'title': 'C++'
                }
              }
            ),
            html.Button('View', id='view_' + topics[2], n_clicks=0),
          ])
          ])

      ])
    ]),

    html.Div(className="bookmark_history", children=[
      html.Div(className="bookmark", children=[
        html.P("Bookmarks D")
      ], style={"border": "1px solid black"}),
      html.Div(className="history", children=[
        html.P("History E")
      ], style={"border": "1px solid black"})
    ])
  ])

@app.callback(
  Output(component_id='test1', component_property='children'),
  [Input(component_id='input_search', component_property='value'),
   Input(component_id='view_' + topics[0], component_property='n_clicks')])
def open_pdf(value, n_clicks):
  if(n_clicks > 0):
    highlight_text_in_pdf("topics/tema1/NVIDIA - Turing GPU Architecture - Graphics Reinveted.pdf", [value])
    os.startfile(r"C:\Users\rajna\Documents\urank\topics\tema1\output_NVIDIA - Turing GPU Architecture - Graphics Reinveted.pdf")
    n_clicks = 0

#
# @app.callback(
#   Output(component_id='histogram', component_property='children'),
#   [Input(component_id='input_search', component_property='value')])
# def make_plot(value):
#   print("Dropdown", value)
#   if value != None:
#     return
#   else:
#     return None

if __name__ == '__main__':
  ## select_topics("tema1")
  # add_new_keyword("Nvidia")
  app.run_server(debug=False, port=8090)