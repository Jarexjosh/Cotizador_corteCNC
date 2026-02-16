# ==========================
# Cotizador Backend 2026
# ==========================

# Constantes de lámina estándar
ANCHO_LAMINA_STD = 122.0
LARGO_LAMINA_STD = 244.0
AREA_LAMINA_STD = ANCHO_LAMINA_STD * LARGO_LAMINA_STD

# Diccionario de ganancias actualizado hasta el 100%
GANANCIAS = {f"{i}%": 1 + (i/100) for i in range(0, 105, 5)}

def calcular_cotizacion(tiempo_min, num_piezas, precio_lamina_completa, costo_minuto_maquina, 
                        ganancia_str, ancho_p, largo_p):
    
    area_pieza = ancho_p * largo_p
    
    # Costo proporcional + 5% desperdicio
    precio_por_cm2 = precio_lamina_completa / AREA_LAMINA_STD
    costo_material_total = (precio_por_cm2 * area_pieza * 1.05) * num_piezas
    
    # Costo de Proceso
    costo_proceso = tiempo_min * costo_minuto_maquina
    
    # Cálculo Final
    subtotal = costo_material_total + costo_proceso
    factor = GANANCIAS.get(ganancia_str, 1.0)
    total_final = subtotal * factor
    
    porcentaje_uso = (area_pieza * num_piezas / AREA_LAMINA_STD) * 100
    
    return {
        "Costo Material": costo_material_total,
        "Costo Máquina": costo_proceso,
        "Subtotal": subtotal,
        "Total Final": total_final,
        "Uso Material %": porcentaje_uso
    }
