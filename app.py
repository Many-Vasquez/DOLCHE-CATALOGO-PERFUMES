import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Configuración de la página web de la app
st.set_page_config(page_title="Dolchē - Catálogo y Precios", page_icon="🛍️", layout="wide")

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

            # Extracción de la imagen
            img_tag = item.find('img')
            imagen = ""
            if img_tag:
                imagen = img_tag.get('src') or img_tag.get('data-src') or ""
                if imagen.startswith('//'):
                    imagen = "https:" + imagen

            precio_tag = item.find(['span', 'div', 'p'], class_=lambda x: x and ('price' in x or 'amount' in x))
            precio_proveedor = 0.0
            
            if precio_tag:
                precio_str = precio_tag.text.replace('$', '').replace('USD', '').replace(',', '').strip()
                numeros = re.findall(r'\d+\.\d+|\d+', precio_str)
                if numeros:
                    precio_proveedor = float(numeros[0])
            
            if precio_proveedor > 0:
                # APLICACIÓN DE LA REGLA: Multiplicación directa por 36
                precio_final = precio_proveedor * tasa_multiplicador
                
                prod_dict = {
                    "Imagen_URL": imagen,
                    "Nombre": nombre,
                    "Costo USD": round(precio_proveedor, 2),
                    "Precio Venta MXN (Factor 36)": round(precio_final, 2)
                }
                if prod_dict not in productos:
                    productos.append(prod_dict)
                
        return productos
    except Exception as e:
        return []

# --- INTERFAZ VISUAL DE LA APP ---
st.title("🛍️ Dolchē - Sistema de Precios y Catálogo")
st.markdown("Catálogo sincronizado con el proveedor. Aplicando factor de conversión directo por **36**.")

if st.button("🔄 Actualizar Catálogo desde Proveedor"):
    st.cache_data.clear()
    st.rerun()

with st.spinner("Conectando con el proveedor y calculando precios..."):
    catalogo = extraer_catalogo_dolche()

if catalogo:
    busqueda = st.text_input("🔍 Buscar perfume en el catálogo:")
    
    # Filtrar productos si hay búsqueda
    if busqueda:
        catalogo_filtrado = [p for p in catalogo if busqueda.lower() in p['Nombre'].lower()]
    else:
        catalogo_filtrado = catalogo

    st.success(f"¡Se encontraron {len(catalogo_filtrado)} productos disponibles!")

    # Mostrar en formato visual de tarjetas con imagen
    for prod in catalogo_filtrado:
        cols = st.columns([1, 3])
        with cols[0]:
            if prod['Imagen_URL']:
                st.image(prod['Imagen_URL'], width=120)
            else:
                st.markdown("*(Sin imagen)*")
        with cols[1]:
            st.subheader(prod['Nombre'])
            st.write(f"**Costo Proveedor:** ${prod['Costo USD']} USD")
            st.write(f"**Precio Final Venta (x36):** ${['Precio Venta MXN (Factor 36)'][0] if False else prod['Precio Venta MXN (Factor 36)']} MXN")
        st.divider()
else:
    st.info("No se pudieron cargar productos en este momento. Intenta actualizar de nuevo.")
