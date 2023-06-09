from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("lello.csv")

fig = px.bar(df, x="RESÍDUO PREDOMINANTE", y="QUANTIDADE (toneladas)", color="NOME CONDOMÍNIO", barmode="group")
opcoes = list(df['RESÍDUO PREDOMINANTE'].unique())
opcoes.append("Todos os Resíduos")

app.layout = html.Div(children=[
    html.H1(children='Descarte nos Condomínios'),
    html.H2(children='Gráfico com a quantidade em toneladas de lixo, organizado por resíduo e separado por condomínio'),
    dcc.Dropdown(opcoes, value='Todos os Resíduos', id='lista_residuos'),

    dcc.Graph(
        id='grafico_quantidade_residuos',
        figure=fig
    )
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

if __name__ == '__main__':
    app.run_server(debug=True)
