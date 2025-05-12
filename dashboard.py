import pandas as pd
import plotly.express as px
from datetime import datetime

# Cargar el archivo Excel
df = pd.read_excel('05.- Histórico Romanas.xlsx')

# Normalizar nombres de empresas según el mapeo proporcionado
empresa_mapping = {
    "JORQUERA TRANSPORTE S A": "JORQUERA TRANSPORTE S. A.",
    "MINING SERVICES AND DERIVATES": "M S & D SPA",
    "MINING SERVICES AND DERIVATES SPA": "M S & D SPA",
    "M S AND D": "M S & D SPA",
    "M S AND D SPA": "M S & D SPA",
    "MSANDD SPA": "M S & D SPA",
    "M S D": "M S & D SPA",
    "M S D SPA": "M S & D SPA",
    "M S & D": "M S & D SPA",
    "M S & D SPA": "M S & D SPA",
    "MS&D SPA": "M S & D SPA",
    "M AND Q SPA": "M&Q SPA",
    "M AND Q": "M&Q SPA",
    "M Q SPA": "M&Q SPA",
    "MQ SPA": "M&Q SPA",
    "M&Q SPA": "M&Q SPA",
    "MANDQ SPA": "M&Q SPA",
    "MINING AND QUARRYING SPA": "M&Q SPA",
    "MINING AND QUARRYNG SPA": "M&Q SPA",
    "AG SERVICE SPA": "AG SERVICES SPA",
    "AG SERVICES SPA": "AG SERVICES SPA",
    "COSEDUCAM S A": "COSEDUCAM S A",
    "COSEDUCAM": "COSEDUCAM S A"
}

# Aplicar el mapeo y filtrar solo producto SLIT
df['EMPRESA DE TRANSPORTE'] = df['EMPRESA DE TRANSPORTE'].str.strip().str.upper().map(empresa_mapping).fillna(df['EMPRESA DE TRANSPORTE'])
df_slit = df[df['PRODUCTO'].str.strip().str.upper() == 'SLIT'].copy()

# Convertir fecha a formato datetime
df_slit['FECHA'] = pd.to_datetime(df_slit['FECHA'], dayfirst=True)

# Agrupar por fecha y empresa, sumando el tonelaje
df_grouped = df_slit.groupby(['FECHA', 'EMPRESA DE TRANSPORTE'])['TONELAJE'].sum().reset_index()

# Crear el dashboard interactivo
fig = px.bar(df_grouped, 
             x='FECHA', 
             y='TONELAJE', 
             color='EMPRESA DE TRANSPORTE',
             title='Sumatoria Diaria de Tonelaje por Empresa (Producto SLIT)',
             labels={'TONELAJE': 'Tonelaje (ton)', 'FECHA': 'Fecha'},
             height=600)

# Añadir controles de filtro
fig.update_layout(
    updatemenus=[
        dict(
            type="dropdown",
            direction="down",
            buttons=list([
                dict(
                    args=[{"visible": [True]*len(df_grouped)}],
                    label="Todas las empresas",
                    method="update"
                )] + [
                dict(
                    args=[{"visible": [x == empresa for x in df_grouped['EMPRESA DE TRANSPORTE']]}],
                    label=empresa,
                    method="update"
                ) for empresa in df_grouped['EMPRESA DE TRANSPORTE'].unique()
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            x=1.05,
            xanchor="left",
            y=1,
            yanchor="top"
        ),
        dict(
            type="buttons",
            direction="right",
            buttons=list([
                dict(
                    args=[{"xaxis.type": "date"}],
                    label="Rango de fechas",
                    method="relayout"
                )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            x=1.05,
            xanchor="left",
            y=0.9,
            yanchor="top"
        )
    ]
)

# Mostrar el gráfico
fig.show()