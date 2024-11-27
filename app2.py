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
tabs = st.tabs(["Información del Cliente", "Análisis de ETFs", "Resultados"])

# Información Personal del Cliente
with tabs[0]:
    # Verificar si los datos han sido guardados
    if 'datos_guardados' in st.session_state and st.session_state.datos_guardados:
        st.header("Datos Guardados Correctamente")
        if st.button("Editar Información"):
            # Reiniciar los campos y la sesión
            st.session_state.datos_guardados = False  # Para poder editar nuevamente
            st.session_state.nombre_cliente = ""
            st.session_state.edad_cliente = 0
            st.session_state.genero_cliente = "Masculino"  # Establecer un valor predeterminado
            st.session_state.direccion_cliente = ""
            st.session_state.pais_cliente = ""
            st.session_state.nacionalidad_cliente = ""
            st.session_state.ocupacion_cliente = ""
            
    else:
        st.header("Información Personal del Cliente")
        nombre = st.text_input("Nombre:", value=st.session_state.get("nombre_cliente", ""))
        edad = st.number_input("Edad:", min_value=0, max_value=150, value=st.session_state.get("edad_cliente", 0))
        
        # Seleccionar género
        genero_opciones = ["Masculino", "Femenino", "Otro"]
        genero = st.selectbox("Género:", genero_opciones, index=genero_opciones.index(st.session_state.get("genero_cliente", "Masculino")) if st.session_state.get("genero_cliente") in genero_opciones else 0)

        direccion = st.text_input("Dirección:", value=st.session_state.get("direccion_cliente", ""))
        pais = st.text_input("País:", value=st.session_state.get("pais_cliente", ""))
        nacionalidad = st.text_input("Nacionalidad:", value=st.session_state.get("nacionalidad_cliente", ""))
        ocupacion = st.text_input("Ocupación:", value=st.session_state.get("ocupacion_cliente", ""))

        # Guardar la información del cliente
        if st.button("Guardar Información"):
            st.session_state.nombre_cliente = nombre
            st.session_state.edad_cliente = edad
            st.session_state.genero_cliente = genero
            st.session_state.direccion_cliente = direccion
            st.session_state.pais_cliente = pais
            st.session_state.nacionalidad_cliente = nacionalidad
            st.session_state.ocupacion_cliente = ocupacion
            
            # Marcar que los datos han sido guardados
            st.session_state.datos_guardados = True
             

