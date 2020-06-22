import dash
import dash_core_components as dcc
import dash_html_components as html
import pdfplumber
from urank_backend import UserInput
from dash.dependencies import Input, Output
import fitz
from utils import Utils
import os
# import dash_bootstrap_components as dbc

app = dash.Dash()#external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "uRank"

pdf_dict = {}
indexer_and_searcher = UserInput()


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
  indexer_and_searcher.search_files()
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


@app.callback(
  Output(component_id='bookmark_list', component_property='children'),
  [Input(component_id='tabs', component_property='value'),
   Input(component_id="bookmark_doc_", component_property='n_clicks'),
   Input(component_id='clear_bookmark', component_property='n_clicks'),
   ],
  [dash.dependencies.State('tabs', 'value')]
)
def bookmark(value, n_clicks, n_clicks2, state):
  if n_clicks2 is not None:
    print(n_clicks2)
    Utils.bookmarked_documents.clear()
    return [html.P(doc) for doc in Utils.bookmarked_documents]
  if n_clicks > Utils.bookmark_click_count:
    if value is not None:
      if value not in Utils.bookmarked_documents:
        Utils.bookmarked_documents.append(value)
        print("lista", Utils.bookmarked_documents)
        Utils.bookmark_click_count = n_clicks
        return [html.P(doc) for doc in Utils.bookmarked_documents]
    elif value == "":
      return [html.P(doc) for doc in Utils.bookmarked_documents]
  else:
    return [html.P(doc) for doc in Utils.bookmarked_documents]


def select_themas():
  return_list = []
  for subdir, dirs, files in os.walk("topics"):
    for dir in dirs:
      return_list.append({'label': dir, 'value': dir})

  return return_list


#######################
# FRONTEND
#######################
app.layout = \
  html.Div(className="big_container", children=[
    html.Title("uRank"),

    html.Div(className="bookmark_history", children=[
      html.Div(className="bookmark", children=[
        html.H1('Choose a topic'),

        # html.Br(),
        dcc.Dropdown(
          id='topic-dropdown',
          options=select_themas(),
        ),
      ]),
      html.Div(id="words_search", className="history", children=[
        html.H1('Type in words'),
        dcc.Input(
          id="input_search",
          type="search",
          placeholder="search",
        ),
        html.Button('Submit', id='submit_val', n_clicks=0),
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
        html.I(id='bookmark_doc_', n_clicks=0, className='fi-star')

      ])
    ]),

    html.Div(className="bookmark_history", children=[
      html.Div(className="bookmark", children=[
        html.H1("Bookmark"),
        html.Button('Clear bookmarks', id='clear_bookmark',
                    style={"background-color": "#DAF0EB"}),
        html.Div(id="bookmark_list", children=[html.P(doc) for doc in Utils.bookmarked_documents])
      ]),
      html.Div(id="his", className="history", children=[html.H1("History"),
                                                        html.Button('Clear history', id='clear_history',
                                                                    style={"background-color": "#DAF0EB"}),
                                                        html.Div(id="history")])
    ])
  ])


@app.callback(
  Output(component_id='history', component_property='children'),
  [Input(component_id='input_search', component_property='value'),
   Input(component_id='submit_val', component_property='n_clicks'),
   Input(component_id='clear_history', component_property='n_clicks')])
def update_history(value, n_clicks, n_clicks2):
  if n_clicks2 is not None:
    print(n_clicks2)
    Utils.history_word.clear()
    return [html.P(word) for word in Utils.history_word]
  if n_clicks > Utils.click_count_temp:
    if value is not None:
      if value not in Utils.history_word:
        Utils.history_word.append(value)
      return [html.P(word) for word in Utils.history_word]
    elif value == "":
      return [html.P(word) for word in Utils.history_word]
  else:
    return [html.P(word) for word in Utils.history_word]


@app.callback(
  Output(component_id='tabs', component_property='children'),
  [Input(component_id='input_search', component_property='value'),
   Input(component_id='topic-dropdown', component_property='value'),
   Input(component_id='submit_val', component_property='n_clicks')],
  prevent_initial_call=True)
def add_word_to_search(value, thema, n_clicks):
  if n_clicks > Utils.click_count_temp:
    if value is not None and thema is not None:
      select_topics(thema)
      add_new_keyword(value)
      Utils.click_count_temp = n_clicks
      return update_graphs()


@app.callback(
  Output(component_id='test1', component_property='children'),
  [Input(component_id='view', component_property='n_clicks'),
   Input(component_id='topic-dropdown', component_property='value'),
   Input(component_id='tabs', component_property='value')])
def open_pdf(n_clicks, topic_value, value):
  if topic_value is not None:
    highlighted_document = os.getcwd() + '/highlighted_pdfs' + '/output_' + value + ".pdf"
    input_dir = os.path.join(highlighted_document)
  if n_clicks > 0:
    highlight_text_in_pdf("topics/thema1/" + value + ".pdf", Utils.history_word)
    os.startfile(input_dir)


if __name__ == '__main__':
  # indexer_and_searcher.index_files()
  app.run_server(debug=False)
