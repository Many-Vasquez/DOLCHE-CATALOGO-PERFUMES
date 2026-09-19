import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

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
    .stButton>button {
        background: linear-gradient(135deg, #2b221e 0%, #4a3b32 100%);
        color: #f4efe6;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(43,34,30,0.15);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #b89753 0%, #d4b87a 100%);
        color: #1a1a1a;
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

URL_PRINCIPAL = "https://gpmcallen.com/"

@st.cache_data(ttl=7200)
def extraer_catalogo_por_categorias(tasa_multiplicador=36.0):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    # URLs específicas de categorías en gpmcallen basadas en su estructura de menú
    endpoints = {
        "Dama": ["", "collections/ladies-perfumes", "collections/womens-perfumes"],
        "Caballero": ["collections/mens-colognes", "collections/mens-perfumes"],
        "Conjuntos": ["collections/ladies-sets", "collections/mens-sets", "collections/gift-sets"],
        "Kids": ["collections/kids-perfumes"]
    }
    
    catalogo_general = []
    
    for categoria, rutas in endpoints.items():
        for ruta in rutas:
            url_target = URL_PRINCIPAL.rstrip('/') + '/' + ruta if ruta else URL_PRINCIPAL
            try:
                response = requests.get(url_target, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    items = soup.find_all(['div', 'li', 'article'], class_=lambda x: x and any(c in x for c in ['product', 'item', 'grid', 'card', 'col']))
                    
                    for item in items:
                        nombre_tag = item.find(['h2', 'h3', 'a', 'span'], class_=lambda x: x and ('title' in x or 'name' in x))
                        if not nombre_tag:
                            nombre_tag = item.find('a')
                        nombre = nombre_tag.text.strip() if nombre_tag else ""
                        
                        if not nombre or len(nombre) < 3:
                            continue
                        
                        # Filtro anti-basura / anti-cremas
                        n_lower = nombre.lower()
                        if any(p in n_lower for p in ['cream', 'lotion', 'gel', 'makeup', 'body wash', 'lipstick', 'skincare', 'suero', 'bioglow', 'cleaner', 'latest products']):
                            continue

                        precio_tag = item.find(['span', 'div', 'p'], class_=lambda x: x and ('price' in x or 'amount' in x))
                        precio_proveedor = 0.0
                        
                        if precio_tag:
                            precio_str = precio_tag.text.replace('$', '').replace('USD', '').replace(',', '').strip()
                            numeros = re.findall(r'\d+\.\d+|\d+', precio_str)
                            if numeros:
                                precio_proveedor = float(numeros[0])
                        
                        if precio_proveedor > 0:
                            precio_final = precio_proveedor * tasa_multiplicador
                            
                            prod_dict = {
                                "Nombre": nombre,
                                "Precio Venta MXN": round(precio_final, 2),
                                "Categoria": categoria
                            }
                            
                            if prod_dict not in catalogo_general:
                                catalogo_general.append(prod_dict)
            except:
                continue
                
    return catalogo_general

# --- ENCABEZADO DE LA APP ---
st.title("✨ Dolchē — Perfumería Fina & Exclusiva")
st.markdown("<p class='brand-subtitle'>Catálogo oficial de fragancias importadas de alta gama</p>", unsafe_allow_html=True)

col_sup1, _ = st.columns([1, 5])
with col_sup1:
    if st.button("🔄 Actualizar Catálogo"):
        st.cache_data.clear()
        st.rerun()

st.divider()

# --- CARGAR CATÁLOGO ---
with st.spinner("Sincronizando categorías y precios oficiales..."):
    catalogo = extraer_catalogo_por_categorias()

if catalogo:
    cat_dama = [p for p in catalogo if p['Categoria'] == 'Dama']
    cat_caballero = [p for p in catalogo if p['Categoria'] == 'Caballero']
    cat_conjunto = [p for p in catalogo if p['Categoria'] == 'Conjunto']
    cat_kids = [p for p in catalogo if p['Categoria'] == 'Kids']

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
        renderizar_pestana(cat_conjunto, "Conjunto")
    with tab_kids:
        renderizar_pestana(cat_kids, "Kids")
else:
    st.info("No se pudieron cargar productos en este momento. Intenta dar clic en 'Actualizar Catálogo'.")
