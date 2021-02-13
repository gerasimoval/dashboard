import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

pd.options.display.max_columns = None
pd.options.display.max_rows = None

df = pd.read_excel('test_data.xlsx', header=None)


def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i] [col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='Параметры'),
    dcc.Checklist(
        options=[
            {'label': 'Поручения', 'value': '1'},
            {'label': 'Протоколы', 'value': '2'},
            {'label': 'Служебные записки', 'value': '3'},
            {'label': 'Показывать завершенные', 'value': '4'}
        ],
        value=['MTL', 'SF']
    ),
    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)
