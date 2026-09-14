# ============================================================
# GUÍA DE LECTURA DEL SCRIPT
# ============================================================
# Python / Streamlit = recibe datos y realiza cálculos.
# HTML = define qué elementos existen en pantalla.
# CSS = define cómo se ven esos elementos.
# JavaScript = define qué sucede cuando el usuario interactúa.
#
# Los comentarios están escritos en términos simples para que
# el archivo pueda utilizarse directamente durante la clase.
# ============================================================

# Importamos Streamlit: convierte Python en una app web interactiva.
import streamlit as st

# Configura nombre de pestaña, icono y distribución de la página.
st.set_page_config(page_title="Producción Oil & Gas", page_icon="🛢️", layout="centered")

st.title("Panel básico de producción")
st.write("Versión base con Streamlit puro, sin HTML ni JavaScript.")

# slider = barra deslizante para escoger un valor.
oil_bopd = st.slider("Producción de petróleo [BOPD]", 100, 5000, 1200, 50)
# Segundo slider: mismo componente, pero para agua.
water_bwpd = st.slider("Producción de agua [BWPD]", 0, 5000, 600, 50)
# number_input = campo para ingresar un valor numérico.
oil_price = st.number_input("Precio estimado [USD/bbl]", 1.0, 200.0, 75.0, 1.0)

# button = botón. El bloque interno se ejecuta solo al presionarlo.
if st.button("Calcular indicadores", type="primary"):
    # Fluido total = petróleo + agua.
    total_fluid = oil_bopd + water_bwpd
    # Water Cut = porcentaje de agua respecto al fluido total.
    water_cut = water_bwpd / total_fluid * 100 if total_fluid else 0
    # Producción mensual aproximada = producción diaria x 30 días.
    monthly_oil = oil_bopd * 30
    # Ingreso bruto estimado = barriles mensuales x precio.
    gross_revenue = monthly_oil * oil_price

    # columns divide la pantalla en tres bloques horizontales.
    c1, c2, c3 = st.columns(3)
    c1.metric("Fluido total", f"{total_fluid:,.0f} BFPD")
    c2.metric("Water Cut", f"{water_cut:.1f}%")
    c3.metric("Ingreso mensual", f"${gross_revenue:,.0f}")
