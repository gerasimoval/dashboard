import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from datetime import date
import datetime as dt
import plotly.graph_objs as go

pd.options.display.max_columns = None
pd.options.display.max_rows = None

CheckDate = 'Выбор даты'
df = pd.read_excel('test_data.xlsx', header=None)

colors = {
    'graphBackground': '#212529',
    'background': '#9DB1CC',
    'text': '#293133'
}


def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H4('Параметры', style={
        'align': 'left',
        'color': colors['text']
    }),

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
        id='date-picker-range',
        min_date_allowed=date(1990, 1, 1),
        max_date_allowed=date(2021, 2, 13),
        initial_visible_month=date(2021, 1, 1),
        # end_date=date(2021, 1, 1)
    ),
    html.Div(id='output-container-date-picker-range'),

    # generate_table(df)
    dcc.Graph(id='in-temp-graph')
])


# @app.callback(
#     dash.dependencies.Output('output-container-date-picker-range', 'children'),
#     [dash.dependencies.Input('date-picker-range', 'start_date'),
#      dash.dependencies.Input('date-picker-range', 'end_date')])
# def update_output(start_date, end_date):
#     string_prefix = 'Вы выбрали '
#     if start_date is not None:
#         start_date_object = date.fromisoformat(start_date)
#         start_date_string = start_date_object.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'начальную дату: ' + start_date_string + ' | '
#     if end_date is not None:
#         end_date_object = date.fromisoformat(end_date)
#         end_date_string = end_date_object.strftime('%B %d, %Y')
#         string_prefix = string_prefix + 'конечную дату: ' + end_date_string
#     if len(string_prefix) == len('Вы выбрали '):
#         return 'Выберите дату, что бы увидеть здесь'
#     else:
#         return string_prefix


@app.callback(
    Output('in-temp-graph', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end-date')]
)
def update_graph(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_df = df[df.date.between(
        dt.datetime.strftime(start_date, '%Y-%m-%d'),
        dt.datetime.strftime(end_date, '%Y-$m-%d')
    )]

    trace1 = go.Scatter(
        x=filtered_df.date,
        mode='lines',
        name=CheckDate
    )

    return {
        'data': [trace1],
        'layout': go.Layout(
            title=CheckDate,
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"]
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
