import streamlit as st
import pandas as pd
import os
import base64
import requests
from cotizador import calcular_cotizacion, GANANCIAS

# --- CONFIGURACIÓN DE GITHUB (Secrets) ---
# Asegúrate de configurar estos en Streamlit Cloud Settings > Secrets
try:
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
    REPO_OWNER = st.secrets["REPO_OWNER"]
    REPO_NAME = st.secrets["REPO_NAME"]
except:
    GITHUB_TOKEN = "tu_token_aqui" # Solo para pruebas locales
    REPO_OWNER = "tu_usuario"
    REPO_NAME = "tu_repo"

FILE_PATH = "Catalogo_precios.xlsx"

st.set_page_config(page_title="Cotizador CNC Pro", layout="wide")

# --- FUNCIONES DE GITHUB ---
def actualizar_en_github(archivo_bytes):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    res = requests.get(url, headers=headers)
    sha = res.json().get("sha") if res.status_code == 200 else None
    
    content_base64 = base64.b64encode(archivo_bytes).decode("utf-8")
    data = {"message": "Update via App", "content": content_base64, "sha": sha}
    response = requests.put(url, json=data, headers=headers)
    return response.status_code in [200, 201]

# --- CARGA DE DATOS ---
@st.cache_data
def leer_excel_local():
    if os.path.exists(FILE_PATH):
        return pd.read_excel(FILE_PATH, sheet_name=None)
    return None

catalogo = leer_excel_local()

st.title("💻 Cotizador de Corte CNC")

# --- BARRA LATERAL (ADMIN) ---
with st.sidebar:
    st.header("📂 Administración")
    archivo_subido = st.file_uploader("Actualizar Excel en GitHub", type=["xlsx"])
    if archivo_subido and st.button("💾 Guardar Cambios Permanentes"):
        if actualizar_en_github(archivo_subido.getvalue()):
            st.success("✅ GitHub actualizado")
            st.cache_data.clear() # Limpiar caché para ver cambios
        else:
            st.error("❌ Error de conexión")

# --- INTERFAZ PRINCIPAL ---
if catalogo:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 Material y Dimensiones")
        material_sel = st.selectbox("1. Material", list(catalogo.keys()))
        df_mat = catalogo[material_sel]
        espesor_sel = st.selectbox("2. Grosor (mm)", df_mat["Grosor"].tolist())
        precio_lamina = float(df_mat.loc[df_mat["Grosor"] == espesor_sel, "Precio"].values[0])
        st.info(f"Precio Base: **${precio_lamina:,.2f}**")

        st.write("---")
        c1, c2 = st.columns(2)
        ancho_p = c1.number_input("Ancho pieza (cm)", min_value=0.1, value=10.0)
        largo_p = c2.number_input("Largo pieza (cm)", min_value=0.1, value=10.0)
        num_piezas = st.number_input("3. Cantidad", min_value=1, value=1)

    with col2:
        st.subheader("⚙️ Configuración de Corte")
        tipo_corte = st.radio("4. Proceso", ["Fresadora", "Laser"], horizontal=True)
        
        # --- LÓGICA DE RANGOS DINÁMICOS ---
        if tipo_corte == "Fresadora":
            min_v, max_v, default_v = 7.0, 17.0, 12.0
        else: # Laser
            min_v, max_v, default_v = 11.0, 25.0, 18.0
            
        costo_minuto = st.slider(f"Tarifa {tipo_corte} ($/min)", 
                                 min_value=min_v, 
                                 max_value=max_v, 
                                 value=default_v,
                                 step=0.5)
        
        st.caption(f"Rango permitido para {tipo_corte}: ${min_v} - ${max_v}")
        
        tiempo = st.number_input("5. Tiempo (minutos)", min_value=1, value=15)
        ganancia_sel = st.selectbox("6. Ganancia", list(GANANCIAS.keys()), index=4)

    st.divider()

    if st.button("CALCULAR COTIZACIÓN FINAL", use_container_width=True):
        res = calcular_cotizacion(tiempo, num_piezas, precio_lamina, costo_minuto, ganancia_sel, ancho_p, largo_p)
        
        st.success(f"### Resumen (Uso: {res['Uso Material %']:.2f}% de la lámina)")
        m1, m2, m3 = st.columns(3)
        m1.metric("Material", f"${res['Costo Material']:,.2f}")
        m2.metric("Proceso", f"${res['Costo Máquina']:,.2f}")
        m3.metric("TOTAL CLIENTE", f"${res['Total Final']:,.2f}")
else:
    st.warning("⚠️ Sube el archivo 'Catalogo_precios.xlsx' a GitHub para iniciar.")
