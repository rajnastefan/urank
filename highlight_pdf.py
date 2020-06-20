# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 09:59:11 2020

@author: GRussell
"""

import base64
import fitz
import datetime
import io
import time

import fitz
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from pdf2image import convert_from_path, convert_from_bytes

import pandas as pd

from pdf2image import convert_from_bytes

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Div(
        children=[
            dcc.Upload(
                className="four columns",
                id='upload-coa',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select PDF')
                ]),
                style={
                    'width': '45%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=False
            ),
        ]
    ),
    html.Hr(),
    html.Div(id='output-coa'),
])


def pil_to_b64_dash(im):
    buffered = io.BytesIO()
    im.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return bytes("data:image/jpeg;base64,", encoding='utf-8') + img_str



def highlight_text_in_pdf(filename,words):
    doc = fitz.open(filename)
    for page in doc:
        for word in words:
            text_instance = page.searchFor(word)
            if (text_instance):
                for inst in text_instance:
                    highlight = page.addHighlightAnnot(inst)

    doc.save("output_" + filename, garbage=4, deflate=True, clean=True)

def parse_coa_contents(contents, filename, date):

    ### READ IN PDF
    highlight_text_in_pdf("","")


    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    images = convert_from_bytes(decoded)
    div_child = []
    for image in images:
        encode = pil_to_b64_dash(image)
        div_child.append(html.Img(src=encode.decode('utf-8')))



    return html.Div(
       children = div_child
    )


@app.callback(Output('output-coa', 'children'),
              [Input('upload-coa', 'contents')],
              [State('upload-coa', 'filename'),
               State('upload-coa', 'last_modified')])
def show_coa(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [parse_coa_contents(list_of_contents, list_of_names, list_of_dates)]
        return children


if __name__ == '__main__':
    app.run_server(debug=True)