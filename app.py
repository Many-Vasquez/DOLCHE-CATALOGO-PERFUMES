import streamlit as st
import re

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
    .brand-subtitle {
        color: #7a6e65;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS MAESTRA AMPLIADA ---
CATALOGO_MAESTRO_GPM = [
    # Sección Dama
    {"Nombre": "11 11 Azure 1.7oz Eau de Parfum", "Precio Venta MXN": 1798.20, "Seccion": "Dama"},
    {"Nombre": "212 Heroes For Her .34oz Mini Edp By Carolina Herrera", "Precio Venta MXN": 826.20, "Seccion": "Dama"},
    {"Nombre": "Alien Extra Intense .2oz Edp Mini By Thierry Mugler", "Precio Venta MXN": 574.20, "Seccion": "Dama"},
    {"Nombre": "Alien Goddess Int .2oz Mini Eau de Parfum By Thierry Mugler", "Precio Venta MXN": 574.20, "Seccion": "Dama"},
    {"Nombre": "Ariana Grande Cloud 3.4oz Eau de Parfum", "Precio Venta MXN": 1582.20, "Seccion": "Dama"},
    {"Nombre": "Ariana Grande Thank U Next 3.4oz Eau de Parfum", "Precio Venta MXN": 1582.20, "Seccion": "Dama"},
    {"Nombre": "Armani My Way 3.0oz Eau de Parfum", "Precio Venta MXN": 2698.20, "Seccion": "Dama"},
    {"Nombre": "Billie Eilish Eilish No. 1 3.4oz Eau de Parfum", "Precio Venta MXN": 1942.20, "Seccion": "Dama"},
    {"Nombre": "Burberry Goddess 3.3oz Eau de Parfum", "Precio Venta MXN": 2338.20, "Seccion": "Dama"},
    {"Nombre": "Carolina Herrera Good Girl Legere 2.7oz", "Precio Venta MXN": 2698.20, "Seccion": "Dama"},
    {"Nombre": "Carolina Herrera Very Good Girl 2.7oz Edp", "Precio Venta MXN": 2698.20, "Seccion": "Dama"},
    {"Nombre": "Chanel Coco Mademoiselle 3.4oz Eau de Parfum", "Precio Venta MXN": 3598.20, "Seccion": "Dama"},
    {"Nombre": "Club de Nuit Woman 3.6oz Eau de Parfum By Armaf", "Precio Venta MXN": 1150.20, "Seccion": "Dama"},
    {"Nombre": "Dior J'adore 3.4oz Eau de Parfum", "Precio Venta MXN": 3238.20, "Seccion": "Dama"},
    {"Nombre": "Dolce & Gabbana Light Blue 3.3oz Edt", "Precio Venta MXN": 1978.20, "Seccion": "Dama"},
    {"Nombre": "Good Girl .24oz Mini Edp By Carolina Herrera", "Precio Venta MXN": 826.20, "Seccion": "Dama"},
    {"Nombre": "Good Girl Blush .24oz Mini Edp By Carolina Herrera", "Precio Venta MXN": 826.20, "Seccion": "Dama"},
    {"Nombre": "Good Girl Supreme .24oz Mini Edp By Carolina Herrera", "Precio Venta MXN": 826.20, "Seccion": "Dama"},
    {"Nombre": "Gucci Bloom 3.3oz Eau de Parfum", "Precio Venta MXN": 2518.20, "Seccion": "Dama"},
    {"Nombre": "Gucci Flora Gorgeous Orchid 3.3oz Eau de Parfum", "Precio Venta MXN": 2482.20, "Seccion": "Dama"},
    {"Nombre": "Jean Paul Gaultier La Belle Rosea .2oz Mini edp for Women", "Precio Venta MXN": 574.20, "Seccion": "Dama"},
    {"Nombre": "Jean Paul Gaultier Scandal 2.7oz Edp", "Precio Venta MXN": 2518.20, "Seccion": "Dama"},
    {"Nombre": "Lancome Idole 3.4oz Eau de Parfum", "Precio Venta MXN": 2698.20, "Seccion": "Dama"},
    {"Nombre": "Lancome La Vie Est Belle 3.4oz Eau de Parfum", "Precio Venta MXN": 2878.20, "Seccion": "Dama"},
    {"Nombre": "Lattafa Yara 3.4oz Eau de Parfum", "Precio Venta MXN": 934.20, "Seccion": "Dama"},
    {"Nombre": "Lattafa Yara Moi 3.4oz Eau de Parfum", "Precio Venta MXN": 934.20, "Seccion": "Dama"},
    {"Nombre": "Lattafa Yara Tous 3.4oz Eau de Parfum", "Precio Venta MXN": 934.20, "Seccion": "Dama"},
    {"Nombre": "Marc Jacobs Daisy 3.4oz Eau de Toilette", "Precio Venta MXN": 2158.20, "Seccion": "Dama"},
    {"Nombre": "Marc Jacobs Daisy Eau So Fresh 4.2oz Edt", "Precio Venta MXN": 2338.20, "Seccion": "Dama"},
    {"Nombre": "Mugler Angel 1.7oz Eau de Parfum", "Precio Venta MXN": 2518.20, "Seccion": "Dama"},
    {"Nombre": "Narciso Rodriguez For Her 3.3oz Edt", "Precio Venta MXN": 2338.20, "Seccion": "Dama"},
    {"Nombre": "Orientica Royal Amber 2.7oz Eau de Parfum", "Precio Venta MXN": 1798.20, "Seccion": "Dama"},
    {"Nombre": "Prada Paradoxe 3.3oz Eau de Parfum", "Precio Venta MXN": 2698.20, "Seccion": "Dama"},
    {"Nombre": "Prada Paradoxe Intense .23oz Mini Eau de Parfum", "Precio Venta MXN": 934.20, "Seccion": "Dama"},
    {"Nombre": "Sol de Janeiro Cheirosa 62 8.1oz Mist", "Precio Venta MXN": 934.20, "Seccion": "Dama"},
    {"Nombre": "Sol de Janeiro Cheirosa 68 8.1oz Mist", "Precio Venta MXN": 934.20, "Seccion": "Dama"},
    {"Nombre": "Valentino Born In Roma Donna 3.4oz Edp", "Precio Venta MXN": 2878.20, "Seccion": "Dama"},
    {"Nombre": "Versace Bright Crystal 3.0oz Eau de Toilette", "Precio Venta MXN": 1798.20, "Seccion": "Dama"},
    {"Nombre": "Very Good Girl .24oz Mini Edp By Carolina Herrera", "Precio Venta MXN": 826.20, "Seccion": "Dama"},
    {"Nombre": "Viktor & Rolf Flowerbomb 3.4oz Eau de Parfum", "Precio Venta MXN": 3058.20, "Seccion": "Dama"},
    {"Nombre": "Yves Saint Laurent Libre 3.0oz Eau de Parfum", "Precio Venta MXN": 2988.20, "Seccion": "Dama"},

    # Sección Caballero
    {"Nombre": "212 Men .34oz Mini Edt By Carolina Herrera", "Precio Venta MXN": 826.20, "Seccion": "Caballero"},
    {"Nombre": "Acqua Di Gio Giorgio Armani 4.2oz Edt", "Precio Venta MXN": 2338.20, "Seccion": "Caballero"},
    {"Nombre": "Acqua Di Gio Parfum 2.5oz Parfum By Giorgio Armani", "Precio Venta MXN": 2338.20, "Seccion": "Caballero"},
    {"Nombre": "Asad 3.4oz Eau de Parfum By Lattafa", "Precio Venta MXN": 934.20, "Seccion": "Caballero"},
    {"Nombre": "Azzaro Most Wanted Parfum 3.4oz", "Precio Venta MXN": 2698.20, "Seccion": "Caballero"},
    {"Nombre": "Bad Boy .27oz Mini Edt By Carolina Herrera", "Precio Venta MXN": 826.20, "Seccion": "Caballero"},
    {"Nombre": "Bad Boy Cobalt .27oz Mini Edp By Carolina Herrera", "Precio Venta MXN": 826.20, "Seccion": "Caballero"},
    {"Nombre": "Bleu de Chanel 3.4oz Eau de Toilette", "Precio Venta MXN": 2988.20, "Seccion": "Caballero"},
    {"Nombre": "Bleu de Chanel 3.4oz Eau de Parfum", "Precio Venta MXN": 3598.20, "Seccion": "Caballero"},
    {"Nombre": "Club de Nuit Intense Man 3.6oz Edp By Armaf", "Precio Venta MXN": 1258.20, "Seccion": "Caballero"},
    {"Nombre": "Dior Sauvage 3.4oz Eau de Toilette", "Precio Venta MXN": 2878.20, "Seccion": "Caballero"},
    {"Nombre": "Dior Sauvage Elixir 2.0oz", "Precio Venta MXN": 3958.20, "Seccion": "Caballero"},
    {"Nombre": "Dolce & Gabbana The One For Men 3.3oz Edt", "Precio Venta MXN": 1978.20, "Seccion": "Caballero"},
    {"Nombre": "Eros Energy 3.4oz Eau de Parfum By Versace", "Precio Venta MXN": 2338.20, "Seccion": "Caballero"},
    {"Nombre": "Eros Flame 3.4oz Eau de Parfum By Versace", "Precio Venta MXN": 2158.20, "Seccion": "Caballero"},
    {"Nombre": "Hermes Terre D'Hermes 3.4oz Edt", "Precio Venta MXN": 2518.20, "Seccion": "Caballero"},
    {"Nombre": "Jean Paul Gaultier Le Male Le Parfum 4.2oz", "Precio Venta MXN": 2698.20, "Seccion": "Caballero"},
    {"Nombre": "Khamrah Qahwa 3.4oz Eau de Parfum By Lattafa", "Precio Venta MXN": 1150.20, "Seccion": "Caballero"},
    {"Nombre": "Montblanc Explorer 3.4oz Edp", "Precio Venta MXN": 1438.20, "Seccion": "Caballero"},
    {"Nombre": "Paco Rabanne 1 Million 3.4oz Eau de Toilette", "Precio Venta MXN": 2338.20, "Seccion": "Caballero"},
    {"Nombre": "Paco Rabanne Invictus 3.4oz Eau de Toilette", "Precio Venta MXN": 2338.20, "Seccion": "Caballero"},
    {"Nombre": "Prada Luna Rossa Black 3.4oz Edp", "Precio Venta MXN": 2698.20, "Seccion": "Caballero"},
    {"Nombre": "Tom Ford Noir Extreme 3.4oz Edp", "Precio Venta MXN": 4138.20, "Seccion": "Caballero"},
    {"Nombre": "Tom Ford Ombre Leather 3.4oz Eau de Parfum", "Precio Venta MXN": 3958.20, "Seccion": "Caballero"},
    {"Nombre": "Valentino Born In Roma Uomo 3.4oz Edt", "Precio Venta MXN": 2878.20, "Seccion": "Caballero"},
    {"Nombre": "Versace Dylan Blue 3.4oz Edt", "Precio Venta MXN": 1798.20, "Seccion": "Caballero"},
    {"Nombre": "Versace Eros 3.4oz Eau de Toilette", "Precio Venta MXN": 1978.20, "Seccion": "Caballero"},
    {"Nombre": "Yves Saint Laurent Y Edp 3.4oz", "Precio Venta MXN": 2878.20, "Seccion": "Caballero"},

    # Sección Kids
    {"Nombre": "Barbie Pink Eau de Toilette for Kids 3.4oz", "Precio Venta MXN": 590.00, "Seccion": "Kids"},
    {"Nombre": "Cars Disney Pixar Eau de Toilette for Boys 3.4oz", "Precio Venta MXN": 610.00, "Seccion": "Kids"},
    {"Nombre": "Disney Frozen II Eau de Toilette Set for Kids 3.4oz", "Precio Venta MXN": 650.00, "Seccion": "Kids"},
    {"Nombre": "Disney Mickey Mouse Eau de Toilette for Kids 3.4oz", "Precio Venta MXN": 620.00, "Seccion": "Kids"},
    {"Nombre": "Hello Kitty Classic Eau de Toilette for Girls 3.4oz", "Precio Venta MXN": 630.00, "Seccion": "Kids"},
    {"Nombre": "Spider-Man Marvel Eau de Toilette for Kids 3.4oz", "Precio Venta MXN": 640.00, "Seccion": "Kids"},

    # Sección Conjuntos / Sets
    {"Nombre": "1 Million Gift Set By Paco Rabanne (Edt 3.4oz + Travel Spray)", "Precio Venta MXN": 2698.20, "Seccion": "Conjuntos"},
    {"Nombre": "Bleu de Chanel Gift Set (Edp 3.4oz + Deodorant Stick)", "Precio Venta MXN": 3418.20, "Seccion": "Conjuntos"},
    {"Nombre": "Eros Gift Set By Versace (Edt 3.4oz + Travel Spray + Pouch)", "Precio Venta MXN": 2518.20, "Seccion": "Conjuntos"},
    {"Nombre": "Good Girl Gift Set By Carolina Herrera (Edp 2.7oz + Body Lotion)", "Precio Venta MXN": 2878.20, "Seccion": "Conjuntos"},
    {"Nombre": "La Vie Est Belle Gift Set By Lancome (Edp 3.4oz + Body Lotion)", "Precio Venta MXN": 3058.20, "Seccion": "Conjuntos"},
    {"Nombre": "Libre Gift Set By Yves Saint Laurent (Edp 3.0oz + Mini Travel)", "Precio Venta MXN": 3118.20, "Seccion": "Conjuntos"},
    {"Nombre": "Sauvage Gift Set By Dior (Edt 3.4oz + Shower Gel)", "Precio Venta MXN": 3238.20, "Seccion": "Conjuntos"},
    {"Nombre": "Valentino Born In Roma Gift Set (Edp 3.4oz + Mini)", "Precio Venta MXN": 3318.20, "Seccion": "Conjuntos"}
]

# --- FUNCIÓN PARA CONVERTIR ONZAS A ML AUTOMÁTICAMENTE ---
def extraer_y_convertir_oz(nombre):
    # Busca patrones como "3.4oz", ".34oz", "8.1 oz", etc.
    match = re.search(r'([\d.]+)\s*(?:oz|OZ)', nombre)
    if match:
        try:
            onzas = float(match.group(1))
            ml = onzas * 29.5735  # 1 oz líquida = 29.5735 ml
            return f"{onzas} oz ({ml:.1f} ml)"
        except ValueError:
            pass
    return "N/D"

# --- FUNCIÓN DE BÚSQUEDA Y ORDENAMIENTO ALFABÉTICO ---
def buscar_y_ordenar(seccion_buscada, termino=""):
    resultados = [p for p in CATALOGO_MAESTRO_GPM if p['Seccion'].lower() == seccion_buscada.lower()]
    if termino:
        resultados = [p for p in resultados if termino.lower() in p['Nombre'].lower()]
    # Orden alfabético estricto por nombre
    return sorted(resultados, key=lambda x: x['Nombre'])

# --- ENCABEZADO DE LA APP ---
st.title("✨ Dolchē — Perfumería Fina & Exclusiva")
st.markdown("<p class='brand-subtitle'>Catálogo oficial ordenado alfabéticamente con conversión de volumen</p>", unsafe_allow_html=True)
st.divider()

# --- PESTAÑAS ---
cat_dama = buscar_y_ordenar("Dama")
cat_caballero = buscar_y_ordenar("Caballero")
cat_kids = buscar_y_ordenar("Kids")
cat_conjuntos = buscar_y_ordenar("Conjuntos")

tab_dama, tab_caballero, tab_kids, tab_conjuntos = st.tabs([
    f"🌸 Dama ({len(cat_dama)})", 
    f"👔 Caballero ({len(cat_caballero)})", 
    f"🧸 Kids ({len(cat_kids)})",
    f"🎁 Conjuntos ({len(cat_conjuntos)})"
])

def renderizar_pestana_tabla(seccion_nombre, tab_key):
    busqueda = st.text_input(f"🔍 Búsqueda rápida en {seccion_nombre}:", placeholder="Escribe el nombre del perfume...", key=f"search_{tab_key}")
    
    filtrados = buscar_y_ordenar(seccion_nombre, busqueda)

    st.markdown(f"<p style='color: #7a6e65;'>Mostrando <b>{len(filtrados)}</b> artículos ordenados alfabéticamente</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not filtrados:
        st.info("No se encontraron coincidencias en esta sección.")
        return

    # Preparar datos sin numeración y con la columna de conversión
    datos_tabla = []
    for prod in filtrados:
        datos_tabla.append({
            "Descripción / Nombre del Perfume": prod['Nombre'],
            "Contenido (Oz / Ml)": extraer_y_convertir_oz(prod['Nombre']),
            "Precio Venta MXN": f"${prod['Precio Venta MXN']:,.2f} MXN"
        })

    st.dataframe(
        datos_tabla, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Descripción / Nombre del Perfume": st.column_config.TextColumn(width="large"),
            "Contenido (Oz / Ml)": st.column_config.TextColumn(width="small"),
            "Precio Venta MXN": st.column_config.TextColumn(width="medium")
        }
    )

with tab_dama:
    renderizar_pestana_tabla("Dama", "dama")
with tab_caballero:
    renderizar_pestana_tabla("Caballero", "caballero")
with tab_kids:
    renderizar_pestana_tabla("Kids", "kids")
with tab_conjuntos:
    renderizar_pestana_tabla("Conjuntos", "conjuntos")
