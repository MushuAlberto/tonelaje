import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Configuración de la página
st.set_page_config(layout="wide", page_title="Dashboard de Tonelaje")

# Título de la aplicación
st.title("Dashboard de Tonelaje por Empresa")

# Función para normalizar nombres de empresas
def normalizar_empresas(df):
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
    df['EMPRESA DE TRANSPORTE'] = df['EMPRESA DE TRANSPORTE'].str.strip().str.upper().map(empresa_mapping).fillna(df['EMPRESA DE TRANSPORTE'])
    return df

# Carga de archivo
uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Leer el archivo
        df = pd.read_excel(uploaded_file)

        # Normalizar empresas
        df = normalizar_empresas(df)

        # Filtrar solo producto SLIT
        df_slit = df[df['PRODUCTO'].str.strip().str.upper() == 'SLIT'].copy()

        # Convertir fecha
        df_slit['FECHA'] = pd.to_datetime(df_slit['FECHA'], dayfirst=True)

        # Filtros
        empresas_unicas = df_slit['EMPRESA DE TRANSPORTE'].unique().tolist()
        empresas_seleccionadas = st.multiselect("Selecciona Empresas", empresas_unicas, default=empresas_unicas)

        fechas_unicas = df_slit['FECHA'].dt.date.unique().tolist()
        fechas_seleccionadas = st.multiselect("Selecciona Fechas", fechas_unicas, default=fechas_unicas)

        # Filtrar DataFrame
        df_filtrado = df_slit[
            (df_slit['EMPRESA DE TRANSPORTE'].isin(empresas_seleccionadas)) &
            (df_slit['FECHA'].dt.date.isin(fechas_seleccionadas))
        ]

        # Agrupar datos
        df_grouped = df_filtrado.groupby(['FECHA', 'EMPRESA DE TRANSPORTE'])['TONELAJE'].sum().reset_index()

        # Valor programado fijo
        tonelaje_programado = 1197

        # Crear gráfico con barras reales y línea de tonelaje programado
        fig = go.Figure()

        # Añadir barras por empresa
        for empresa in df_grouped['EMPRESA DE TRANSPORTE'].unique():
            df_emp = df_grouped[df_grouped['EMPRESA DE TRANSPORTE'] == empresa]
            fig.add_trace(go.Bar(
                x=df_emp['FECHA'],
                y=df_emp['TONELAJE'],
                name=f'Real - {empresa}'
            ))

        # Añadir línea de tonelaje programado
        fechas_sorted = sorted(df_grouped['FECHA'].unique())
        fig.add_trace(go.Scatter(
            x=fechas_sorted,
            y=[tonelaje_programado] * len(fechas_sorted),
            mode='lines',
            name='Tonelaje Programado (1197)',
            line=dict(color='red', dash='dash')
        ))

        # Configurar layout
        fig.update_layout(
            title='Sumatoria Diaria de Tonelaje por Empresa (Producto SLIT) vs Tonelaje Programado',
            xaxis_title='Fecha',
            yaxis_title='Tonelaje (ton)',
            barmode='group',
            height=600
        )

        # Mostrar gráfico
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {str(e)}")
else:
    st.info("Por favor, sube un archivo Excel para comenzar.")