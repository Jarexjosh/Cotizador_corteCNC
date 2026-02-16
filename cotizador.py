# ==========================
# Cotizador Backend 2026
# ==========================

# Mantenemos el diccionario de ganancias para el multiplicador final
GANANCIAS = {f"{i}%": 1 + (i/100) for i in range(0, 55, 5)}

def calcular_cotizacion(tiempo_min, num_laminas, costo_unitario_lamina, costo_minuto_maquina, ganancia_str):
    """
    Calcula el total: (Material + (Tiempo * Costo Máquina)) * Ganancia
    """
    # 1. Costo de Material (Láminas enteras)
    costo_material_total = costo_unitario_lamina * num_laminas
    
    # 2. Costo de Proceso (Tiempo en min * Precio fijo según tipo de corte)
    costo_proceso = tiempo_min * costo_minuto_maquina
    
    # 3. Subtotal (Suma de gastos directos)
    subtotal = costo_material_total + costo_proceso
    
    # 4. Aplicar Ganancia (Multiplicador)
    factor = GANANCIAS.get(ganancia_str, 1.0)
    total_final = subtotal * factor
    
    return {
        "Costo Material": costo_material_total,
        "Costo Máquina": costo_proceso,
        "Subtotal": subtotal,
        "Total Final": total_final
    }