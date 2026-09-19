import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Configuración de la página web de la app
st.set_page_config(page_title="Dolchē - Catálogo y Precios", page_icon="🛍️", layout="wide")

URL_PROVEEDOR = "https://gpmcallen.com/"

@st.cache_data(ttl=3600) # Guarda en caché por 1 hora para agilizar consultas
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
        
        items = soup.find_all('div', class_='product-item')
        
        for item in items:
            nombre_tag = item.find('h2', class_='product-title')
            nombre = nombre_tag.text.strip() if nombre_tag else "Perfume sin nombre"
            
            img_tag = item.find('img', class_='product-image')
            imagen = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ""
            
            precio_tag = item.find('span', class_='price')
            if precio_tag:
                precio_str = precio_tag.text.replace('$', '').replace(',', '').strip()
                precio_proveedor = float(precio_str)
                precio_final = precio_proveedor * tasa_multiplicador
                
                productos.append({
                    "Nombre": nombre,
                    "Imagen": imagen,
                    "Costo USD": round(precio_proveedor, 2),
                    "Precio Venta MXN (Tasa 1.36)": round(precio_final, 2)
                })
                
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
    
    # Barra de búsqueda rápida
    busqueda = st.text_input("🔍 Buscar perfume en el catálogo:")
    if busqueda:
        df = df[df['Nombre'].str.contains(busqueda, case=False, na=False)]
    
    st.success(f"¡Se encontraron {len(df)} productos disponibles!")
    
    # Mostrar tabla interactiva con formato limpio
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No se pudieron cargar productos automáticamente en este momento o la estructura de la web requiere un ajuste fino de etiquetas. Actualiza o verifica la conexión.")
