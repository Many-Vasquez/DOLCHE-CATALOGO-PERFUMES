import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Configuración de la página web de la app
st.set_page_config(page_title="Dolchē - Perfumería Fina", page_icon="✨", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS (Estética de Perfumería) ---
st.markdown("""
    <style>
    .main {
        background-color: #faf8f5;
    }
    h1 {
        color: #2c221e;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        letter-spacing: -1px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #2c221e 0%, #4a3b32 100%);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #bfa15f 0%, #d4b87a 100%);
        color: #1a1a1a;
    }
    div.product-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #f0e6dc;
        text-align: center;
        margin-bottom: 20px;
        height: 100%;
    }
    .price-tag {
        color: #bfa15f;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .cost-tag {
        color: #8c827b;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

URL_PROVEEDOR = "https://gpmcallen.com/"

@st.cache_data(ttl=3600)
def extraer_catalogo_dolche(tasa_multiplicador=36.0):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(URL_PROVEEDOR, headers=headers)
        if response.status_code != 200:
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        productos = []
        
        items = soup.find_all(['div', 'li', 'article'], class_=lambda x: x and ('product' in x or 'item' in x or 'grid-item' in x))
        if not items:
            items = soup.find_all('div', class_='product-item')

        for item in items:
            nombre_tag = item.find(['h2', 'h3', 'a', 'span'], class_=lambda x: x and ('title' in x or 'name' in x))
            if not nombre_tag:
                nombre_tag = item.find('a')
            nombre = nombre_tag.text.strip() if nombre_tag else "Perfume sin nombre"
            
            if len(nombre) < 2:
                continue

            img_tag = item.find('img')
            imagen = ""
            if img_tag:
                imagen = (
                    img_tag.get('src') or 
                    img_tag.get('data-src') or 
                    img_tag.get('data-lazy-src') or 
                    img_tag.get('srcset') or 
                    ""
                )
                if ',' in imagen:
                    imagen = imagen.split(',')[0].strip().split(' ')[0]
                
                if imagen.startswith('//'):
                    imagen = "https:" + imagen
                elif imagen.startswith('/'):
                    imagen = "https://gpmcallen.com" + imagen

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
                    "Imagen_URL": imagen,
                    "Nombre": nombre,
                    "Costo USD": round(precio_proveedor, 2),
                    "Precio Venta MXN": round(precio_final, 2)
                }
                if prod_dict not in productos:
                    productos.append(prod_dict)
                
        return productos
    except Exception as e:
        return []

# --- ENCABEZADO DE LA APP ---
st.title("✨ Dolchē — Perfumería Fina & Exclusiva")
st.markdown("Catálogo en tiempo real sincronizado con el proveedor. Conversión aplicada con factor directo **x36**.")

# Barra superior de acciones
col_btn1, col_btn2 = st.columns([1, 4])
with col_btn1:
    if st.button("🔄 Sincronizar Catálogo"):
        st.cache_data.clear()
        st.rerun()

st.divider()

with st.spinner("Preparando esencias y calculando precios exclusivos..."):
    catalogo = extraer_catalogo_dolche()

if catalogo:
    busqueda = st.text_input("🔍 Buscar fragancia por nombre o marca:")
    
    if busqueda:
        catalogo_filtrado = [p for p in catalogo if busqueda.lower() in p['Nombre'].lower()]
    else:
        catalogo_filtrado = catalogo

    st.markdown(f"**Fragancias disponibles:** `{len(catalogo_filtrado)}`")
    st.markdown("<br>", unsafe_allow_html=True)

    # Mostrar en formato de cuadrícula (Grid de 3 columnas)
    cols_per_row = 3
    for i in range(0, len(catalogo_filtrado), cols_per_row):
        row_cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(catalogo_filtrado):
                prod = catalogo_filtrado[i + j]
                with row_cols[j]:
                    with st.container(border=True):
                        if prod['Imagen_URL'] and prod['Imagen_URL'].startswith('http'):
                            try:
                                st.image(prod['Imagen_URL'], use_column_width=True)
                            except:
                                st.markdown("*(Imagen no disponible)*")
                        else:
                            st.markdown("✨ *(Dolchē)*")
                        
                        st.markdown(f"**{prod['Nombre']}**")
                        st.markdown(f"<span class='cost-tag'>Costo Proveedor: ${prod['Costo USD']} USD</span>", unsafe_allow_html=True)
                        st.markdown(f"<span class='price-tag'>Precio Venta: ${prod['Precio Venta MXN']} MXN</span>", unsafe_allow_html=True)
else:
    st.info("No se pudieron cargar productos en este momento. Intenta sincronizar de nuevo.")
