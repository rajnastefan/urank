import os
import PyPDF2 as p2
import dash
import dash_core_components as dcc
import dash_html_components as html
import pdfplumber

app = dash.Dash()
app.title = "uRank"
CURRENT_LIMIT_OF_PAGES = 50
STARTING_PAGE = 21

input_dir = os.path.join(os.getcwd(), "pdfs-master")
pdf_dict = {}


def extract_and_print_text(pdf):
    counter = STARTING_PAGE
    while counter < CURRENT_LIMIT_OF_PAGES:
        page = pdf.pages[counter]
        text = page.extract_text()
        words_from_text = text.split()
        # print(words_from_text)
        counter = counter + 1
    return words_from_text


for file in os.listdir(input_dir):
    if file[-4:] == ".pdf":
        try:
            path_to_file = os.path.join(input_dir, file)
            print(path_to_file)
            pdf = pdfplumber.open(path_to_file)
            list_of_words = extract_and_print_text(pdf)
            pdf_dict.update({file: list_of_words})
        except:
            print("[ERROR] loading " + file)

for x, y in pdf_dict.items():
    print(x, y)

#######################
# FRONTEND
#######################
print("")
app.layout = \
    html.Div(className="big_container", children=[
        html.Title("uRank"),
        html.Div(className="words", children=[
            html.P("words A")
        ], style={"border": "1px solid black"}),
        html.Div(className="middle_field", children=[
            html.Div(className="documents", children=[
                html.P("Documents B")
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
if __name__ == '__main__':
    app.run_server(debug=False, port=8090)
