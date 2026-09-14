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

# Streamlit crea controles, organiza la pantalla y ejecuta los cálculos.
import streamlit as st
# components permite incluir una zona con HTML/CSS/JavaScript.
import streamlit.components.v1 as components
# dedent elimina sangría del HTML para que Streamlit lo renderice correctamente.
from textwrap import dedent

st.set_page_config(page_title="Oil & Gas Production Dashboard", page_icon="🛢️", layout="wide")

# Color del fondo general.
FONDO = "#12304A"
# Color usado en las tarjetas.
SUPERFICIE = "#1B476B"
# Color neón usado para destacar información.
ACENTO = "#20E6C7"
# Color principal del texto.
TEXTO = "#F7FBFF"

st.markdown(dedent(f"""
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

.stApp{{background:{FONDO};color:{TEXTO};}}
h1,h2,h3,p,label,small{{color:{TEXTO} !important;}}
.hero{{
    border:2px solid rgba(32,230,199,.58);
    border-radius:32px !important; overflow:hidden !important; clip-path: inset(0 round 32px);
    padding:28px; background:{SUPERFICIE}; box-shadow:0 18px 42px rgba(4,18,29,.22); margin-bottom:22px;
}}
.accent{{color:{ACENTO};font-weight:800;}}
.oil-card{{
    position:relative; border:2px solid rgba(32,230,199,.58);
    border-radius:32px !important; overflow:hidden !important; clip-path: inset(0 round 32px);
    padding:26px; background:{SUPERFICIE}; box-shadow:0 16px 38px rgba(4,18,29,.24);
    transition:transform .22s ease, box-shadow .22s ease, border-color .22s ease;
}}
.oil-card::before{{
    content:""; position:absolute; inset:0; border-radius:32px;
    background:linear-gradient(135deg, rgba(32,230,199,.05), rgba(255,255,255,.01));
    pointer-events:none;
}}
.oil-card:hover{{transform:translateY(-4px); border-color:{ACENTO}; box-shadow:0 20px 48px rgba(32,230,199,.18);}}
.value{{color:{ACENTO};font-size:1.22rem;font-weight:800;}}
div.stButton > button{{
    width:100%; background:#20557E; color:{ACENTO}; border:2px solid {ACENTO};
    border-radius:18px !important; padding:.82rem 1rem; font-weight:800;
    transition:transform .2s ease, box-shadow .2s ease;
}}
div.stButton > button:hover{{transform:translateY(-2px); box-shadow:0 0 28px rgba(32,230,199,.34); color:{TEXTO};}}
div[data-testid="stMetric"]{{
    border:2px solid rgba(32,230,199,.42); border-radius:24px !important;
    overflow:hidden !important; clip-path: inset(0 round 24px); background:{SUPERFICIE}; padding:16px;
}}
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
<div class="hero">
    <h1>Oil & Gas Production Dashboard</h1>
    <p>
        Aplicación educativa para analizar
        <span class="accent">producción</span>,
        <span class="accent">Water Cut</span>
        e
        <span class="accent">ingreso bruto mensual estimado</span>
        de un pozo.
    </p>
</div>
"""), unsafe_allow_html=True)

# columns divide la interfaz en dos zonas: parámetros e interacción.
left, right = st.columns([1.05, 0.95], gap="large")

# Todo lo indentado aquí aparece en la columna izquierda.
with left:
    st.subheader("1. Parámetros operacionales")
    oil_bopd = st.slider("Producción de petróleo [BOPD]", 100, 5000, 1200, 50)
    water_bwpd = st.slider("Producción de agua [BWPD]", 0, 5000, 600, 50)
    oil_price = st.number_input("Precio estimado [USD/bbl]", 1.0, 200.0, 75.0, 1.0)

    st.markdown(dedent(f"""
    <div class="oil-card">
        <h3>Parámetros activos</h3>
        <p>Petróleo: <span class="value">{oil_bopd:,} BOPD</span></p>
        <p>Agua: <span class="value">{water_bwpd:,} BWPD</span></p>
        <p>Precio: <span class="value">${oil_price:.2f}/bbl</span></p>
        <p><small>Esta tarjeta reacciona con hover por CSS.</small></p>
    </div>
    """), unsafe_allow_html=True)

    # El botón devuelve True cuando se presiona y permite ejecutar los cálculos.
    calcular = st.button("Calcular indicadores", type="primary")

