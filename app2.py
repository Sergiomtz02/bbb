import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Definimos la lista de instrumentos financieros como una variable global
ETFs_Data = [
    {"nombre": "AZ QQQ NASDAQ 100", "descripcion": "ETF que sigue el rendimiento del índice NASDAQ 100.", "simbolo": "QQQ"},
    {"nombre": "AZ SPDR S&P 500 ETF TRUST", "descripcion": "ETF que sigue el rendimiento del índice S&P 500.", "simbolo": "SPY"},
    {"nombre": "AZ SPDR DJIA TRUST", "descripcion": "ETF que sigue el rendimiento del índice Dow Jones Industrial Average.", "simbolo": "DIA"},
    {"nombre": "AZ VANGUARD EMERGING MARKET ETF", "descripcion": "ETF de Vanguard que sigue el rendimiento de mercados emergentes.", "simbolo": "VWO"},
    {"nombre": "AZ FINANCIAL SELECT SECTOR SPDR", "descripcion": "ETF que sigue el rendimiento del sector financiero de EE.UU.", "simbolo": "XLF"},
    {"nombre": "AZ HEALTH CARE SELECT SECTOR", "descripcion": "ETF que sigue el rendimiento del sector de salud de EE.UU.", "simbolo": "XLV"},
    {"nombre": "AZ DJ US HOME CONSTRUCT", "descripcion": "ETF que sigue el rendimiento del sector de construcción de viviendas en EE.UU.", "simbolo": "ITB"},
    {"nombre": "AZ SILVER TRUST", "descripcion": "ETF que sigue el precio de la plata.", "simbolo": "SLV"},
    {"nombre": "AZ MSCI TAIWAN INDEX FD", "descripcion": "ETF que sigue el rendimiento del índice MSCI Taiwan.", "simbolo": "EWT"},
    {"nombre": "AZ MSCI UNITED KINGDOM", "descripcion": "ETF que sigue el rendimiento del índice MSCI United Kingdom.", "simbolo": "EWU"},
    {"nombre": "AZ MSCI SOUTH KOREA IND", "descripcion": "ETF que sigue el rendimiento del índice MSCI South Korea.", "simbolo": "EWY"},
    {"nombre": "AZ MSCI EMU", "descripcion": "ETF que sigue el rendimiento del índice MSCI EMU (Unión Monetaria Europea).", "simbolo": "EZU"},
    {"nombre": "AZ MSCI JAPAN INDEX FD", "descripcion": "ETF que sigue el rendimiento del índice MSCI Japan.", "simbolo": "EWJ"},
    {"nombre": "AZ MSCI CANADA", "descripcion": "ETF que sigue el rendimiento del índice MSCI Canada.", "simbolo": "EWC"},
    {"nombre": "AZ MSCI GERMANY INDEX", "descripcion": "ETF que sigue el rendimiento del índice MSCI Germany.", "simbolo": "EWG"},
    {"nombre": "AZ MSCI AUSTRALIA INDEX", "descripcion": "ETF que sigue el rendimiento del índice MSCI Australia.", "simbolo": "EWA"},
    {"nombre": "AZ BARCLAYS AGGREGATE", "descripcion": "ETF que sigue el rendimiento del índice de bonos Barclays Aggregate.", "simbolo": "AGG"}
]

# Periodos a analizar
periodos = {
    "1 Mes": "1mo",
    "3 Meses": "3mo",
    "6 Meses": "6mo",
    "1 Año": "1y",
    "3 Años": "3y",
    "5 Años": "5y",
    "10 Años": "10y",
    "YTD": "ytd"
}

# Inicializar session_state
if 'nombre_cliente' not in st.session_state:
    st.session_state.nombre_cliente = ""
if 'pestaña_actual' not in st.session_state:
    st.session_state.pestaña_actual = 0  # Comienza en la primera pestaña

# Streamlit UI
st.title("Allianz Patrimonial")

# Crear pestañas
tabs = st.tabs(["Información del Cliente", "Análisis de ETFs", "Resultados", "Recomendaciones por Perfil"])

# Información Personal del Cliente
with tabs[0]:
    if 'datos_guardados' in st.session_state and st.session_state.datos_guardados:
        st.header("Datos Guardados Correctamente")
        if st.button("Editar Información"):
            st.session_state.datos_guardados = False
            st.session_state.nombre_cliente = ""
            st.session_state.edad_cliente = 0
            st.session_state.genero_cliente = "Masculino"
            st.session_state.direccion_cliente = ""
            st.session_state.pais_cliente = ""
            st.session_state.nacionalidad_cliente = ""
            st.session_state.ocupacion_cliente = ""
    else:
        st.header("Información Personal del Cliente")
        nombre = st.text_input("Nombre:", value=st.session_state.get("nombre_cliente", ""))
        edad = st.number_input("Edad:", min_value=0, max_value=150, value=st.session_state.get("edad_cliente", 0))
        genero_opciones = ["Masculino", "Femenino", "Otro"]
        genero = st.selectbox("Género:", genero_opciones, index=genero_opciones.index(st.session_state.get("genero_cliente", "Masculino")) if st.session_state.get("genero_cliente") in genero_opciones else 0)
        direccion = st.text_input("Dirección:", value=st.session_state.get("direccion_cliente", ""))
        pais = st.text_input("País:", value=st.session_state.get("pais_cliente", ""))
        nacionalidad = st.text_input("Nacionalidad:", value=st.session_state.get("nacionalidad_cliente", ""))
        ocupacion = st.text_input("Ocupación:", value=st.session_state.get("ocupacion_cliente", ""))
        if st.button("Guardar Información"):
            st.session_state.nombre_cliente = nombre
            st.session_state.edad_cliente = edad
            st.session_state.genero_cliente = genero
            st.session_state.direccion_cliente = direccion
            st.session_state.pais_cliente = pais
            st.session_state.nacionalidad_cliente = nacionalidad
            st.session_state.ocupacion_cliente = ocupacion
            st.session_state.datos_guardados = True

