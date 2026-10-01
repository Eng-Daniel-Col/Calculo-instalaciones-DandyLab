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
        clean_token = token.replace('.', '').replace('(', '').replace(')', '')
        if clean_token.isdigit():
            v_num = float(token.replace('(', '').replace(')', ''))
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


def calcular_calibre_y_breaker(corriente_estimada_a, distancia_metros=20):
    """
    Calcula el calibre de cable recomendado y el interruptor termomagnético (breaker).
    """
    # Aplicar factor de diseño del 125% según norma RETIE / NTC 2050
    corriente_diseno = corriente_estimada_a * 1.25

    # Breakers comerciales estándar
    breakers_comerciales = [15, 20, 30, 40, 50, 60, 70, 80, 100, 125, 150, 175, 200, 225, 250, 300, 400]
    breaker_sugerido = next((b for b in breakers_comerciales if b >= corriente_diseno), 400)

    # Tabla simplificada de calibres AWG / kcmil (cobre a 75°C)
    if corriente_diseno <= 20:
        calibre = "12 AWG"
    elif corriente_diseno <= 30:
        calibre = "10 AWG"
    elif corriente_diseno <= 50:
        calibre = "8 AWG"
    elif corriente_diseno <= 65:
        calibre = "6 AWG"
    elif corriente_diseno <= 85:
        calibre = "4 AWG"
    elif corriente_diseno <= 115:
        calibre = "2 AWG"
    elif corriente_diseno <= 130:
        calibre = "1 AWG"
    elif corriente_diseno <= 150:
        calibre = "1/0 AWG"
    elif corriente_diseno <= 175:
        calibre = "2/0 AWG"
    elif corriente_diseno <= 200:
        calibre = "3/0 AWG"
    elif corriente_diseno <= 230:
        calibre = "4/0 AWG"
    else:
        calibre = "250 kcmil o superior"

    return {
        "corriente_diseno_a": round(corriente_diseno, 1),
        "breaker_sugerido_a": breaker_sugerido,
        "calibre_sugerido": calibre
    }
