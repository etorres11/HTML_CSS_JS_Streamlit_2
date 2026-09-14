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
# components permite insertar HTML/CSS/JavaScript en Streamlit.
import streamlit.components.v1 as components

st.set_page_config(page_title="JS 3", page_icon="🛢️", layout="centered")

st.title("Halo dinámico con JavaScript")

components.html("""
<style>
/* --x y --y son variables CSS.
   JavaScript cambiará sus valores según la posición del cursor.
   radial-gradient usa esas coordenadas para dibujar el halo. */
html,body{
    margin:0; padding:10px; background:transparent; font-family:Arial,sans-serif;
}
.card{
    --x:50%; --y:50%;
    border:2px solid rgba(32,230,199,.65);
    border-radius:32px; overflow:hidden; clip-path: inset(0 round 32px);
    padding:30px;
    background:
        radial-gradient(circle at var(--x) var(--y), rgba(32,230,199,.32), rgba(27,71,107,0) 38%),
        #1B476B;
    color:#F7FBFF; box-shadow:0 16px 40px rgba(4,18,29,.26);
}
.card strong{color:#20E6C7;}
</style>

<div id="card" class="card">
    <h2>Pozo productor</h2>
    <p>Petróleo: <strong>1,450 BOPD</strong></p>
    <p>Mueva el cursor dentro de la tarjeta.</p>
</div>

<script>
// Buscamos la tarjeta por su id.
const card = document.getElementById("card");

// mousemove se ejecuta continuamente mientras el cursor se mueve dentro de la tarjeta.
card.addEventListener("mousemove", (event) => {
    // getBoundingClientRect obtiene posición, ancho y alto reales de la tarjeta.
    const rect = card.getBoundingClientRect();

    // clientX = posición horizontal del cursor.
    // Convertimos esa posición a porcentaje dentro de la tarjeta.
    const x = ((event.clientX - rect.left) / rect.width) * 100;

    // clientY = posición vertical del cursor.
    const y = ((event.clientY - rect.top) / rect.height) * 100;

    // setProperty cambia una variable CSS desde JavaScript.
    card.style.setProperty("--x", x + "%");
    card.style.setProperty("--y", y + "%");

    // Como radial-gradient usa --x y --y, la luz parece seguir al mouse.
});
</script>
""", height=245)
