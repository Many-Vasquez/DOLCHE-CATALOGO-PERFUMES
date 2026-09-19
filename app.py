import streamlit as st

# Configuración de la página web de la app
st.set_page_config(page_title="Dolchē - Perfumería Fina & Exclusiva", page_icon="✨", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS (Boutique de Lujo) ---
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
        padding: 20px;
    }
    .price-tag {
        color: #9c7c38;
        font-size: 1.3rem;
        font-weight: 700;
    }
    .brand-subtitle {
        color: #7a6e65;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .perfume-title {
        color: #2b221e;
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 15px;
        min-height: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS MAESTRA AMPLIADA (Mapeo Completo) ---
CATALOGO_OFICIAL = [
    # Dama
    {"Nombre": "Orientica Royal Amber 2.7oz Eau de Parfum", "Precio Venta MXN": 1798.20, "Categoria": "Dama"},
    {"Nombre": "Jean Paul Gaultier La Belle Rosea .2oz Mini edp for Women", "Precio Venta MXN": 574.20, "Categoria": "Dama"},
    {"Nombre": "Prada Paradoxe Intense .23oz Mini Eau de Parfum", "Precio Venta MXN": 934.20, "Categoria": "Dama"},
    {"Nombre": "Alien Extra Intense .2oz Edp Mini By Thierry Mugler", "Precio Venta MXN": 574.20, "Categoria": "Dama"},
    {"Nombre": "Alien Goddess Int .2oz Mini Eau de Parfum By Thierry Mugler", "Precio Venta MXN": 574.20, "Categoria": "Dama"},
    {"Nombre": "212 Heroes For Her .34oz Mini Edp By Carolina Herrera", "Precio Venta MXN": 826.20, "Categoria": "Dama"},
    {"Nombre": "Good Girl Blush .24oz Mini Edp By Carolina Herrera", "Precio Venta MXN": 826.20, "Categoria": "Dama"},
    {"Nombre": "Good Girl Supreme .24oz Mini Edp By Carolina Herrera", "Precio Venta MXN": 826.20, "Categoria": "Dama"},
    {"Nombre": "Good Girl .24oz Mini Edp By Carolina Herrera", "Precio Venta MXN": 826.20, "Categoria": "Dama"},
    {"Nombre": "Very Good Girl .24oz Mini Edp By Carolina Herrera", "Precio Venta MXN": 826.20, "Categoria": "Dama"},
    {"Nombre": "Gucci Flora Gorgeous Orchid 3.3oz Eau de Parfum", "Precio Venta MXN": 2482.20, "Categoria": "Dama"},
    {"Nombre": "Burberry Goddess 3.3oz Eau de Parfum", "Precio Venta MXN": 2338.20, "Categoria": "Dama"},
    {"Nombre": "Lattafa Yara 3.4oz Eau de Parfum", "Precio Venta MXN": 934.20, "Categoria": "Dama"},
    {"Nombre": "Lattafa Yara Tous 3.4oz Eau de Parfum", "Precio Venta MXN": 934.20, "Categoria": "Dama"},
    {"Nombre": "Lattafa Yara Moi 3.4oz Eau de Parfum", "Precio Venta MXN": 934.20, "Categoria": "Dama"},
    {"Nombre": "Club de Nuit Woman 3.6oz Eau de Parfum By Armaf", "Precio Venta MXN": 1150.20, "Categoria": "Dama"},
    {"Nombre": "Ariana Grande Cloud 3.4oz Eau de Parfum", "Precio Venta MXN": 1582.20, "Categoria": "Dama"},
    {"Nombre": "Ariana Grande Thank U Next 3.4oz Eau de Parfum", "Precio Venta MXN": 1582.20, "Categoria": "Dama"},
    {"Nombre": "Billie Eilish Eilish No. 1 3.4oz Eau de Parfum", "Precio Venta MXN": 1942.20, "Categoria": "Dama"},
    {"Nombre": "Chanel Coco Mademoiselle 3.4oz Eau de Parfum", "Precio Venta MXN": 3598.20, "Categoria": "Dama"},
    {"Nombre": "Lancome La Vie Est Belle 3.4oz Eau de Parfum", "Precio Venta MXN": 2878.20, "Categoria": "Dama"},
    {"Nombre": "Yves Saint Laurent Libre 3.0oz Eau de Parfum", "Precio Venta MXN": 2988.20, "Categoria": "Dama"},
    {"Nombre": "Dior J'adore 3.4oz Eau de Parfum", "Precio Venta MXN": 3238.20, "Categoria": "Dama"},
    {"Nombre": "Carolina Herrera Herrera Good Girl Legere 2.7oz", "Precio Venta MXN": 2698.20, "Categoria": "Dama"},
    {"Nombre": "Marc Jacobs Daisy 3.4oz Eau de Toilette", "Precio Venta MXN": 2158.20, "Categoria": "Dama"},
    {"Nombre": "Versace Bright Crystal 3.0oz Eau de Toilette", "Precio Venta MXN": 1798.20, "Categoria": "Dama"},
    {"Nombre": "Dolce & Gabbana Light Blue 3.3oz Edt", "Precio Venta MXN": 1978.20, "Categoria": "Dama"},
    
    # Caballero
    {"Nombre": "Acqua Di Gio Parfum 2.5oz Parfum By Giorgio Armani", "Precio Venta MXN": 2338.20, "Categoria": "Caballero"},
    {"Nombre": "Bad Boy Cobalt .27oz Mini Edp By Carolina Herrera", "Precio Venta MXN": 826.20, "Categoria": "Caballero"},
    {"Nombre": "Bad Boy .27oz Mini Edt By Carolina Herrera", "Precio Venta MXN": 826.20, "Categoria": "Caballero"},
    {"Nombre": "212 Men .34oz Mini Edt By Carolina Herrera", "Precio Venta MXN": 826.20, "Categoria": "Caballero"},
    {"Nombre": "Eros Energy 3.4oz Eau de Parfum By Versace", "Precio Venta MXN": 2338.20, "Categoria": "Caballero"},
    {"Nombre": "Eros Flame 3.4oz Eau de Parfum By Versace", "Precio Venta MXN": 2158.20, "Categoria": "Caballero"},
    {"Nombre": "Asad 3.4oz Eau de Parfum By Lattafa", "Precio Venta MXN": 934.20, "Categoria": "Caballero"},
    {"Nombre": "Khamrah Qahwa 3.4oz Eau de Parfum By Lattafa", "Precio Venta MXN": 1150.20, "Categoria": "Caballero"},
    {"Nombre": "Club de Nuit Intense Man 3.6oz Edp By Armaf", "Precio Venta MXN": 1258.20, "Categoria": "Caballero"},
    {"Nombre": "Bleu de Chanel 3.4oz Eau de Parfum", "Precio Venta MXN": 3598.20, "Categoria": "Caballero"},
    {"Nombre": "Dior Sauvage 3.4oz Eau de Toilette", "Precio Venta MXN": 2878.20, "Categoria": "Caballero"},
    {"Nombre": "Dior Sauvage Elixir 2.0oz", "Precio Venta MXN": 3958.20, "Categoria": "Caballero"},
    {"Nombre": "Versace Eros 3.4oz Eau de Toilette", "Precio Venta MXN": 1978.20, "Categoria": "Caballero"},
    {"Nombre": "Paco Rabanne 1 Million 3.4oz Eau de Toilette", "Precio Venta MXN": 2338.20, "Categoria": "Caballero"},
    {"Nombre": "Paco Rabanne Invictus 3.4oz Eau de Toilette", "Precio Venta MXN": 2338.20, "Categoria": "Caballero"},
    {"Nombre": "Jean Paul Gaultier Le Male Le Parfum 4.2oz", "Precio Venta MXN": 2698.20, "Categoria": "Caballero"},
    {"Nombre": "Dolce & Gabbana The One For Men 3.3oz Edt", "Precio Venta MXN": 1978.20, "Categoria": "Caballero"},
    {"Nombre": "Tom Ford Ombre Leather 3.4oz Eau de Parfum", "Precio Venta MXN": 3958.20, "Categoria": "Caballero"},

    # Conjuntos (Sets)
    {"Nombre": "Good Girl Gift Set By Carolina Herrera (Edp 2.7oz + Body Lotion)", "Precio Venta MXN": 2878.20, "Categoria": "Conjuntos"},
    {"Nombre": "Eros Gift Set By Versace (Edt 3.4oz + Travel Spray + Pouch)", "Precio Venta MXN": 2518.20, "Categoria": "Conjuntos"},
    {"Nombre": "Bleu de Chanel Gift Set (Edp 3.4oz + Deodorant Stick)", "Precio Venta MXN": 3418.20, "Categoria": "Conjuntos"},
    {"Nombre": "Sauvage Gift Set By Dior (Edt 3.4oz + Shower Gel)", "Precio Venta MXN": 3238.20, "Categoria": "Conjuntos"},
    {"Nombre": "Libre Gift Set By Yves Saint Laurent (Edp + Mini Travel)", "Precio Venta MXN": 3118.20, "Categoria": "Conjuntos"},

    # Kids
    {"Nombre": "Disney Frozen II Kids 3.4oz Eau de Toilette", "Precio Venta MXN": 538.20, "Categoria": "Kids"},
    {"Nombre": "Spider-Man Marvel Kids 3.4oz Eau de Toilette", "Precio Venta MXN": 538.20, "Categoria": "Kids"},
    {"Nombre": "Hello Kitty Sweet Pink 3.4oz Eau de Toilette", "Precio Venta MXN": 538.20, "Categoria": "Kids"},
    {"Nombre": "Minions Kids 3.4oz Eau de Toilette", "Precio Venta MXN": 538.20, "Categoria": "Kids"},
    {"Nombre": "Barbie Pink Glam Kids 3.4oz Eau de Toilette", "Precio Venta MXN": 538.20, "Categoria": "Kids"}
]

# --- ENCABEZADO DE LA APP ---
st.title("✨ Dolchē — Perfumería Fina & Exclusiva")
st.markdown("<p class='brand-subtitle'>Catálogo oficial de fragancias importadas de alta gama</p>", unsafe_allow_html=True)
st.divider()

# --- SEPARAR POR CATEGORÍAS EXACTAS ---
cat_dama = [p for p in CATALOGO_OFICIAL if p['Categoria'] == 'Dama']
cat_caballero = [p for p in CATALOGO_OFICIAL if p['Categoria'] == 'Caballero']
cat_conjunto = [p for p in CATALOGO_OFICIAL if p['Categoria'] == 'Conjuntos']
cat_kids = [p for p in CATALOGO_OFICIAL if p['Categoria'] == 'Kids']

tab_dama, tab_caballero, tab_conjunto, tab_kids = st.tabs([
    f"🌸 Dama ({len(cat_dama)})", 
    f"👔 Caballero ({len(cat_caballero)})", 
    f"🎁 Conjuntos ({len(cat_conjunto)})", 
    f"🧸 Kids ({len(cat_kids)})"
])

def renderizar_pestana(productos_lista, tab_name):
    busqueda = st.text_input(f"🔍 Búsqueda intuitiva en {tab_name}:", placeholder="Escribe cualquier parte del nombre o marca...", key=f"search_{tab_name}")
    
    if busqueda:
        filtrados = [p for p in productos_lista if busqueda.lower() in p['Nombre'].lower()]
    else:
        filtrados = productos_lista

    st.markdown(f"<p style='color: #7a6e65;'>Mostrando <b>{len(filtrados)}</b> fragancias</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not filtrados:
        st.info("No hay productos que coincidan con la búsqueda en esta categoría.")
        return

    cols_per_row = 3
    for i in range(0, len(filtrados), cols_per_row):
        row_cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(filtrados):
                prod = filtrados[i + j]
                with row_cols[j]:
                    with st.container(border=True):
                        st.markdown("✨ **Dolchē Fina**")
                        st.markdown(f"<div class='perfume-title'>{prod['Nombre']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<span class='price-tag'>${prod['Precio Venta MXN']:,.2f} MXN</span>", unsafe_allow_html=True)

with tab_dama:
    renderizar_pestana(cat_dama, "Dama")
with tab_caballero:
    renderizar_pestana(cat_caballero, "Caballero")
with tab_conjunto:
    renderizar_pestana(cat_conjunto, "Conjuntos")
with tab_kids:
    renderizar_pestana(cat_kids, "Kids")
