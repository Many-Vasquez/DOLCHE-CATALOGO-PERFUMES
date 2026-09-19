import requests
from bs4 import BeautifulSoup

# URL de la tienda proveedora en McAllen
URL_PROVEEDOR = "https://gpmcallen.com/"

def extraer_catalogo_dolche(tasa_multiplicador=1.36):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print("Conectando con el proveedor de McAllen para actualizar catálogo...")
    try:
        response = requests.get(URL_PROVEEDOR, headers=headers)
        if response.status_code != 200:
            print(f"Error al conectar con la página. Código de estado: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        productos = []
        
        # Estructura de elementos en la web del proveedor
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
                
                # Aplicación directa de tu tasa (incluye taxes y ganancia)
                precio_final = precio_proveedor * tasa_multiplicador
                
                productos.append({
                    "nombre": nombre,
                    "imagen": imagen,
                    "precio_proveedor_usd": precio_proveedor,
                    "precio_final_mxn": round(precio_final, 2)
                })
                
        return productos

    except Exception as e:
        print(f"Ocurrió un error durante la extracción: {e}")
        return []

if __name__ == "__main__":
    catalogo = extraer_catalogo_dolche()
    print(f"\n--- CATÁLOGO DOLCHÊ ACTUALIZADO ({len(catalogo)} productos) ---")
    for prod in catalogo:
        print(f"Perfume: {prod['nombre']}")
        print(f"Costo Proveedor: ${prod['precio_proveedor_usd']} USD")
        print(f"Precio Venta (Tasa 1.36): ${prod['precio_final_mxn']} MXN")
        print("-" * 40)
