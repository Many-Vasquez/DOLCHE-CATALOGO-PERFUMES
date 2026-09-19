import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Configuración de la página web de la app
st.set_page_config(page_title="Dolchē - Perfumería Fina & Exclusiva", page_icon="✨", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS (Boutique de Lujo) ---
st.markdown("""
    <style>
    /* Fondo general estilo boutique / perfumería fina */
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
        padding: 0.5rem 1.2rem;
        border: none;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 10px rgba(43,34,30,0.15);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #b89753 0%, #d4b87a 100%);
        color: #1a1a1a;
    }
    /* Estilo elegante para el buscador */
    div[data-baseweb="input"] {
        border-radius: 8px;
        border-color: #d4b87a !important;
        background-color: #ffffff;
    }
    /* Tarjetas de productos limpias y con sombra suave */
    div.stContainer {
        background-color: #ffffff;
        border-radius: 12px;
        border: 1px solid #eae2d6 !important;
        box-shadow: 0 6px 20px rgba(43,34,30,0.04);
        padding: 15px;
    }
    .price-tag {
        color: #9c7c38;
        font-size: 1.3rem;
        font-weight: 700;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .brand-subtitle {
        color: #7a6e65;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
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
                    "Precio Venta MXN": round(precio_final, 2)
                }
                if prod_dict not in productos:
                    productos.append(prod_dict)
                
        return productos
    except Exception as e:
        return []

# --- ENCABEZADO DE LA APP PARA CLIENTES ---
st.title("✨ Dolchē — Perfumería Fina & Exclusiva")
st.markdown("<p class='brand-subtitle'>Catálogo de fragancias importadas de alta gama</p>", unsafe_allow_html=True)

# Botón discreto de sincronización en la barra lateral o superior
col_btn1, col_btn2 = st.columns([1, 5])
with col_btn1:
    if st.button("🔄 Actualizar"):
        st.cache_data.clear()
        st.rerun()

st.divider()

with st.spinner("Cargando nuestra colección exclusiva..."):
    catalogo = extraer_catalogo_dolche()

if catalogo:
    # Buscador intuitivo con respuesta al instante
    busqueda = st.text_input("🔍 Buscar fragancia (escribe el nombre, marca o notas...):", placeholder="Ej. Jean Paul, Prada, Orientica...")
    
    # Filtrado inteligente
    if busqueda:
        # Filtra si encuentra coincidencia sin importar mayúsculas/minúsculas
        catalogo_filtrado = [p for p in catalogo if busqueda.lower() in p['Nombre'].lower()]
    else:
        catalogo_filtrado = catalogo

    st.markdown(f"<p style='color: #7a6e65;'>Mostrando <b>{len(catalogo_filtrado)}</b> fragancias disponibles</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Mostrar en cuadrícula elegante de 3 columnas
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
                                st.markdown("✨ *(Dolchē)*")
                        else:
                            st.markdown("✨ *(Dolchē)*")
                        
                        st.markdown(f"**{prod['Nombre']}**")
                        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                        st.markdown(f"<span class='price-tag'>${prod['Precio Venta MXN']:,.2f} MXN</span>", unsafe_allow_html=True)
else:
    st.info("El catálogo se está actualizando. Por favor, dale clic al botón 'Actualizar' superior.")