# Análisis de ETFs
with tabs[1]:
    if st.session_state.nombre_cliente:
        st.write(f"**Bienvenido, {st.session_state.nombre_cliente}**")
        st.write(f"- **Edad**: {st.session_state.edad_cliente}")
        st.write(f"- **Género**: {st.session_state.genero_cliente}")
        st.write(f"- **Dirección**: {st.session_state.direccion_cliente}")
        st.write(f"- **País**: {st.session_state.pais_cliente}")
        st.write(f"- **Nacionalidad**: {st.session_state.nacionalidad_cliente}")
        st.write(f"- **Ocupación**: {st.session_state.ocupacion_cliente}")

    st.write("Analiza el rendimiento y riesgo de múltiples ETFs en periodos específicos.")
    etfs_seleccionados = st.multiselect("Selecciona ETFs para comparar:", [etf['nombre'] for etf in ETFs_Data])
    etf_symbols = [etf['simbolo'] for etf in ETFs_Data if etf['nombre'] in etfs_seleccionados]
    periodo_seleccionado = st.selectbox("Selecciona el periodo de análisis:", list(periodos.keys()))
    periodo = periodos[periodo_seleccionado]
    monto_invertir = st.number_input("Monto a invertir por ETF (USD):", min_value=0.0, step=1.0)

# Función para calcular rendimiento y riesgo
def calcular_rendimiento_riesgo(etf_symbol, period):
    data = yf.Ticker(etf_symbol).history(period=period)
    if data.empty:
        return None, None
    precio_inicial = data['Close'].iloc[0]
    precio_final = data['Close'].iloc[-1]
    rendimiento = ((precio_final / precio_inicial) - 1) * 100
    retornos_diarios = data['Close'].pct_change().dropna()
    volatilidad = retornos_diarios.std() * (252 ** 0.5) * 100
    return {
        "ETF": etf_symbol,
        "Rendimiento Total (%)": round(rendimiento, 2),
        "Riesgo (Desviación Estándar Anualizada) (%)": round(volatilidad, 2)
    }, data['Close']

# Resultados
with tabs[2]:
    if st.button("Calcular y Comparar Rendimiento y Riesgo"):
        if etf_symbols:
            resultados = []
            datos_graficos = pd.DataFrame()

            for etf in etf_symbols:
                resultado, data_periodo = calcular_rendimiento_riesgo(etf, periodo)
                if resultado:
                    resultados.append(resultado)
                    datos_graficos[etf] = data_periodo

            if resultados:
                resultados_df = pd.DataFrame(resultados)
                st.write("Resultados Comparativos de Rendimiento y Riesgo:")
                st.table(resultados_df)

# Recomendaciones por perfil
with tabs[3]:
    st.header("Recomendaciones Basadas en Perfil de Inversión")
    monto = st.number_input("Monto total a invertir (USD):", min_value=0.0, step=1.0)
    perfil = st.selectbox("Selecciona tu perfil de inversión:", ["Seguro", "Óptimo", "Riesgo"])

    if monto > 0 and perfil:
        st.subheader(f"Recomendaciones para el perfil **{perfil}**")

        # Análisis de ETFs y asignación según perfil
        etf_resultados = []
        for etf in ETFs_Data:
            resultado, _ = calcular_rendimiento_riesgo(etf['simbolo'], "1y")  # Análisis de 1 año por defecto
            if resultado:
                etf_resultados.append({
                    "ETF": etf['nombre'],
                    "Rendimiento": resultado["Rendimiento Total (%)"],
                    "Riesgo": resultado["Riesgo (Desviación Estándar Anualizada) (%)"],
                    "Simbolo": etf['simbolo'],
                    "Descripcion": etf['descripcion']
                })

        etf_resultados_df = pd.DataFrame(etf_resultados)

        # Selección según perfil
        if perfil == "Seguro":
            seleccion = etf_resultados_df[etf_resultados_df["Riesgo"] < 15].sort_values(by="Rendimiento", ascending=False)
        elif perfil == "Óptimo":
            seleccion = etf_resultados_df[(etf_resultados_df["Riesgo"] >= 15) & (etf_resultados_df["Riesgo"] <= 30)].sort_values(by="Rendimiento", ascending=False)
        elif perfil == "Riesgo":
            seleccion = etf_resultados_df[etf_resultados_df["Riesgo"] > 30].sort_values(by="Rendimiento", ascending=False)

        # Asignación del monto según perfil
        seleccion["Porcentaje Asignado (%)"] = [50, 30, 20][:len(seleccion)]
        seleccion["Monto Asignado (USD)"] = seleccion["Porcentaje Asignado (%)"] * monto / 100

        # Mostrar resultados
        st.write("### Distribución de Inversión")
        st.table(seleccion[["ETF", "Descripcion", "Porcentaje Asignado (%)", "Monto Asignado (USD)"]])

        # Gráficos para visualizar la distribución de inversión
        st.write("### Visualización de Distribución por ETF")
        fig_bar = px.bar(
            seleccion,
            x="ETF",
            y="Monto Asignado (USD)",
            color="Porcentaje Asignado (%)",
            title="Distribución de Inversión por ETF",
            labels={"Monto Asignado (USD)": "Monto en USD"}
        )
        st.plotly_chart(fig_bar)

        # Gráfico de pastel
        fig_pie = px.pie(
            seleccion,
            names="ETF",
            values="Monto Asignado (USD)",
            title="Proporción de Inversión por ETF",
            hole=0.3
        )
        st.plotly_chart(fig_pie)
    
