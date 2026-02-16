import streamlit as st
import pandas as pd
from cotizador import calcular_cotizacion, GANANCIAS

st.set_page_config(page_title="Cotizador CNC Pro", layout="wide")

st.title("💻 Cotizador de Corte CNC")
st.markdown("Cálculo optimizado para láminas estándar de **122 x 244 cm**.")

# --- CARGA DE DATOS ---
@st.cache_data
def cargar_catalogo():
    archivo = "Catalogo_precios.xlsx"
    return pd.read_excel(archivo, sheet_name=None)

try:
    catalogo = cargar_catalogo()
    hojas_disponibles = list(catalogo.keys())

    # --- INTERFAZ DE USUARIO ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 Selección de Material")
        material_sel = st.selectbox("1. Material", hojas_disponibles)
        
        df_material = catalogo[material_sel]
        espesores_disponibles = df_material["Grosor"].tolist()
        espesor_sel = st.selectbox("2. Grosor (mm)", espesores_disponibles)
        
        precio_lamina = float(df_material.loc[df_material["Grosor"] == espesor_sel, "Precio"].values[0])
        st.info(f"Precio Lámina (122x244): **${precio_lamina:,.2f} MXN**")

        st.write("---")
        st.subheader("📐 Medidas de la Pieza")
        cp1, cp2 = st.columns(2)
        ancho_p = cp1.number_input("Ancho de pieza (cm)", min_value=1.0, value=10.0, step=0.5)
        largo_p = cp2.number_input("Largo de pieza (cm)", min_value=1.0, value=10.0, step=0.5)
        
        num_piezas = st.number_input("3. Cantidad de piezas a cotizar", min_value=1, value=1)

    with col2:
        st.subheader("⚙️ Configuración del Trabajo")
        tipo_corte = st.selectbox("4. Proceso de Corte", ["Fresadora", "Laser"])
        
        # Tarifas por minuto (puedes ajustarlas aquí)
        costo_minuto = 17.0 if tipo_corte == "Fresadora" else 25.0
        st.warning(f"Tarifa {tipo_corte}: **${costo_minuto:,.2f} / min**")
        
        tiempo = st.number_input("5. Tiempo de máquina (minutos)", min_value=1, value=15)
        
        ganancia_sel = st.selectbox("6. Margen de utilidad", list(GANANCIAS.keys()), index=4)

    st.divider()

    # --- ACCIÓN DE CÁLCULO ---
    if st.button("GENERAR COTIZACIÓN", use_container_width=True):
        res = calcular_cotizacion(
            tiempo, num_piezas, precio_lamina, costo_minuto, ganancia_sel,
            ancho_p, largo_p
        )
        
        # --- PRESENTACIÓN DE RESULTADOS ---
        st.success(f"### Análisis de costos (Uso de lámina: {res['Uso Material %']:.2f}%)")
        
        met1, met2, met3, met4 = st.columns(4)
        met1.metric("Costo Material", f"${res['Costo Material']:,.2f}")
        met2.metric("Costo Operativo", f"${res['Costo Máquina']:,.2f}")
        met3.metric("Subtotal Sin Ganancia", f"${res['Subtotal']:,.2f}")
        st.divider()
        st.metric("PRECIO TOTAL AL CLIENTE", f"${res['Total Final']:,.2f}", 
                  delta=f"Incluye {ganancia_sel} de utilidad")

except FileNotFoundError:
    st.error("⚠️ El archivo 'Catalogo_precios.xlsx' no se encuentra en el repositorio.")
except Exception as e:
    st.error(f"⚠️ Ocurrió un error: {e}")
