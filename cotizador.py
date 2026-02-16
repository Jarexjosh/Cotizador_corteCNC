
# ==========================
# Cotizador Backend 2026 - Versión Corregida
# ==========================

# Constantes de lámina estándar
ANCHO_LAMINA_STD = 122.0
LARGO_LAMINA_STD = 244.0
AREA_LAMINA_STD = ANCHO_LAMINA_STD * LARGO_LAMINA_STD

GANANCIAS = {f"{i}%": 1 + (i/100) for i in range(0, 55, 5)}

def calcular_cotizacion(tiempo_min, num_piezas, precio_lamina_completa, costo_minuto_maquina, 
                        ganancia_str, ancho_p, largo_p):
    """
    Recibe 7 argumentos y calcula el costo proporcional por cm2.
    """
    # 1. Área de la pieza
    area_pieza = ancho_p * largo_p
    
    # 2. Costo proporcional del material + 5% desperdicio
    precio_por_cm2 = precio_lamina_completa / AREA_LAMINA_STD
    costo_material_total = (precio_por_cm2 * area_pieza * 1.05) * num_piezas
    
    # 3. Costo de Proceso
    costo_proceso = tiempo_min * costo_minuto_maquina
    
    # 4. Cálculo Final
    subtotal = costo_material_total + costo_proceso
    factor = GANANCIAS.get(ganancia_str, 1.0)
    total_final = subtotal * factor
    
    # Uso de lámina
    porcentaje_uso = (area_pieza * num_piezas / AREA_LAMINA_STD) * 100
    
    return {
        "Costo Material": costo_material_total,
        "Costo Máquina": costo_proceso,
        "Subtotal": subtotal,
        "Total Final": total_final,
        "Uso Material %": porcentaje_uso
    }
