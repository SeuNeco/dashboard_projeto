from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# EDA
df = pd.read_csv("lello.csv")

avg_rec = df['RSU RECICLAVEL (kg)'].mean()
avg_org = df['ORGÂNICO'].mean()
avg_tot = df['RSU TOTAL (kg)'].mean()

hist_columns = ['UN', 'RSU TOTAL (kg)', 'RSU RECICLAVEL (kg)', 'ORGÂNICO', 'QUANTIDADE (toneladas)',
                'TAXA DE APROVEITAMENTO (%)', 'CUSTO DA COLETA (R$)', 'TEMPO DE COLETA (minutos)']
hist = px.histogram(df, x='UN', barmode="relative",
                    color_discrete_sequence=['#4df5b7'])

res_pred_counts = df['RESÍDUO PREDOMINANTE'].value_counts()
pie = px.pie(df, names=res_pred_counts.index, values=res_pred_counts.values,
             color_discrete_sequence=['#7640ef', '#4df5b7'])

top_cond = df.groupby('NOME CONDOMÍNIO')[
    'RSU RECICLAVEL (kg)'].sum().nlargest(5)
top5 = px.bar(top_cond, x='RSU RECICLAVEL (kg)', y=top_cond.index, orientation='h',
              color=top_cond.values, color_continuous_scale=['#7640ef', '#4df5b7'])

types = list(df['RESÍDUO PREDOMINANTE'].unique())
types.insert(0, "Todos os Resíduos")
bar = px.bar(df, x="RESÍDUO PREDOMINANTE", y="QUANTIDADE (toneladas)",
             color="NOME CONDOMÍNIO", barmode="group")

scatter = px.scatter(df, x="RSU TOTAL (kg)", y="ORGÂNICO",
                     trendline_scope="trace", color_discrete_sequence=['#4df5b7'])

# Dashboard
app = Dash(__name__)

app.layout = html.Div(className='main-container', children=[
    html.H1('Statistics'),

    html.Div(className='section-container', children=[
        html.Div(className='avg-container', children=[
            html.Div([html.H2('Reciclável'), html.P(
                f"{avg_rec:.3f} kg")], className='small-container'),
            html.Div([html.H2('Orgânico'), html.P(
                f"{avg_org:.3f} kg")], className='small-container'),
            html.Div([html.H2('Total'), html.P(
                f"{avg_tot:.3f} kg")], className='small-container')
        ]),
        html.Div(className='hist_container', children=[
            html.H2('Distribuições das Variáveis'),
            dcc.Dropdown(hist_columns, value='UN', id='hist_columns',
                         clearable=False, className='dropdown'),
            dcc.Graph(id='histograms', figure=hist)])
    ]),

    html.Div(className='section-container', children=[
        html.Div(className='scatter-container', children=[
            html.H2('Condomínios que mais Reciclam'),
            dcc.Graph(id='top5', figure=top5)])
    ]),

    html.Div(className='section-container', children=[
        html.Div(className='pie-container', children=[
            dcc.Graph(id='pie', figure=pie)]),
        html.Div(className='bar-container', children=[
            html.H2('Distribuições dos Resíduos'),
            dcc.Dropdown(types, value='Todos os Resíduos',
                         id='types_list', clearable=False, className='dropdown'),
            dcc.Graph(id='bar', figure=bar)
        ])
    ]),

    html.Div(className='section-container', children=[
        html.Div(className='scatter-container', children=[
            html.H2('Relacionamento das coletas'),
            dcc.Dropdown(['ORGÂNICO', 'RSU RECICLAVEL (kg)'],
                         value='ORGÂNICO', id='total_relations', className='dropdown'),
            dcc.Graph(id='scatter', figure=scatter)])
    ]),
])


@app.callback(
    Output('histograms', 'figure'),
    Input('hist_columns', 'value')
)
def update_output(value):
    return px.histogram(df, x=value, barmode="relative", color_discrete_sequence=['#4df5b7'])


@app.callback(
    Output('bar', 'figure'),
    Input('types_list', 'value')
)
def update_output(value):
    if value == 'Todos os Resíduos':
        return px.bar(df, x='RESÍDUO PREDOMINANTE', y='QUANTIDADE (toneladas)', color='NOME CONDOMÍNIO', barmode='group')
    else:
        return px.bar(df[df['RESÍDUO PREDOMINANTE'] == value], x='RESÍDUO PREDOMINANTE', y='QUANTIDADE (toneladas)', color='NOME CONDOMÍNIO', barmode='group')


@app.callback(
    Output('scatter', 'figure'),
    Input('total_relations', 'value')
)
def update_output(value):
    if value == 'ORGÂNICO':
        return px.scatter(df, x="RSU TOTAL (kg)", y=value, trendline_scope="trace", color_discrete_sequence=['#4df5b7'])
    else:
        return px.scatter(df, x="RSU TOTAL (kg)", y=value, trendline_scope="trace", color_discrete_sequence=['#7640ef'])


if __name__ == '__main__':
    app.run_server(debug=True)
