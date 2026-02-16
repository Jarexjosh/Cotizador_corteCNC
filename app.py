import streamlit as st
import pandas as pd
from cotizador import calcular_cotizacion, GANANCIAS

st.set_page_config(page_title="Cotizador CNC Pro", layout="wide")

st.title("💻 Cotizador de Corte CNC")
st.markdown("Cálculo automático mediante catálogo de materiales (Excel).")

# --- CARGA DE DATOS ---
@st.cache_data
def cargar_catalogo():
    # El archivo DEBE estar en la misma carpeta
    archivo = "Catalogo_precios.xlsx"
    return pd.read_excel(archivo, sheet_name=None)

try:
    catalogo = cargar_catalogo()
    hojas_disponibles = list(catalogo.keys())

    # --- INTERFAZ DE USUARIO ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Configuración de Material")
        material_sel = st.selectbox("1. Selecciona el Material (Hoja de Excel)", hojas_disponibles)
        
        # Filtrar grosores según la hoja seleccionada
        df_material = catalogo[material_sel]
        espesores_disponibles = df_material["Grosor"].tolist()
        espesor_sel = st.selectbox("2. Grosor (mm)", espesores_disponibles)
        
        # Obtener precio automático del Excel
        precio_lamina = float(df_material.loc[df_material["Grosor"] == espesor_sel, "Precio"].values[0])
        st.info(f"Precio base de lámina: **${precio_lamina:,.2f} MXN**")
        
        num_laminas = st.number_input("3. Cantidad de láminas", min_value=1, value=1)

    with col2:
        st.subheader("Configuración de Corte")
        tipo_corte = st.selectbox("4. Tipo de Proceso", ["Fresadora", "Laser"])
        
        # Lógica de costos fijos por minuto
        costo_minuto = 17.0 if tipo_corte == "Fresadora" else 25.0
        
        st.warning(f"Tarifa configurada: **${costo_minuto:,.2f} / minuto** (Incluye herramienta)")
        
        tiempo = st.number_input("5. Tiempo de impresión/trabajo (minutos)", min_value=1, value=15)
        
        ganancia_sel = st.selectbox("6. Margen de Ganancia", list(GANANCIAS.keys()), index=4) # 20% default

    st.divider()

    # --- CÁLCULO ---
    if st.button("CALCULAR COTIZACIÓN FINAL", use_container_width=True):
        res = calcular_cotizacion(
            tiempo, num_laminas, precio_lamina, costo_minuto, ganancia_sel
        )
        
        # --- RESULTADOS ---
        st.success("### Resumen de la Cotización")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Costo Material", f"${res['Costo Material']:,.2f}")
        c2.metric("Costo Operativo", f"${res['Costo Máquina']:,.2f}")
        c3.metric("Subtotal", f"${res['Subtotal']:,.2f}")
        c4.metric("TOTAL CLIENTE", f"${res['Total Final']:,.2f}", delta=f"{ganancia_sel} Ganancia")

except FileNotFoundError:
    st.error("⚠️ **Error:** No se encontró el archivo 'Catalogo_precios.xlsx' en la carpeta actual.")
except Exception as e:
    st.error(f"⚠️ **Error al leer el archivo:** {e}")