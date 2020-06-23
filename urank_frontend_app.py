import os
from time import sleep

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import fitz
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from urank_backend import UserInput
from utils import Utils

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "uRank"

pdf_dict = {}
indexer_and_searcher = UserInput()


def save_bookmarks(bookmark):
  # TODO connect with backend
  indexer_and_searcher.index_bookmark(bookmark)


def clear_bookmarks():
  # TODO connect with backend
  indexer_and_searcher.clear_bookmarks_indices()


def select_themas():
  return_list = []
  for subdir, dirs, files in os.walk("topics"):
    for dir in dirs:
      return_list.append({'label': dir, 'value': dir})

  return return_list

  # for key in indexer_and_searcher.found_pdfs.keys():
  #   list_tabs.append(
  #     dcc.Tab(label=key.split(".pd")[0], id=key.split(".pd")[0], value=key.split(".pd")[0], children=[
  #       dcc.Graph(
  #         figure={
  #           'data': [
  #             dict(
  #               x=1,
  #               y=[indexer_and_searcher.found_pdfs[key]["keywords"][name]],
  #               type='bar',
  #               text=name,
  #               name=name
  #             ) for name in indexer_and_searcher.found_pdfs[key]["keywords"]
  #           ],
  #           'layout': {
  #             'title': key.split(".pd")[0]
  #           }
  #         }
  #       )
  #     ]))
  # return list_tabs


def update_fig():
  list_tabs = []
  print("Lista rijeci", Utils.list_of_found_words)
  for key in Utils.list_of_found_words:
    counter = 1
    y = []
    x = []
    list_name = []
    for name in indexer_and_searcher.found_pdfs.keys():
      if key in indexer_and_searcher.found_pdfs[name]["keywords"]:
        y.append(indexer_and_searcher.found_pdfs[name]["keywords"][key])
        x.append(counter)
        list_name.append(name)
        counter += 1
    list_tabs.append(
      dcc.Tab(label=str(key), id=str(key), value=str(key), children=[
        dcc.Graph(
          figure={
            'data': [
              dict(
                x=x,
                y=y,
                type='scatter',
                text=list_name,
                name=list_name
              )  # for name in indexer_and_searcher.found_pdfs.keys()
            ],
            'layout': {
              'title': key
            }
          }
        )
      ]))

  return list_tabs


def highlight_text_in_pdf(filename, words):
  doc = fitz.open(filename)
  for page in doc:
    for word in words:
      text_instance = page.searchFor(word)
      if (text_instance):
        for inst in text_instance:
          highlight = page.addHighlightAnnot(inst)

  input_dir = os.path.join(os.getcwd(), "highlighted_pdfs/")
  doc.save(input_dir + os.path.join("output_" + filename.split("/")[2]), garbage=4,
           deflate=True, clean=True)


def select_topics(topic):
  indexer_and_searcher.prepare_indexes_for_searching(topic)


def add_new_keyword(keyword):
  indexer_and_searcher.fill_term_list(keyword)
  indexer_and_searcher.search_files(keyword)
  Utils.list_of_found_words = indexer_and_searcher.list_of_found_words
  # print("found results: ")
  # print(indexer_and_searcher.found_pdfs)


def update_graphs():
  list_tabs = []
  for key in indexer_and_searcher.found_pdfs.keys():
    list_tabs.append(
      dcc.Tab(label=key.split(".pd")[0], id=key.split(".pd")[0], value=key.split(".pd")[0], children=[
        dcc.Graph(
          figure={
            'data': [
              dict(
                x=1,
                y=[indexer_and_searcher.found_pdfs[key]["keywords"][name]],
                type='bar',
                text=name,
                name=name
              ) for name in indexer_and_searcher.found_pdfs[key]["keywords"]
            ],
            'layout': {
              'title': key.split(".pd")[0]
            }
          }
        )
      ]))
  return list_tabs


def select_themas():
  return_list = []
  for subdir, dirs, files in os.walk("topics"):
    for dir in dirs:
      return_list.append({'label': dir, 'value': dir})

  return return_list