# Análisis de ETFs (Pestaña 2)
with tabs[1]:
    # Mostrar mensaje de bienvenida con todos los datos del cliente si la información está guardada
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

    # Nuevos campos para definir porcentajes optimista y pesimista
    porcentaje_optimista = st.number_input("Porcentaje de Rendimiento Optimista (%):", value=20, step=1)
    porcentaje_pesimista = st.number_input("Porcentaje de Rendimiento Pesimista (%):", value=20, step=1)

    st.header("ETFS")
    # Mostrar tabla con descripciones de los ETFs seleccionados
    if etfs_seleccionados:
        descripciones_df = pd.DataFrame({
            "Nombre del ETF": [etf["nombre"] for etf in ETFs_Data if etf["nombre"] in etfs_seleccionados],
            "Descripción": [etf["descripcion"] for etf in ETFs_Data if etf["nombre"] in etfs_seleccionados]
        })
        st.write("### Descripción de los ETFs Seleccionados")
        st.table(descripciones_df)

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

                # Comparación de Escenarios
                escenarios_dfs = []
                texto_escenarios = ""  # Variable para almacenar el texto de comparación

                for res in resultados:
                    rendimiento_total = res["Rendimiento Total (%)"]
                    retorno_inversion = (monto_invertir * rendimiento_total) / 100

                    # Escenarios usando los porcentajes seleccionados por el usuario
                    rendimiento_optimista = rendimiento_total + porcentaje_optimista
                    rendimiento_neutro = rendimiento_total
                    rendimiento_pesimista = rendimiento_total - porcentaje_pesimista

                    # Calcular retornos para cada escenario
                    escenarios_dfs.append({
                        "ETF": res["ETF"],
                        "Optimista": round((monto_invertir * rendimiento_optimista) / 100, 2),
                        "Neutro": round(retorno_inversion, 2),
                        "Pesimista": round((monto_invertir * rendimiento_pesimista) / 100, 2)
                    })

                    # Agregar información al texto comparativo
                    texto_escenarios += (
                        f"\n**{res['ETF']}**\n"
                        f"- Optimista: ${round((monto_invertir * rendimiento_optimista) / 100, 2)}\n"
                        f"- Neutro: ${round(retorno_inversion, 2)}\n"
                        f"- Pesimista: ${round((monto_invertir * rendimiento_pesimista) / 100, 2)}\n"
                    )

                # Crear DataFrame para los escenarios y mostrar tabla
                escenarios_df = pd.DataFrame(escenarios_dfs)
                st.write("### Tabla de Comparación de Retornos Estimados en Diferentes Escenarios")
                st.table(escenarios_df)  # Mostramos la tabla de escenarios aquí

                # Mostrar texto comparativo de los escenarios en formato horizontal
                st.write("### Comparación de Retornos Estimados por ETF y Escenario")
                num_etfs = len(resultados)  # Total de ETFs
                num_filas = (num_etfs + 2) // 3  # Calcula cuántas filas serán necesarias (3 ETFs por fila)

                for i in range(num_filas):
                    cols = st.columns(3)  # Crear 3 columnas por fila
                    for j in range(3):
                        etf_index = i * 3 + j  # Índice del ETF en la lista de resultados
                        if etf_index < num_etfs:
                            res = resultados[etf_index]
                            cols[j].markdown(
                                f"**{res['ETF']}**\n\n"
                                f"- **Optimista**: ${round((monto_invertir * (res['Rendimiento Total (%)'] + porcentaje_optimista)) / 100, 2)}\n"
                                f"- **Neutro**: ${round((monto_invertir * res['Rendimiento Total (%)']) / 100, 2)}\n"
                                f"- **Pesimista**: ${round((monto_invertir * (res['Rendimiento Total (%)'] - porcentaje_pesimista)) / 100, 2)}"
                            )

                # Gráfico de los escenarios
                fig_escenarios = px.bar(
                    escenarios_df.melt(id_vars="ETF", var_name="Escenario", value_name="Retorno Estimado (USD)"),
                    x="ETF", y="Retorno Estimado (USD)", color="Escenario",
                    barmode="group", title="Comparación de Retornos Estimados por ETF y Escenario"
                )
                st.plotly_chart(fig_escenarios)

                # Gráfica de todos los precios de cierre en una sola gráfica
                datos_graficos.reset_index(inplace=True)
                datos_graficos = datos_graficos.melt(id_vars=["Date"], var_name="ETF", value_name="Precio de Cierre")
                fig = px.line(datos_graficos, x="Date", y="Precio de Cierre", color="ETF",
                    title=f"Comparación de Precios de Cierre de ETFs Seleccionados en {periodo_seleccionado}",
                    labels={"Date": "Fecha", "Precio de Cierre": "Precio de Cierre (USD)"})
                fig.update_layout(template="plotly_dark", title_font=dict(size=20), title_x=0.5)
                fig.update_yaxes(range=[0, 1000])
                st.plotly_chart(fig)

                # Gráfico de Volatilidad de los ETFs (lineal)
                fig_volatilidad = px.bar(resultados_df, x="ETF", y="Riesgo (Desviación Estándar Anualizada) (%)",
                    title="Volatilidad de los ETFs Seleccionados",
                    labels={"Riesgo (Desviación Estándar Anualizada) (%)": "Volatilidad (%)"})
                fig_volatilidad.update_layout(title_font=dict(size=20), title_x=0.5)
                st.plotly_chart(fig_volatilidad)

                # Gráfico de Rendimiento de los ETFs (lineal)
                fig_rendimiento = px.bar(resultados_df, x="ETF", y="Rendimiento Total (%)",
                    title="Rendimiento Total de los ETFs Seleccionados",
                    labels={"Rendimiento Total (%)": "Rendimiento (%)"})
                fig_rendimiento.update_layout(title_font=dict(size=20), title_x=0.5)
                st.plotly_chart(fig_rendimiento)
            else:
                st.write("No se encontraron resultados para los ETFs seleccionados.")