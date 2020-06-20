import os
import PyPDF2 as p2
import dash
import dash_core_components as dcc
import dash_html_components as html
import pdfplumber
# from search import UserInput
from dash.dependencies import Input, Output


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

print("Frequency", frequency_of_keywords)
print("Keywords", only_keywords)


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
        placeholder="input word",
      )
    ]),

    html.Div(className="middle_field", children=[
      html.Div(className="documents", children=[
        html.P("Documents B"),
        html.Div(id="test")
      ], style={"border": "1px solid black"}),
      html.Div(id="histogram", className="results", children=[
        html.P("Histogram C"),
      ], style={"border": "1px solid black"})
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

for y, name in zip(frequency_of_keywords, only_keywords.keys()):
  print("y ->", y)
  print("name ->", name)


# for i,j in y.items():
# for k,l in j.items():
# print(j.keys())
# break
# print(k)
# print(l)
#######################


# @app.callback(
#   Output(component_id='words-dropdown', component_property='options'),
#   [Input(component_id='topic-dropdown', component_property='value')])
# def update_df(value):
#   return choose_words(value)

#
@app.callback(
  Output(component_id='test', component_property='children'),
  [Input(component_id='input_search', component_property='value')])
def update_df(value):
  return [html.P(value), html.P(value), html.P(value), html.P(value), html.P(value), html.P(value)]


@app.callback(
  Output(component_id='histogram', component_property='children'),
  [Input(component_id='words-dropdown', component_property='value')])
def make_plot(value):
  print("Dropdown", value)
  if value != None:
    return dcc.Tabs([
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
        )
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
        )
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
        )
      ]),
      dcc.Tab(label=topics[3], children=[
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
        )
      ]),
      dcc.Tab(label=topics[4], children=[
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
        )
      ]),
    ])
  else:
    return None


def main():
  print("pozvo prva")
  print("pozvo select topics")


if __name__ == '__main__':
  ## select_topics("tema1")
  # add_new_keyword("Nvidia")
  app.run_server(debug=False, port=8090)
