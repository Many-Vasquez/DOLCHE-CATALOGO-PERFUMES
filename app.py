import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Configuración de la página web de la app
st.set_page_config(page_title="Dolchē - Catálogo y Precios", page_icon="🛍️", layout="wide")

URL_PROVEEDOR = "https://gpmcallen.com/"

@st.cache_data(ttl=3600)
def extraer_catalogo_dolche(tasa_multiplicador=1.36):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(URL_PROVEEDOR, headers=headers)
        if response.status_code != 200:
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        productos = []
        
        # Buscamos contenedores comunes de productos en tiendas online
        items = soup.find_all(['div', 'li', 'article'], class_=lambda x: x and ('product' in x or 'item' in x or 'grid-item' in x))
        
        # Si no encuentra con clases específicas, intentamos buscar de forma general
        if not items:
            items = soup.find_all('div', class_='product-item')

        for item in items:
            # Buscar el nombre en cualquier etiqueta de encabezado o enlace principal
            nombre_tag = item.find(['h2', 'h3', 'a', 'span'], class_=lambda x: x and ('title' in x or 'name' in x))
            if not nombre_tag:
                nombre_tag = item.find('a') # Plan B: buscar el primer enlace
            nombre = nombre_tag.text.strip() if nombre_tag else "Perfume sin nombre"
            
            # Limpiamos textos muy largos o vacíos
            if len(nombre) < 2:
                continue

            # Buscar la imagen del producto
            img_tag = item.find('img')
            imagen = ""
            if img_tag:
                imagen = img_tag.get('src') or img_tag.get('data-src') or ""
                if imagen.startswith('//'):
                    imagen = "https:" + imagen

            # Buscar el precio en formato de moneda
            precio_tag = item.find(['span', 'div', 'p'], class_=lambda x: x and ('price' in x or 'amount' in x))
            precio_proveedor = 0.0
            
            if precio_tag:
                precio_str = precio_tag.text.replace('$', '').replace('USD', '').replace(',', '').strip()
                # Extraer solo la parte numérica por si hay texto extra
                import re
                numeros = re.findall(r'\d+\.\d+|\d+', precio_str)
                if numeros:
                    precio_proveedor = float(numeros[0])
            
            if precio_proveedor > 0:
                precio_final = precio_proveedor * tasa_multiplicador
                
                # Evitar duplicados exactos
                prod_dict = {
                    "Nombre": nombre,
                    "Costo USD": round(precio_proveedor, 2),
                    "Precio Venta MXN (Tasa 1.36)": round(precio_final, 2)
                }
                if prod_dict not in productos:
                    productos.append(prod_dict)
                
        return productos
    except Exception as e:
        return []

# --- INTERFAZ VISUAL DE LA APP ---
st.title("🛍️ Dolchē - Sistema de Precios y Catálogo")
st.markdown("Bienvenido al sistema automatizado. Extrayendo precios y aplicando tu tasa del **1.36** de forma directa.")

if st.button("🔄 Actualizar Catálogo desde Proveedor"):
    st.cache_data.clear()
    st.rerun()

with st.spinner("Conectando con el proveedor y calculando precios..."):
    catalogo = extraer_catalogo_dolche()

if catalogo:
    df = pd.DataFrame(catalogo)
    
    busqueda = st.text_input("🔍 Buscar perfume en el catálogo:")
    if busqueda:
        df = df[df['Nombre'].str.contains(busqueda, case=False, na=False)]
    
    st.success(f"¡Se encontraron {len(df)} productos con nombres y precios detectados!")
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No se pudieron cargar productos automáticamente. Asegúrate de que la página del proveedor esté accesible.")
