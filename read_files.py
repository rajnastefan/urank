import os
import PyPDF2
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.title = "uRank"

input_dir = os.path.join(os.getcwd(), "pdfs-master")
pdf_dict = {}

for file in os.listdir(input_dir):
    if file[-4:] == ".pdf":
        try:
            #print(file)
            path_to_file = os.path.join(input_dir, file)
            pdf_file = open(path_to_file, 'rb')
            file_reader = PyPDF2.PdfFileReader(pdf_file)
            pdf_dict.update({file: file_reader})
        except:
            print("[ERROR] loading " + file)

print("")
app.layout = \
    html.Div(className="big_container", children=[
        html.Title("uRank"),
        html.Div(className="words", children=[
            html.P("words A")
        ], style={"border":"1px solid black"}),
        html.Div(className="middle_field", children=[
            html.Div(className="documents", children=[
                html.P("Documents B")
            ], style={"border":"1px solid black"}),
            html.Div(className="results", children=[
                html.P("Histogram C")
            ], style={"border":"1px solid black"})
        ], style={"border":"1px solid black"}),

        html.Div(className="bookmark_history", children=[
            html.Div(className="bookmark", children=[
                html.P("Bookmarks D")
            ], style={"border": "1px solid black"}),
            html.Div(className="history", children=[
                html.P("History E")
            ], style={"border": "1px solid black"})
        ], style={"border":"1px solid black"})
])

if __name__ == '__main__':
    app.run_server(debug=False, port=8090)