def select_words():
  return_list = []
  for word in Utils.list_of_found_words:
    return_list.append({'label': word, 'value': word})
  return [dcc.Dropdown(
    id='words-dd',
    options=return_list,
    className='round-dropdown',
    value=Utils.list_of_found_words,
    multi=True,
    clearable=False
  )]


def open_pdf_test():
  print("usli")


#######################
# FRONTEND
#######################
app.layout = \
  html.Div(className="big_container", children=[
    html.Title("uRank"),

    html.Div(className="bookmark_history", children=[
      html.Div(className="bookmark", children=[
        html.H1('Choose a topic', className='center-header'),

        # html.Br(),
        dcc.Dropdown(
          id='topic-dropdown',
          options=select_themas(),
          className='round-dropdown'
        ),
      ]),
      html.Div(id="words_search", className="history", children=[
        html.H1('Type in words', className='center-header'),
        dcc.Input(
          id="input_search",
          type="search",
          placeholder="Search",
          className="search"
        ),
        html.I(id='submit_val', n_clicks=0, className='fi-page-search'),
        html.Br(),
        html.Div(id='words-dropdown', children=[
        ])
      ])
    ]),
    html.Div(className="middle_field", children=[
      html.Div(id="test1"),
      html.Div(id="test2"),
      html.Div(id="histogram", className="results", children=[
        dcc.Tabs(id="tabs", children=[
          dcc.Tab(label="Doc 1", children=[
            dcc.Graph(
              figure={
                'data': [
                ],
                'layout': {
                  'title': 'Dummy'
                }
              }
            )
          ])
        ]),
        html.Button('View', id='view', n_clicks=0),
        html.I(id='bookmark_doc_', n_clicks=0, className='fi-star'),
        html.Div(id="graph_div", children=[
          dcc.Tabs(id="tabs_scatter", children=[
            dcc.Tab(label="Doc 1", children=[
              dcc.Graph(
                figure={
                  'data': [
                  ],
                  'layout': {
                    'title': 'Dummy'
                  }
                }
              )
            ])
          ]),
        ])
      ]),
    ]),

    html.Div(className="bookmark_history", children=[
      html.Div(className="bookmark", children=[
        html.H1("Bookmarks", className='center-header'),
        html.Button('Clear bookmarks', id='clear_bookmark', className='clear-bookmark', n_clicks=0
                    ),
        html.Div(id="bookmark_list", children=[
          dbc.ListGroup(id="bookmark_group"
                        )
        ])

      ]),
      html.Div(id="his", className="history", children=[html.H1("History of words", className='center-header'),
                                                        html.Button('Clear history', id='clear_history',
                                                                    className='clear-history', n_clicks=0),
                                                        html.Div(id="history")])
    ])
  ])


# @app.callback(Output(component_id='his', component_property='children'),
#               [Input(component_id='bookmarks_nav', component_property='n_clicks')])
# def test_nav(*args):
#   print(args)

@app.callback(
  Output(component_id='bookmark_group', component_property='children'),
  [Input(component_id='tabs', component_property='value'),
   Input(component_id="bookmark_doc_", component_property='n_clicks'),
   Input(component_id='clear_bookmark', component_property='n_clicks'),
   Input(component_id='topic-dropdown', component_property='value')
   ],
)
def bookmark(value, n_clicks, n_clicks2, topic):
  if n_clicks2 > Utils.bookmark_click_count_clear:
    Utils.bookmarked_documents.clear()
    Utils.bookmark_click_count_clear = n_clicks2
    clear_bookmarks()
    return [html.P(doc) for doc in Utils.bookmarked_documents]
  if n_clicks > Utils.bookmark_click_count:
    if value is not None:
      if value not in Utils.bookmarked_documents:
        Utils.bookmarked_documents.append(value)
        save_bookmarks(value)
        Utils.bookmark_click_count = n_clicks
      return [dbc.ListGroupItem(html.A(doc, href='/assets/topics/' + topic + '/' + doc + '.pdf'),
                                className='rounded-bookmark') for doc in Utils.bookmarked_documents]
    elif value == "":
      return [dbc.ListGroupItem(html.A(doc, href='/assets/topics/' + topic + '/' + doc + '.pdf'),
                                className='rounded-bookmark') for doc in Utils.bookmarked_documents]
  else:
    return [
      dbc.ListGroupItem(html.A(doc, href='/assets/topics/' + topic + '/' + doc + '.pdf'), className='rounded-bookmark')
      for doc in Utils.bookmarked_documents]


