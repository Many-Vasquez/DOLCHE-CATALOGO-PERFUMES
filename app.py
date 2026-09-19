import streamlit as st
import requests
from bs4 import BeautifulSoup
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
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

URL_PRINCIPAL = "https://gpmcallen.com/"

@st.cache_data(ttl=7200)
def extraer_nombres_y_precios(tasa_multiplicador=36.0):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    productos = []
    
    try:
        response = requests.get(URL_PRINCIPAL, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar elementos contenedores de productos
            items = soup.find_all(['div', 'li', 'article'], class_=lambda x: x and any(c in x for c in ['product', 'item', 'grid', 'card', 'col']))
            
            for item in items:
                # Extraer nombre completo
                nombre_tag = item.find(['h2', 'h3', 'a', 'span'], class_=lambda x: x and ('title' in x or 'name' in x))
                if not nombre_tag:
                    nombre_tag = item.find('a')
                nombre = nombre_tag.text.strip() if nombre_tag else ""
                
                if not nombre or len(nombre) < 3:
                    continue

                # Filtro estricto para descartar cremas, geles o cosméticos ajenos a perfumes
                n_lower = nombre.lower()
                palabras_prohibidas = ['cream', 'lotion', 'gel', 'makeup', 'body wash', 'lipstick', 'skincare', 'suero', 'bioglow', 'cleaner']
                if any(p in n_lower for p in palabras_prohibidas):
                    continue

                # Extraer precio del proveedor en USD
                precio_tag = item.find(['span', 'div', 'p'], class_=lambda x: x and ('price' in x or 'amount' in x))
                precio_proveedor = 0.0
                
                if precio_tag:
                    precio_str = precio_tag.text.replace('$', '').replace('USD', '').replace(',', '').strip()
                    numeros = re.findall(r'\d+\.\d+|\d+', precio_str)
                    if numeros:
                        precio_proveedor = float(numeros[0])
                
                if precio_proveedor > 0:
                    precio_final = precio_proveedor * tasa_multiplicador
                    
                    # Clasificación inteligente por categorías
                    if 'set' in n_lower or 'conjunto' in n_lower or 'gift' in n_lower or 'coffret' in n_lower:
                        categoria = "Conjunto"
                    elif 'kid' in n_lower or 'child' in n_lower or 'baby' in n_lower or 'niño' in n_lower or 'niña' in n_lower:
                        categoria = "Kids"
                    elif 'men' in n_lower or 'pour homme' in n_lower or 'caballero' in n_lower or 'for him' in n_lower:
                        categoria = "Caballero"
                    else:
                        categoria = "Dama"

                    prod_dict = {
                        "Nombre": nombre,
                        "Precio Venta MXN": round(precio_final, 2),
                        "Categoria": categoria
                    }
                    
                    if prod_dict not in productos:
                        productos.append(prod_dict)
    except:
        pass
        
    return productos

# --- INICIALIZAR CARRITO ---
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# --- ENCABEZADO DE LA APP ---
st.title("✨ Dolchē — Perfumería Fina & Exclusiva")
st.markdown("<p class='brand-subtitle'>Catálogo oficial de fragancias importadas de alta gama</p>", unsafe_allow_html=True)

col_sup1, _ = st.columns([1, 5])
with col_sup1:
    if st.button("🔄 Actualizar Catálogo"):
        st.cache_data.clear()
        st.rerun()

st.divider()

# --- CARGAR BIBLIOTECA DE NOMBRES ---
with st.spinner("Sincronizando nombres y precios de la biblioteca..."):
    catalogo = extraer_nombres_y_precios()

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

    def renderizar_grid_textos(productos_lista, tab_name):
        busqueda = st.text_input(f"🔍 Buscar en {tab_name}:", placeholder="Escribe el nombre exacto o marca...", key=f"search_{tab_name}")
        
        if busqueda:
            filtrados = [p for p in productos_lista if busqueda.lower() in p['Nombre'].lower()]
        else:
            filtrados = productos_lista

        st.markdown(f"<p style='color: #7a6e65;'>Mostrando <b>{len(filtrados)}</b> fragancias disponibles</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if not filtrados:
            st.info("No hay productos que coincidan con la búsqueda.")
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
                            st.markdown("<br>", unsafe_allow_html=True)
                            
                            if st.button("🛒 Agregar al Carrito", key=f"add_{tab_name}_{i+j}"):
                                st.session_state.carrito.append(prod)
                                st.toast(f"¡Agregado: {prod['Nombre']}!", icon="✨")

    with tab_dama:
        renderizar_grid_textos(cat_dama, "Dama")
    with tab_caballero:
        renderizar_grid_textos(cat_caballero, "Caballero")
    with tab_conjunto:
        renderizar_grid_textos(cat_conjunto, "Conjunto")
    with tab_kids:
        renderizar_grid_textos(cat_kids, "Kids")

    # --- SECCIÓN DEL CARRITO ---
    st.divider()
    st.markdown("### 🛍️ Tu Carrito de Compras")
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío.")
    else:
        total_carrito = 0
        for idx, item in enumerate(st.session_state.carrito):
            col_c1, col_c2, col_c3 = st.columns([3, 2, 1])
            with col_c1:
                st.markdown(f"**{item['Nombre']}**")
            with col_c2:
                st.markdown(f"<span class='price-tag'>${item['Precio Venta MXN']:,.2f} MXN</span>", unsafe_allow_html=True)
            with col_c3:
                if st.button("❌ Quitar", key=f"del_{idx}"):
                    st.session_state.carrito.pop(idx)
                    st.rerun()
            st.divider()
            total_carrito += item['Precio Venta MXN']
        
        st.markdown(f"### Total General: ${total_carrito:,.2f} MXN")
        
        NUMERO_WHATSAPP = "5218448939820"  # Reemplaza con tu número real
        
        mensaje = "Hola Dolchē, quiero solicitar el siguiente pedido:\n\n"
        for item in st.session_state.carrito:
            mensaje += f"- {item['Nombre']} (${item['Precio Venta MXN']:,.2f} MXN)\n"
        mensaje += f"\n*Total a pagar: ${total_carrito:,.2f} MXN*"
        
        mensaje_codificado = urllib.parse.quote(mensaje)
        url_whatsapp = f"https://wa.me/{NUMERO_WHATSAPP}?text={mensaje_codificado}"
        
        st.markdown(f"""
            <a href="{url_whatsapp}" target="_blank">
                <button style="width: 100%; background-color: #25d366; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer; text-align: center; font-size: 1.1rem;">
                    💬 Solicitar Pedido por WhatsApp
                </button>
            </a>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ Vaciar Carrito"):
            st.session_state.carrito = []
            st.rerun()
else:
    st.info("No se pudieron cargar productos en este momento. Intenta dar clic en 'Actualizar Catálogo'.")
