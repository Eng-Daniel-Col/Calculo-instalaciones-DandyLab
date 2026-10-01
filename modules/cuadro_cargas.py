# modules/cuadro_cargas.py

def calcular_carga_red_cliente(potencia_laser_kw, consumo_auxiliares_kw, voltaje_fases, pf=0.85):
    """
    Calcula la carga requerida en la red del cliente expresada en kW.
    - potencia_laser_kw: Potencia de la fuente/módulo principal en kW
    - consumo_auxiliares_kw: Consumo combinado de Chiller, Extractor, Compresor en kW
    - voltaje_fases: Texto con el voltaje de la red (ej: '220V (3Ph)')
    - pf: Factor de potencia (por defecto 0.85)
    """
    # Potencia Activa Total en kW
    potencia_activa_total_kw = potencia_laser_kw + consumo_auxiliares_kw
    
    # Potencia Aparente en kVA (kVA = kW / FP)
    potencia_aparente_kva = potencia_activa_total_kw / pf if pf > 0 else potencia_activa_total_kw
    
    # Extraer valor numérico del voltaje para la fórmula
    v_num = 220.0
    for token in str(voltaje_fases).replace('V', '').split():
        if token.replace('.', '').isdigit():
            v_num = float(token)
            break

    # Estimación de corriente nominal por fase (Trifásico vs Monofásico/Bifásico)
    es_trifasico = "3Ph" in str(voltaje_fases) or "380" in str(voltaje_fases) or "440" in str(voltaje_fases) or "Trifásico" in str(voltaje_fases)
    
    if es_trifasico:
        corriente_estimada_a = (potencia_activa_total_kw * 1000) / (1.732 * v_num * pf)
    else:
        corriente_estimada_a = (potencia_activa_total_kw * 1000) / (v_num * pf)

    return {
        "potencia_laser_kw": round(potencia_laser_kw, 2),
        "consumo_auxiliares_kw": round(consumo_auxiliares_kw, 2),
        "potencia_activa_kw": round(potencia_activa_total_kw, 2),
        "potencia_aparente_kva": round(potencia_aparente_kva, 2),
        "corriente_estimada_a": round(corriente_estimada_a, 1),
        "factor_potencia": pf,
        "voltaje_fases": voltaje_fases
    }
