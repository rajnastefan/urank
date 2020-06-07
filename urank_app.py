import os
import PyPDF2 as p2
import dash
import dash_core_components as dcc
import dash_html_components as html
import pdfplumber
from search import UserInput

from dash.dependencies import Input, Output

app = dash.Dash()
app.title = "uRank"

pdf_dict = {}
indexer_and_searcher = UserInput()


def select_topics(topic):
    #test.select_topic(topic)
    #print('mala kurcina', test.pdf_dict)

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
              dcc.Dropdown(
                  id='words-dropdown',
                   #funkcija koja ce sadrzati rijeci
                  multi=True
              ),
          ], style={"border": "1px solid black"}),

    html.Div(className="middle_field", children=[
      html.Div(className="documents", children=[
        html.P("Documents B"),
          html.Div(id="test")
      ], style={"border": "1px solid black"}),
      html.Div(className="results", children=[
        html.P("Histogram C")
      ], style={"border": "1px solid black"})
    ], style={"border": "1px solid black"}),

    html.Div(className="bookmark_history", children=[
      html.Div(className="bookmark", children=[
        html.P("Bookmarks D")
      ], style={"border": "1px solid black"}),
      html.Div(className="history", children=[
        html.P("History E")
      ], style={"border": "1px solid black"})
    ], style={"border": "1px solid black"})
  ])
#######################


@app.callback(
    Output(component_id='words-dropdown', component_property='options'),
    [Input(component_id='topic-dropdown', component_property='value')])
def update_df(value):
    return choose_words(value)


@app.callback(
    Output(component_id='test', component_property='children'),
    [Input(component_id='words-dropdown', component_property='value')])
def update_df(value):
    return [html.P(value), html.P(value), html.P(value),html.P(value),html.P(value),html.P(value)]



def main():
    print("pozvo prva")
    print("pozvo select topics")

if __name__ == '__main__':
    # select_topics("tema1")
    # add_new_keyword("Nvidia")
    app.run_server(debug=False, port=8090)