@app.callback(
  Output(component_id='history', component_property='children'),
  [Input(component_id='input_search', component_property='value'),
   Input(component_id='submit_val', component_property='n_clicks'),
   Input(component_id='clear_history', component_property='n_clicks')])
def update_history(value, n_clicks, n_clicks2):
  if n_clicks2 > Utils.history_click_count:
    Utils.history_word.clear()
    Utils.history_click_count = n_clicks2
    return [html.P(word) for word in Utils.history_word]
  if n_clicks > Utils.click_count_temp:
    if value is not None:
      if value not in Utils.history_word:
        Utils.history_word.append(value)
      return [html.P(word, className='rounded-history') for word in Utils.history_word]
    elif value == "":
      return [html.P(word, className='rounded-history') for word in Utils.history_word]
  else:
    return [html.P(word, className='rounded-history') for word in Utils.history_word]


@app.callback(
  Output(component_id='test1', component_property='children'),
  [Input(component_id='view', component_property='n_clicks'),
   Input(component_id='topic-dropdown', component_property='value'),
   Input(component_id='tabs', component_property='value')])
def open_pdf(n_clicks, topic_value, value):
  if topic_value is not None:
    highlighted_document = os.getcwd() + '/highlighted_pdfs' + '/output_' + value + ".pdf"
    input_dir = os.path.join(highlighted_document)
  if n_clicks > Utils.highlight_pdf_click_count:
    highlight_text_in_pdf("topics/" + topic_value + "/" + value + ".pdf", Utils.history_word)

    os.startfile(input_dir)
    Utils.highlight_pdf_click_count = n_clicks


@app.callback(
  Output(component_id='tabs', component_property='children'),
  [Input(component_id='input_search', component_property='value'),
   Input(component_id='topic-dropdown', component_property='value'),
   Input(component_id='submit_val', component_property='n_clicks')],
  prevent_initial_call=True)
def add_word_to_search(value, thema, n_clicks):
  if n_clicks > Utils.click_count_temp:
    print("uso u n kliks gornji")
    if value is not None and thema is not None:
      select_topics(thema)
      add_new_keyword(value)
      Utils.click_count_temp = n_clicks
      return update_graphs()
  return update_graphs()


@app.callback(
  Output(component_id='tabs_scatter', component_property='children'),
  [Input(component_id='input_search', component_property='value'),
   Input(component_id='topic-dropdown', component_property='value'),
   Input(component_id='submit_val', component_property='n_clicks')],
  prevent_initial_call=True)
def update_graph(value, thema, n_clicks):
  if n_clicks > Utils.click_count_temp:
    if value is not None and thema is not None:
      sleep(0.5)
      return update_fig()
  return update_fig()


@app.callback(
  Output(component_id='words-dropdown', component_property='children'),
  [Input(component_id='input_search', component_property='value'),
   Input(component_id='topic-dropdown', component_property='value'),
   Input(component_id='submit_val', component_property='n_clicks')],
  prevent_initial_call=True)
def update_word_dropdown(value, thema, n_clicks):
  if n_clicks > Utils.click_count_temp:
    if value is not None and thema is not None:
      sleep(0.5)
      return select_words()
  return select_words()


if __name__ == '__main__':
  #indexer_and_searcher.index_files()
  indexer_and_searcher.init_bookmarks()

  app.run_server(debug=False)
