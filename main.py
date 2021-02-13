import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import date
import re

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

    html.H4('Период отчета'),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(1990, 1, 1),
        max_date_allowed=date(2021, 2, 13),
        initial_visible_month=date(2021, 1, 1),
        # end_date=date(2021, 1, 1)
    ),
    html.Div(id='output-container-date-picker-range'),


generate_table(df)
])


@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'Вы выбрали: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Начальная дата: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Конечная дата: ' + end_date_string
    if len(string_prefix) == len('Вы выбрали: '):
        return 'Выберите дату, что бы увидеть здесь'
    else:
        return string_prefix


if __name__ == '__main__':
    app.run_server(debug=True)



# df.info()

# print(df[23:29])
