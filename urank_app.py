import dash
import dash_core_components as dcc
import dash_html_components as html
import pdfplumber
from search import UserInput
from dash.dependencies import Input, Output
import fitz
from utils import Utils
import os


app = dash.Dash()
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

  doc.save(os.path.join(filename.split("/")[0], filename.split("/")[1], "output_" + filename.split("/")[2]), garbage=4, deflate=True, clean=True)


def select_topics(topic):
  indexer_and_searcher.prepare_indexes_for_searching(topic)


def add_new_keyword(keyword):
  indexer_and_searcher.fill_term_list(keyword)
  indexer_and_searcher.search_files()
  print("found results: ")
  print(indexer_and_searcher.found_pdfs)

def update_graphs():
  list_tabs = []
  for key in indexer_and_searcher.found_pdfs.keys():
    list_tabs.append(
    dcc.Tab(label=key.split(" ")[0], children=[
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
            'title': key.split(" ")[0]
          }
        }
      ),
      html.Button('View', id='view_' + key.split(" ")[0], n_clicks=0),
    ]))
  return list_tabs


#######################
# FRONTEND
#######################
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
          {'label': 'thema1', 'value': 'thema1'},
          {'label': 'thema2', 'value': 'thema2'},
          {'label': 'thema3', 'value': 'thema3'}
        ],
      ),
      html.P('Choose a words'),
      dcc.Input(
        id="input_search",
        type="search",
        placeholder="search",
      ),
      html.Button('Submit', id='submit_val', n_clicks=0),
    ]),

    html.Div(className="middle_field", children=[
      html.Div(id="test1"),
      html.Div(id="test2"),
      html.Div(id="histogram", className="results", children=[
        dcc.Tabs(id="tabs", children=[

          ])

      ])
    ]),

    html.Div(className="bookmark_history", children=[
      html.Div(className="bookmark", children=[
        html.P("Bookmark")
      ]),
      html.Div(id="his", className="history", children=[html.P("History"),
                                                        html.Button('Clear history', id='clear_history', style={"background-color": "#DAF0EB"}),
                                   html.Div(id="history")])
    ])
  ])

@app.callback(
  Output(component_id='history', component_property='children'),
  [Input(component_id='input_search', component_property='value'),
  Input(component_id='submit_val', component_property='n_clicks'),
   Input(component_id='clear_history', component_property='n_clicks')])
def update_history(value, n_clicks, n_clicks2):
  # if n_clicks2 is not None:
  #   print(n_clicks2)
  #   Utils.history_word.clear()
  if n_clicks > Utils.click_count_temp:
    if value is not None:
      if value not in Utils.history_word:
        Utils.history_word.append(value)
      return [html.P(word) for word in Utils.history_word]
    elif value == "":
      [html.P(word) for word in Utils.history_word]
  else:
    [html.P(word) for word in Utils.history_word]

@app.callback(
  Output(component_id='tabs', component_property='children'),
  [Input(component_id='input_search', component_property='value'),
   Input(component_id='topic-dropdown', component_property='value'),
   Input(component_id='submit_val', component_property='n_clicks')])
def add_word_to_search(value, thema, n_clicks):
  if n_clicks > Utils.click_count_temp:
    if value is not None and thema is not None:
      select_topics(thema)
      add_new_keyword(value)
      Utils.click_count_temp = n_clicks
      return update_graphs()
  else:
    return [dcc.Tab(label="Doc 1", children=[
                dcc.Graph(
                  figure={
                    'data': [
                    ],
                    'layout': {
                      'title': 'Dummy'
                    }
                  }
                )
              ])]


@app.callback(
  Output(component_id='test1', component_property='children'),
  [Input(component_id='view_NVIDIA', component_property='n_clicks') ] )
def open_pdf(n_clicks):
  #TODO: Dynamic implementation
  print("usao")
  if(n_clicks > 0):
    highlight_text_in_pdf("topics/thema1/NVIDIA - Turing GPU Architecture - Graphics Reinveted.pdf", Utils.history_word)
    os.startfile(r"C:\Users\rajna\Documents\urank\topics\thema1\output_NVIDIA - Turing GPU Architecture - Graphics Reinveted.pdf")

if __name__ == '__main__':
  # indexer_and_searcher.index_files()
  app.run_server(debug=False)
