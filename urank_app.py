import dash
import dash_core_components as dcc
import dash_html_components as html
import pdfplumber
from search import UserInput
from dash.dependencies import Input, Output
import fitz
import io
import os

app = dash.Dash()
app.title = "uRank"

pdf_dict = {}
indexer_and_searcher = UserInput()

lista = {
  "c++ guide": {
    "keywords": {
      "C++": 300,
      "sql": 0,
      "nvidia": 50
    }
  },
  "sql guide": {
    "keywords": {
      "C++": 300,
      "sql": 0,
      "nvidia": 50
    }
  },
  "nvidia gpu": {
    "keywords": {
      "C++": 300,
      "sql": 0,
      "nvidia": 50
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
  indexer_and_searcher.prepare_indexes_for_searching(topic)


def add_new_keyword(keyword):
  indexer_and_searcher.fill_term_list(keyword)
  indexer_and_searcher.search_files()
  print("found results: ")
  print(indexer_and_searcher.found_pdfs)



def update_plot(topic):
  return html.Div([
    dcc.Graph(
      id='example-graph',
      figure={
        'data': [
          dict(
            x=[1, 2, 3],
            y=[4, 1, 2],
            type='bar',
            text=y.get("keyword"),
            name=topic
          ) for i, y in lista.items()
          # {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
          # {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
        ],
        'layout': {
          'title': 'Dash Data Visualization'
        }
      }
    )
  ])


topics = ['Doc 1', 'Doc 2']

#######################
# FRONTEND
#######################
print("")
app.layout = \
  html.Div(className="big_container", children=[
    html.Title("uRank"),
    html.Div(className="topic", children=[
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
      ),
    ], style={"border": "1px solid black"}),
    html.Div(className="words", children=[
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


if __name__ == '__main__':
  app.run_server(debug=False)
