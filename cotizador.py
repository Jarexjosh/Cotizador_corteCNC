# ==========================
# Cotizador Backend 2026 - Lámina Estándar
# ==========================

# Constantes de lámina estándar (122x244 cm)
ANCHO_LAMINA_STD = 122.0
LARGO_LAMINA_STD = 244.0
AREA_LAMINA_STD = ANCHO_LAMINA_STD * LARGO_LAMINA_STD # 29,768 cm2

# Diccionario de ganancias
GANANCIAS = {f"{i}%": 1 + (i/100) for i in range(0, 55, 5)}

def calcular_cotizacion(tiempo_min, num_piezas, precio_lamina_completa, costo_minuto_maquina, 
                        ganancia_str, ancho_p, largo_p):
    """
    Calcula el total basado en el área ocupada de una lámina fija de 122x244.
    """
    # 1. Área de la pieza individual
    area_pieza = ancho_p * largo_p
    
    # 2. Costo proporcional del material
    # Calculamos el precio por cm2 de la lámina y multiplicamos por el área solicitada
    # Incluye un 5% de factor de desperdicio técnico (kerf/márgenes)
    precio_por_cm2 = precio_lamina_completa / AREA_LAMINA_STD
    costo_material_unitario = precio_por_cm2 * area_pieza * 1.05
    costo_material_total = costo_material_unitario * num_piezas
    
    # 3. Costo de Proceso (Tiempo * Tarifa de máquina)
    costo_proceso = tiempo_min * costo_minuto_maquina
    
    # 4. Cálculo Final con Margen
    subtotal = costo_material_total + costo_proceso
    factor_ganancia = GANANCIAS.get(ganancia_str, 1.0)
    total_final = subtotal * factor_ganancia
    
    # Porcentaje de ocupación total del pedido en la lámina
    porcentaje_uso = (area_pieza * num_piezas / AREA_LAMINA_STD) * 100
    
    return {
        "Costo Material": costo_material_total,
        "Costo Máquina": costo_proceso,
        "Subtotal": subtotal,
        "Total Final": total_final,
        "Uso Material %": porcentaje_uso
    }
