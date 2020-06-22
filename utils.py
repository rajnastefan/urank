from dash.dependencies import Input

class Utils:
    click_count_temp = 0
    bookmark_click_count = 0
    bookmark_click_count_clear = 0
    history_click_count = 0
    history_word = []
    bookmarked_documents = []
    highlight_pdf_click_count = 0
    list_of_found_words = []

    @staticmethod
    def get_input_parameters(keys):
        list_of_something = []
        for key in keys:
            list_of_something.append(
                Input(component_id='bookmark_doc_' + key.split(".pd")[0], component_property='n_clicks'))
        # if len(list_of_something) == 0:
        #     return Input(" ", "")
        # else:
        return list_of_something