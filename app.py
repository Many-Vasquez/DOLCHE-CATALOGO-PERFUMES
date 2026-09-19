import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import urllib.parse

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
        box-shadow: 0 6px 20px rgba(43,34,30,0.04);
        padding: 15px;
    }
    .price-tag {
        color: #9c7c38;
        font-size: 1.2rem;
        font-weight: 700;
    }
    .brand-subtitle {
        color: #7a6e65;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# URL base del proveedor
URL_PROVEEDOR = "https://gpmcallen.com/"

@st.cache_data(ttl=3600)
def extraer_catalogo_dolche(tasa_multiplicador=36.0):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    productos = []
    
    # Intentamos extraer de la página principal y secciones comunes si existen en el menú de la tienda
    urls_a_visitar = [URL_PROVEEDOR]
    
    try:
        response = requests.get(URL_PROVEEDOR, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraer enlaces de categorías (hombre, mujer, niños, paquetes, etc.) si están en el menú
            menu_links = soup.select('nav a, .menu a, .header-nav a, ul.nav-menu a')
            for link in menu_links:
                href = link.get('href')
                if href and ('collection' in href or 'catalog' in href or 'shop' in href or 'categoria' in href):
                    if href.startswith('/'):
                        full_url = "https://gpmcallen.com" + href
                        if full_url not in urls_a_visitar:
                            urls_a_visitar.append(full_url)
                    elif href.startswith('http'):
                        if href not in urls_a_visitar:
                            urls_a_visitar.append(href)
    except:
        pass

    # Recorrer las páginas detectadas para juntar todo el catálogo (hombre, mujer, paquetes, etc.)
    for url in urls_a_visitar[:5]: # Limitar para evitar lentitud
        try:
            resp = requests.get(url, headers=headers, timeout=8)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Buscar elementos de productos de Shopify / plataformas comunes
            items = soup.find_all(['div', 'li', 'article'], class_=lambda x: x and any(c in x for c in ['product', 'item', 'grid-item', 'card']))
            
            for item in items:
                # Nombre del producto
                nombre_tag = item.find(['h2', 'h3', 'a', 'span'], class_=lambda x: x and ('title' in x or 'name' in x))
                if not nombre_tag:
                    nombre_tag = item.find('a')
                nombre = nombre_tag.text.strip() if nombre_tag else ""
                
                if not nombre or len(nombre) < 2:
                    continue

                # Extracción segura de la imagen del producto
                img_tag = item.find('img')
                imagen = ""
                if img_tag:
                    imagen = (
                        img_tag.get('src') or 
                        img_tag.get('data-src') or 
                        img_tag.get('data-lazy-src') or 
                        img_tag.get('data-srcset') or
                        img_tag.get('srcset') or 
                        ""
                    )
                    if ',' in imagen:
                        imagen = imagen.split(',')[0].strip().split(' ')[0]
                    
                    if imagen.startswith('//'):
                        imagen = "https:" + imagen
                    elif imagen.startswith('/'):
                        imagen = "https://gpmcallen.com" + imagen

                # Precio del producto
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
                        "Imagen_URL": imagen if imagen.startswith('http') else "",
                        "Nombre": nombre,
                        "Precio Venta MXN": round(precio_final, 2)
                    }
                    if prod_dict not in productos:
                        productos.append(prod_dict)
        except:
            continue
            
    return productos

# --- INICIALIZAR CARRITO DE COMPRAS EN LA SESIÓN ---
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# --- ENCABEZADO DE LA APP ---
st.title("✨ Dolchē — Perfumería Fina & Exclusiva")
st.markdown("<p class='brand-subtitle'>Catálogo completo de fragancias importadas de alta gama</p>", unsafe_allow_html=True)

col_sup1, col_sup2 = st.columns([1, 5])
with col_sup1:
    if st.button("🔄 Actualizar"):
        st.cache_data.clear()
        st.rerun()

st.divider()

# --- CARGAR CATÁLOGO ---
with st.spinner("Cargando nuestra colección exclusiva de fragancias..."):
    catalogo = extraer_catalogo_dolche()

if catalogo:
    # Contenedor principal y barra lateral para el carrito
    col_catalogo, col_carrito = st.columns([3, 1])
    
    with col_catalogo:
        busqueda = st.text_input("🔍 Buscar fragancia (escribe el nombre, marca o notas...):", placeholder="Ej. Jean Paul, Prada, Orientica...")
        
        if busqueda:
            catalogo_filtrado = [p for p in catalogo if busqueda.lower() in p['Nombre'].lower()]
        else:
            catalogo_filtrado = catalogo

        st.markdown(f"<p style='color: #7a6e65;'>Mostrando <b>{len(catalogo_filtrado)}</b> productos disponibles</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Cuadrícula de 3 columnas para los productos
        cols_per_row = 3
        for i in range(0, len(catalogo_filtrado), cols_per_row):
            row_cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(catalogo_filtrado):
                    prod = catalogo_filtrado[i + j]
                    with row_cols[j]:
                        with st.container(border=True):
                            # Mostrar imagen si existe
                            if prod['Imagen_URL']:
                                try:
                                    st.image(prod['Imagen_URL'], use_column_width=True)
                                except:
                                    st.markdown("✨ *(Dolchē)*")
                            else:
                                st.markdown("✨ *(Dolchē)*")
                            
                            st.markdown(f"**{prod['Nombre']}**")
                            st.markdown(f"<span class='price-tag'>${prod['Precio Venta MXN']:,.2f} MXN</span>", unsafe_allow_html=True)
                            
                            # Botón para agregar al carrito con clave única por índice
                            if st.button("🛒 Agregar", key=f"add_{i+j}"):
                                st.session_state.carrito.append(prod)
                                st.toast(f"¡Agregado: {prod['Nombre']}!", icon="✨")

    with col_carrito:
        st.markdown("### 🛍️ Tu Carrito")
        if not st.session_state.carrito:
            st.info("Tu carrito está vacío.")
        else:
            total_carrito = 0
            for idx, item in enumerate(st.session_state.carrito):
                st.markdown(f"**{item['Nombre']}**")
                st.markdown(f"${item['Precio Venta MXN']:,.2f} MXN")
                if st.button("❌ Quitar", key=f"del_{idx}"):
                    st.session_state.carrito.pop(idx)
                    st.rerun()
                st.divider()
                total_carrito += item['Precio Venta MXN']
            
            st.markdown(f"### Total: ${total_carrito:,.2f} MXN")
            
            # Botón para solicitar pedido por WhatsApp
            # CAMBIA EL NÚMERO AQUÍ por tu número de WhatsApp con lada (ej: 52181XXXXXXXX para México)
            NUMERO_WHATSAPP = "5218100000000" 
            
            mensaje = "Hola Dolchē, quiero solicitar el siguiente pedido:\n\n"
            for item in st.session_state.carrito:
                mensaje += f"- {item['Nombre']} (${item['Precio Venta MXN']:,.2f} MXN)\n"
            mensaje += f"\n*Total a pagar: ${total_carrito:,.2f} MXN*"
            
            mensaje_codificado = urllib.parse.quote(mensaje)
            url_whatsapp = f"https://wa.me/{NUMERO_WHATSAPP}?text={mensaje_codificado}"
            
            st.markdown(f"""
                <a href="{url_whatsapp}" target="_blank">
                    <button style="width: 100%; background-color: #25d366; color: white; border: none; padding: 10px; border-radius: 8px; font-weight: bold; cursor: pointer; text-align: center;">
                        💬 Solicitar por WhatsApp
                    </button>
                </a>
            """, unsafe_allow_html=True)
            
            if st.button("🗑️ Vaciar Carrito"):
                st.session_state.carrito = []
                st.rerun()
else:
    st.info("No se pudieron cargar productos en este momento. Intenta dar clic en 'Actualizar'.")
