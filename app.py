import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Dolchē - Perfumería Fina & Exclusiva", page_icon="✨", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #fbf9f6 0%, #f4efe6 100%);
    }
    h1, h2, h3 {
        color: #2b221e;
        font-family: 'Playfair Display', serif, sans-serif;
    }
    div.stContainer {
        background-color: #ffffff;
        border-radius: 12px;
        border: 1px solid #eae2d6 !important;
        box-shadow: 0 4px 15px rgba(43,34,30,0.04);
        padding: 15px;
        text-align: center;
    }
    .price-tag {
        color: #9c7c38;
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 10px;
    }
    .brand-subtitle {
        color: #7a6e65;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .perfume-title {
        color: #2b221e;
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 10px;
        margin-bottom: 10px;
        min-height: 45px;
    }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS MAESTRA (Con campo optimizado para enlace directo del proveedor) ---
CATALOGO_MAESTRO_GPM = [
    # Sección Dama
    {
        "Nombre": "212 Heroes For Her .34oz Mini Edp By Carolina Herrera", 
        "Precio Venta MXN": 826.20, 
        "Seccion": "Dama", 
        "Imagen": "https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=400&q=80"
    },
    {
        "Nombre": "Alien Extra Intense .2oz Edp Mini By Thierry Mugler", 
        "Precio Venta MXN": 574.20, 
        "Seccion": "Dama", 
        "Imagen": "https://images.unsplash.com/photo-1594035910387-fea47794261f?auto=format&fit=crop&w=400&q=80"
    },
    {
        "Nombre": "Ariana Grande Cloud 3.4oz Eau de Parfum", 
        "Precio Venta MXN": 1582.20, 
        "Seccion": "Dama", 
        "Imagen": "https://images.unsplash.com/photo-1523293182086-7651a899d37f?auto=format&fit=crop&w=400&q=80"
    },
    {
        "Nombre": "Carolina Herrera Very Good Girl 2.7oz Edp", 
        "Precio Venta MXN": 2698.20, 
        "Seccion": "Dama", 
        "Imagen": "https://images.unsplash.com/photo-1543422967-8854067965fa?auto=format&fit=crop&w=400&q=80"
    },
    
    # Sección Caballero
    {
        "Nombre": "Acqua Di Gio Giorgio Armani 4.2oz Edt", 
        "Precio Venta MXN": 2338.20, 
        "Seccion": "Caballero", 
        "Imagen": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=400&q=80"
    },
    {
        "Nombre": "Bleu de Chanel 3.4oz Eau de Parfum", 
        "Precio Venta MXN": 3598.20, 
        "Seccion": "Caballero", 
        "Imagen": "https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=400&q=80"
    },
    {
        "Nombre": "Dior Sauvage 3.4oz Eau de Toilette", 
        "Precio Venta MXN": 2878.20, 
        "Seccion": "Caballero", 
        "Imagen": "https://images.unsplash.com/photo-1583445013765-46c20c4a6772?auto=format&fit=crop&w=400&q=80"
    },

    # Sección Kids
    {
        "Nombre": "Barbie Pink Eau de Toilette for Kids 3.4oz", 
        "Precio Venta MXN": 590.00, 
        "Seccion": "Kids", 
        "Imagen": "https://images.unsplash.com/photo-1595425970377-c9703cf48b6d?auto=format&fit=crop&w=400&q=80"
    },
    {
        "Nombre": "Disney Frozen II Eau de Toilette Set for Kids", 
        "Precio Venta MXN": 650.00, 
        "Seccion": "Kids", 
        "Imagen": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=400&q=80"
    },

    # Sección Conjuntos
    {
        "Nombre": "1 Million Gift Set By Paco Rabanne (Edt 3.4oz + Travel Spray)", 
        "Precio Venta MXN": 2698.20, 
        "Seccion": "Conjuntos", 
        "Imagen": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=400&q=80"
    },
    {
        "Nombre": "Sauvage Gift Set By Dior (Edt 3.4oz + Shower Gel)", 
        "Precio Venta MXN": 3238.20, 
        "Seccion": "Conjuntos", 
        "Imagen": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=400&q=80"
    }
]

# --- FUNCIÓN DE FILTRADO ---
def buscar_por_seccion_y_alfabeto(seccion_buscada, termino=""):
    resultados = [p for p in CATALOGO_MAESTRO_GPM if p['Seccion'].lower() == seccion_buscada.lower()]
    if termino:
        resultados = [p for p in resultados if termino.lower() in p['Nombre'].lower()]
    return sorted(resultados, key=lambda x: x['Nombre'])

# --- ENCABEZADO ---
st.title("✨ Dolchē — Perfumería Fina & Exclusiva")
st.markdown("<p class='brand-subtitle'>Catálogo oficial sincronizado con galería visual</p>", unsafe_allow_html=True)
st.divider()

# --- PESTAÑAS ---
cat_dama = buscar_por_seccion_y_alfabeto("Dama")
cat_caballero = buscar_por_seccion_y_alfabeto("Caballero")
cat_kids = buscar_por_seccion_y_alfabeto("Kids")
cat_conjuntos = buscar_por_seccion_y_alfabeto("Conjuntos")

tab_dama, tab_caballero, tab_kids, tab_conjuntos = st.tabs([
    f"🌸 Dama ({len(cat_dama)})", 
    f"👔 Caballero ({len(cat_caballero)})", 
    f"🧸 Kids ({len(cat_kids)})",
    f"🎁 Conjuntos ({len(cat_conjuntos)})"
])

def renderizar_pestana(seccion_nombre, tab_key):
    busqueda = st.text_input(f"🔍 Búsqueda rápida en {seccion_nombre}:", placeholder="Escribe el nombre del perfume...", key=f"search_{tab_key}")
    filtrados = buscar_por_seccion_y_alfabeto(seccion_nombre, busqueda)

    st.markdown(f"<p style='color: #7a6e65;'>Mostrando <b>{len(filtrados)}</b> artículos ordenados alfabéticamente</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not filtrados:
        st.info("No se encontraron coincidencias en esta sección.")
        return

    cols_per_row = 3
    for i in range(0, len(filtrados), cols_per_row):
        row_cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(filtrados):
                prod = filtrados[i + j]
                with row_cols[j]:
                    with st.container(border=True):
                        st.image(prod['Imagen'], use_container_width=True)
                        st.markdown("<div class='brand-subtitle' style='margin-top: 8px;'>Dolchē Fina</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='perfume-title'>{prod['Nombre']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='price-tag'>${prod['Precio Venta MXN']:,.2f} MXN</div>", unsafe_allow_html=True)

with tab_dama:
    renderizar_pestana("Dama", "dama")
with tab_caballero:
    renderizar_pestana("Caballero", "caballero")
with tab_kids:
    renderizar_pestana("Kids", "kids")
with tab_conjuntos:
    renderizar_pestana("Conjuntos", "conjuntos")
