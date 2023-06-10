from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("lello.csv")

# gráficos com análises e filtros
fig = px.bar(df, x="RESÍDUO PREDOMINANTE", y="QUANTIDADE (toneladas)", color="NOME CONDOMÍNIO", barmode="group")
fig2 = px.bar(df, x="NOME CONDOMÍNIO", y="RSU RECICLAVEL (kg)", color="NOME CONDOMÍNIO", barmode="group")
fig3 = px.scatter(df, x="RSU TOTAL (kg)", y="ORGÂNICO", trendline_scope="trace")

# histogramas das variáveis do dataset
fig4 = px.histogram(df, x="UN", barmode="relative")
fig5 = px.histogram(df, x="RSU TOTAL (kg)", barmode="relative")
fig6 = px.histogram(df, x="RSU RECICLAVEL (kg)", barmode="relative")
fig7 = px.histogram(df, x="ORGÂNICO", barmode="relative")
fig8 = px.histogram(df, x="QUANTIDADE (toneladas)", barmode="relative")
fig9 = px.histogram(df, x="TAXA DE APROVEITAMENTO (%)", barmode="relative")
fig10 = px.histogram(df, x="CUSTO DA COLETA (R$)", barmode="relative")
fig11 = px.histogram(df, x="TEMPO DE COLETA (minutos)", barmode="relative")

# gráfico de pizza dos resíduos
res_pred_counts = df['RESÍDUO PREDOMINANTE'].value_counts()
fig12 = px.pie(df, names=res_pred_counts.index, values=res_pred_counts.values)

# opções para seleção de filtro dos gráficos onde é possível filtrar
opcoes = list(df['RESÍDUO PREDOMINANTE'].unique())
opcoes.append("Todos os Resíduos")

opcoes2 = list(df['NOME CONDOMÍNIO'].unique())
opcoes2.append("Todos os Condomínios")

app.layout = html.Div(children=[

    html.H1(children='Bem-Vindo ao nosso Dashboard !'),
    html.H1(children='Abaixo podem ser vistas as diversas análises feitas pelo Grupo:'),
    html.H1(children='Descarte nos Condomínios'),
    html.H2(children='Gráfico com a quantidade em toneladas de lixo, organizado por resíduo e separado por condomínio'),
    dcc.Dropdown(opcoes, value='Todos os Resíduos', id='lista_residuos'),

    dcc.Graph(
        id='grafico_quantidade_residuos',
        figure=fig
    ),

    html.H1(children='Condomínios que mais reciclam'),
    html.H2(children='Gráfico que mostra a taxa de RSU Reciclável gerada pelos condomínios'),
    dcc.Dropdown(opcoes2, value='Todos os Condomínios', id='lista_condominios'),

    dcc.Graph(
        id='grafico_condominios',
        figure=fig2
    ),

    html.H1(children='Gráfico de Dispersão'),
    html.H2(children='Gráfico que mostra a dispersão das medidas de descarte orgânico quando comparadas ao rsu total'),

    dcc.Graph(
        id='grafico_dispersao',
        figure=fig3
    ),

    html.H1(children='Histogramas mostrando as distribuições das variáveis'),
    html.H2(children='Gráficos que mostram como as variáveis se distribuem, para que tenhamos uma melhor análise'),

    dcc.Graph(
        id='grafico_histograma1',
        figure=fig4
    ),

    dcc.Graph(
        id='grafico_histograma2',
        figure=fig5
    ),

    dcc.Graph(
        id='grafico_histograma3',
        figure=fig6
    ),

    dcc.Graph(
        id='grafico_histograma4',
        figure=fig7
    ),

    dcc.Graph(
        id='grafico_histograma5',
        figure=fig8
    ),
    dcc.Graph(
        id='grafico_histograma6',
        figure=fig9
    ),
    dcc.Graph(
        id='grafico_histograma7',
        figure=fig10
    ),
    dcc.Graph(
        id='grafico_histograma8',
        figure=fig11
    ),

    html.H1(children='Distribuição dos Tipos de Resíduos'),
    html.H2(children='Gráfico que mostra como se dá a distribuição dos Resíduos gerados pelos condomínios'),

    dcc.Graph(
        id='grafico_pizza',
        figure=fig12
    ),

])


@app.callback(
    Output('grafico_quantidade_residuos', 'figure'),
    Input('lista_residuos', 'value')
)
def update_output(value):
    if value == "Todos os Resíduos":
        fig = px.bar(df, x="RESÍDUO PREDOMINANTE", y="QUANTIDADE (toneladas)", color="NOME CONDOMÍNIO", barmode="group")
    else:
        dataset_filtrado = df.loc[df["RESÍDUO PREDOMINANTE"]==value, :]
        fig = px.bar(dataset_filtrado, x="RESÍDUO PREDOMINANTE", y="QUANTIDADE (toneladas)", color="NOME CONDOMÍNIO", barmode="group")
    return fig


@app.callback(
    Output('grafico_condominios','figure'),
    Input('lista_condominios','value'),
)
def update_output(value):
    if value == "Todos os Condomínios":
        fig2 = px.bar(df, x="NOME CONDOMÍNIO", y="RSU RECICLAVEL (kg)", color="NOME CONDOMÍNIO", barmode="group")
    else:
        filtro = df.loc[df["NOME CONDOMÍNIO"]==value, :]
        fig2 = px.bar(filtro, x="NOME CONDOMÍNIO", y="RSU RECICLAVEL (kg)", color="NOME CONDOMÍNIO", barmode="group")
    return fig2


if __name__ == '__main__':
    app.run_server(debug=True)
