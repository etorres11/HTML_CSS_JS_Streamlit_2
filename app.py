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

import streamlit as st
# dedent elimina la sangría del texto multilínea para que HTML no se muestre como código.
from textwrap import dedent

st.set_page_config(page_title="HTML 1", page_icon="🛢️", layout="centered")

# st.markdown inserta contenido en la app. Con unsafe_allow_html=True puede renderizar HTML/CSS.
st.markdown(dedent("""
<style>
/* ==========================================================
   GUÍA RÁPIDA DE CSS
   ==========================================================
   selector        = indica qué elemento queremos modificar.
   background      = cambia el fondo.
   color           = cambia el color del texto.
   border          = crea un borde.
   border-radius   = redondea las esquinas.
   overflow:hidden = recorta lo que sobresale de la tarjeta.
   clip-path       = fuerza la forma curva del contorno.
   padding         = espacio DENTRO del elemento.
   margin          = espacio FUERA del elemento.
   box-shadow      = crea una sombra o brillo.
   transition      = hace suave un cambio visual.
   transform       = mueve, gira o escala un elemento.
   :hover          = estilo usado cuando el cursor está encima.
   ========================================================== */

.stApp{background:#12304A;color:#F7FBFF;}
h1,h2,h3,p,label{color:#F7FBFF !important;}
.hero-card{
    border:2px solid rgba(32,230,199,.60);
    border-radius:30px; overflow:hidden; clip-path: inset(0 round 30px);
    padding:26px; background:#1B476B;
    box-shadow:0 16px 38px rgba(4,18,29,.22);
    transition:transform .22s ease, box-shadow .22s ease;
}
.hero-card:hover{transform:translateY(-4px); box-shadow:0 18px 42px rgba(32,230,199,.18);}
.accent{color:#20E6C7;font-weight:800;}
</style>
"""), unsafe_allow_html=True)

st.markdown(dedent("""

<!-- ========================================================
     GUÍA RÁPIDA DE HTML
     div   = caja o contenedor.
     h1    = título principal.
     h2/h3 = subtítulos.
     p     = párrafo.
     span  = permite aplicar estilo solo a una parte del texto.
     class = conecta un elemento HTML con una regla CSS.
     ======================================================== -->
<div class="hero-card">
    <h1>Oil & Gas Production Dashboard</h1>
    <p>
        HTML permite estructurar un encabezado visualmente más limpio y profesional.
        En este caso presentamos un panel educativo de
        <span class="accent">producción</span>,
        <span class="accent">Water Cut</span>
        e
        <span class="accent">ingreso bruto estimado</span>.
    </p>
</div>
"""), unsafe_allow_html=True)

oil_bopd = st.slider("Producción de petróleo [BOPD]", 100, 5000, 1200, 50)
water_bwpd = st.slider("Producción de agua [BWPD]", 0, 5000, 600, 50)

st.info("Aquí HTML estructura el bloque principal. No se muestra código HTML en pantalla.")