# Todo lo indentado aquí aparece en la columna derecha.
with right:
    st.subheader("2. Interacción JavaScript")
    components.html("""
    <style>
    html,body{margin:0;padding:10px;background:transparent;font-family:Arial,sans-serif;}
    .shell{
        position:relative; padding:4px; border-radius:36px; overflow:hidden;
        clip-path: inset(0 round 36px); background:#12304A; box-shadow:0 18px 46px rgba(4,18,29,.30);
    }
    .shell::before{
        content:""; position:absolute; width:180%; height:180%; left:-40%; top:-40%;
        background: conic-gradient(from 0deg, transparent 0deg 220deg, #20E6C7 275deg, #F7FBFF 320deg, transparent 360deg);
        opacity:0; transition:opacity .22s ease;
    }
    .shell.active::before{opacity:1; animation:spin 1.5s linear infinite;}
    .card{
        --x:50%; --y:50%; position:relative; z-index:1; min-height:255px;
        border-radius:32px; overflow:hidden; clip-path: inset(0 round 32px); padding:30px;
        background: radial-gradient(circle at var(--x) var(--y), rgba(32,230,199,.28), rgba(27,71,107,0) 36%), #1B476B;
        color:#F7FBFF;
    }
    .card h2{margin-top:0;color:#20E6C7;}
    .card strong{color:#20E6C7;}
    .status{margin-top:20px;padding-top:14px;border-top:1px solid rgba(32,230,199,.40);}
    @keyframes spin{to{transform:rotate(360deg);}}
    </style>

    <div id="shell" class="shell">
        <div id="card" class="card">
            <h2>Pozo A-17</h2>
            <p>Producción: <strong>1,250 BOPD</strong></p>
            <p>Water Cut: <strong>31.4%</strong></p>
            <p>El borde neón y el halo responden al movimiento del cursor.</p>
            <p id="status" class="status">Estado: cursor fuera</p>
        </div>
    </div>

    <script>
    // Buscamos los tres elementos HTML que JavaScript necesita controlar.
    const shell = document.getElementById("shell");   // contenedor del borde neón
    const card = document.getElementById("card");     // tarjeta interior
    const status = document.getElementById("status"); // texto de estado

    // mouseenter = el cursor entra al contenedor.
    shell.addEventListener("mouseenter", () => {
        // Agregamos active: CSS detecta esta clase y enciende el giro neón.
        shell.classList.add("active");
        // Cambiamos el mensaje que ve el usuario.
        status.textContent = "Estado: interacción activa";
    });

    // mouseleave = el cursor sale del contenedor.
    shell.addEventListener("mouseleave", () => {
        // Quitamos active: la animación se detiene.
        shell.classList.remove("active");
        // Restauramos el mensaje.
        status.textContent = "Estado: cursor fuera";
        // Centramos nuevamente el halo.
        card.style.setProperty("--x", "50%");
        card.style.setProperty("--y", "50%");
    });

    // mousemove = el cursor se mueve dentro de la tarjeta.
    card.addEventListener("mousemove", (event) => {
        // Obtiene posición y dimensiones de la tarjeta.
        const rect = card.getBoundingClientRect();
        // Calculamos X e Y del cursor como porcentaje.
        const x = ((event.clientX - rect.left) / rect.width) * 100;
        const y = ((event.clientY - rect.top) / rect.height) * 100;
        // Enviamos X/Y a las variables CSS --x y --y.
        card.style.setProperty("--x", x + "%");
        card.style.setProperty("--y", y + "%");
        // El radial-gradient usa esas variables y por eso la luz sigue al cursor.
    });
    </script>
    """, height=355)

# Este bloque solo se ejecuta después de presionar el botón.
if calcular:
    # Fluido total = petróleo + agua.
    total_fluid = oil_bopd + water_bwpd
    # Water Cut = porcentaje de agua dentro del fluido total.
    water_cut = water_bwpd / total_fluid * 100 if total_fluid else 0
    # Estimamos petróleo mensual usando 30 días.
    monthly_oil = oil_bopd * 30
    # Ingreso bruto = barriles mensuales x precio.
    gross_revenue = monthly_oil * oil_price

    st.subheader("3. Resultado operacional")
    # Cuatro columnas para mostrar los KPI.
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Petróleo", f"{oil_bopd:,.0f} BOPD")
    c2.metric("Fluido total", f"{total_fluid:,.0f} BFPD")
    c3.metric("Water Cut", f"{water_cut:.1f}%")
    c4.metric("Ingreso mensual", f"${gross_revenue:,.0f}")

    st.markdown(dedent(f"""
    <div class="oil-card">
        <h3>Lectura rápida</h3>
        <p>El pozo produce <span class="value">{oil_bopd:,.0f} BOPD</span> de petróleo.</p>
        <p>El Water Cut estimado es <span class="value">{water_cut:.1f}%</span>.</p>
        <p>Con un precio de <span class="value">${oil_price:.2f}/bbl</span>, el ingreso bruto mensual estimado es <span class="value">${gross_revenue:,.0f}</span>.</p>
    </div>
    """), unsafe_allow_html=True)

st.caption("Ejemplo educativo: no incluye regalías, impuestos, OPEX, transporte ni descuentos comerciales.")
