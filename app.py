from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# EDA
df = pd.read_csv("lello.csv")

hist_columns = ['UN', 'RSU TOTAL (kg)', 'RSU RECICLAVEL (kg)', 'ORGÂNICO', 'QUANTIDADE (toneladas)', 'TAXA DE APROVEITAMENTO (%)', 'CUSTO DA COLETA (R$)', 'TEMPO DE COLETA (minutos)']
hist = px.histogram(df, x='UN', barmode="relative", color_discrete_sequence=['#4df5b7'])

res_pred_counts = df['RESÍDUO PREDOMINANTE'].value_counts()
pie = px.pie(df, names=res_pred_counts.index, values=res_pred_counts.values, color_discrete_sequence=['#7640ef', '#4df5b7'])

top_cond = df.groupby('NOME CONDOMÍNIO')['RSU RECICLAVEL (kg)'].sum().nlargest(5)
top5 = px.bar(top_cond, x='RSU RECICLAVEL (kg)', y=top_cond.index, orientation='h', color=top_cond.values, color_continuous_scale=['#7640ef', '#4df5b7'])

types = list(df['RESÍDUO PREDOMINANTE'].unique())
types.insert(0, "Todos os Resíduos")
bar = px.bar(df, x="RESÍDUO PREDOMINANTE", y="QUANTIDADE (toneladas)", color="NOME CONDOMÍNIO", barmode="group")

scatter = px.scatter(df, x="RSU TOTAL (kg)", y="ORGÂNICO", trendline_scope="trace", color_discrete_sequence=['#4df5b7'])

# Dashboard
app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Statistics', style={'color': '#000000', 'font-family': 'Arial', 'font-size': '36px', 'text-align': 'center', 'margin-bottom': '50px'}),
    html.Div([html.H2('Distribuições das Variáveis', style={'color': '#000000', 'font-family': 'Arial'}), dcc.Dropdown(hist_columns, value='UN', id='hist_columns', clearable=False, style={'font-family': 'Arial', 'font-size': '14px'}),
              dcc.Graph(id='histograms', figure=hist)], style={'background-color': '#FFFFFF', 'padding': '20px', 'margin-bottom': '20px', 'border-radius': '10px', 'box-shadow': '0px 0px 20px rgba(0, 0, 0, 0.1)'}),
    html.Div([html.H2('Distribuições dos Resíduos', style={'color': '#000000', 'font-family': 'Arial'}), dcc.Graph(id='pie', figure=pie)], style={'background-color': '#FFFFFF', 'padding': '20px', 'margin-bottom': '20px', 'border-radius': '10px', 'box-shadow': '0px 0px 20px rgba(0, 0, 0, 0.1)'}),
    html.Div([html.H2('Condomínios que mais Reciclam', style={'color': '#000000', 'font-family': 'Arial'}), dcc.Graph(id='top5', figure=top5)], style={'background-color': '#FFFFFF', 'padding': '20px', 'margin-bottom': '20px', 'border-radius': '10px', 'box-shadow': '0px 0px 20px rgba(0, 0, 0, 0.1)'}),
    html.Div([html.H2('Distribuições dos Resíduos', style={'color': '#000000', 'font-family': 'Arial'}), dcc.Dropdown(types, value='Todos os Resíduos', id='types_list', clearable=False, style={'font-family': 'Arial', 'font-size': '14px'}),
              dcc.Graph(id='bar', figure=bar)], style={'background-color': '#FFFFFF', 'padding': '20px', 'margin-bottom': '20px', 'border-radius': '10px', 'box-shadow': '0px 0px 20px rgba(0, 0, 0, 0.1)'}),
    html.Div([html.H2('Relacionamento das coletas', style={'color': '#000000', 'font-family': 'Arial'}), dcc.Dropdown(['ORGÂNICO', 'RSU RECICLAVEL (kg)'], value='ORGÂNICO', id='total_relations', style={'font-family': 'Arial', 'font-size': '14px'}),
              dcc.Graph(id='scatter', figure=scatter)], style={'background-color': '#FFFFFF', 'padding': '20px', 'margin-bottom': '20px', 'border-radius': '10px', 'box-shadow': '0px 0px 20px rgba(0, 0, 0, 0.1)'}),
], style={'background-color': '#FFFFFF', 'padding': '50px'})

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
