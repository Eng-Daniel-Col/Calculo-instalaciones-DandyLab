# modules/cuadro_cargas.py
import math

def obtener_calibre_awg(corriente: float) -> str:
    """Selecciona el calibre AWG / kcmil mínimo según la corriente de diseño (Tabla NTC 2050 / NEC 75°C)."""
    tabla_ampacidad = [
        (15, "14 AWG"),
        (20, "12 AWG"),
        (30, "10 AWG"),
        (55, "8 AWG"),
        (65, "6 AWG"),
        (85, "4 AWG"),
        (115, "2 AWG"),
        (130, "1 AWG"),
        (150, "1/0 AWG"),
        (175, "2/0 AWG"),
        (200, "3/0 AWG"),
        (230, "4/0 AWG"),
        (255, "250 kcmil"),
        (285, "300 kcmil"),
        (335, "400 kcmil"),
        (380, "500 kcmil")
    ]
    for amp, calibre in tabla_ampacidad:
        if corriente <= amp:
            return calibre
    return "500 kcmil (Especial/Paralelo)"

def obtener_breaker_sugerido(corriente: float, fases: int) -> str:
    """Calcula la protección térmica sugerida (125% por norma) y selecciona un valor comercial."""
    i_proteccion = corriente * 1.25
    breakers_comerciales = [15, 20, 30, 40, 50, 60, 70, 80, 100, 125, 150, 175, 200, 225, 250, 300, 350, 400, 500, 600]
    
    breaker_sel = breakers_comerciales[-1]
    for b in breakers_comerciales:
        if b >= i_proteccion:
            breaker_sel = b
            break
            
    polos = "3P" if fases == 3 else ("2P" if fases == 2 else "1P")
    return f"{breaker_sel}A / {polos}"

def calcular_caida_tension_pct(corriente: float, distancia_m: float, voltaje: float, fases: int) -> float:
    """Calcula el porcentaje de caída de tensión aproximado."""
    # Factor K aproximado para cobre en tubería conduit (impedancia simplificada)
    k = 0.000035 
    if fases == 3:
        delta_v = math.sqrt(3) * corriente * distancia_m * k * 100
    else:
        delta_v = 2 * corriente * distancia_m * k * 100
        
    caida_pct = (delta_v / voltaje) if voltaje > 0 else 0.0
    return round(caida_pct, 2)

def generar_cuadro_de_cargas(datos_tablero: dict, lista_equipos: list, pais_norma: str = "COLOMBIA") -> dict:
    """
    Procesa la lista de equipos y genera el cuadro de cargas, calculando corrientes,
    potencia total en kW, alimentadores y requerimientos del transformador.
    """
    usar_trafo = datos_tablero.get("usar_transformador", False)
    v_primario = datos_tablero.get("voltaje_primario", 220)
    fases_primario = datos_tablero.get("fases_primario", 3)
    v_secundario = datos_tablero.get("voltaje_secundario", 380)
    distancia_acometida = datos_tablero.get("distancia_acometida_m", 15.0)
    eficiencia_trafo = datos_tablero.get("eficiencia_trafo", 0.95)

    cuadro_circuitos = []
    potencia_total_w = 0.0

    for eq in lista_equipos:
        # CORRECCIÓN DE LA CLAVE: Manejo robusto para potencia_kw o potencia_w
        if "potencia_kw" in eq:
            pot_w = float(eq["potencia_kw"]) * 1000.0
        elif "potencia_w" in eq:
            pot_w = float(eq["potencia_w"])
        else:
            pot_w = 0.0

        pot_kw = round(pot_w / 1000.0, 2)
        potencia_total_w += pot_w

        voltaje_eq = float(eq.get("voltaje", v_secundario))
        fases_eq = int(eq.get("fases", 3))
        fp = float(eq.get("fp", 0.85))
        dist_m = float(eq.get("distancia_m", 10.0))

        # Cálculo de corriente de línea
        if fases_eq == 3:
            i_diseno = pot_w / (math.sqrt(3) * voltaje_eq * fp)
        else:
            i_diseno = pot_w / (voltaje_eq * fp)

        i_diseno = round(i_diseno, 2)
        cable_awg = obtener_calibre_awg(i_diseno)
        breaker_str = obtener_breaker_sugerido(i_diseno, fases_eq)
        caida_pct = calcular_caida_tension_pct(i_diseno, dist_m, voltaje_eq, fases_eq)

        cuadro_circuitos.append({
            "equipo": eq.get("nombre", "Equipo Generico"),
            "potencia_kw": pot_kw,
            "potencia_w": pot_w,
            "corriente_diseno_a": i_diseno,
            "cable_awg": cable_awg,
            "caida_pct": caida_pct,
            "breaker": breaker_str
        })

    potencia_total_kw = round(potencia_total_w / 1000.0, 2)

    # Cálculo de corriente de la acometida principal (lado primario)
    pot_trafo_w = potencia_total_w / eficiencia_trafo if usar_trafo else potencia_total_w
    
    if fases_primario == 3:
        i_acometida_primario = pot_trafo_w / (math.sqrt(3) * v_primario * 0.90)
    elif fases_primario == 2:
        i_acometida_primario = pot_trafo_w / (v_primario * 0.90)
    else:
        i_acometida_primario = pot_trafo_w / (v_primario * 0.90)

    i_acometida_primario = round(i_acometida_primario, 2)
    cable_acometida = obtener_calibre_awg(i_acometida_primario)
    breaker_primario_amp = int(math.ceil((i_acometida_primario * 1.25) / 5.0) * 5)
    
    caida_acometida_pct = calcular_caida_tension_pct(i_acometida_primario, distancia_acometida, v_primario, fases_primario)

    # Potencia en kVA para sugerencia de transformador
    kva_requeridos = (potencia_total_kw / 0.85) / eficiencia_trafo
    estandares_kva = [5, 10, 15, 20, 25, 30, 45, 75, 112.5, 150]
    capacidad_trafo_kva = estandares_kva[-1]
    for kva in estandares_kva:
        if kva >= kva_requeridos:
            capacidad_trafo_kva = kva
            break

    return {
        "norma_aplicada": f"RETIE / NTC 2050 ({pais_norma})",
        "usar_transformador": usar_trafo,
        "transformador": {
            "capacidad_sugerida_kva": capacidad_trafo_kva,
            "v_primario": v_primario,
            "fases_primario": fases_primario,
            "v_secundario": v_secundario,
            "eficiencia": f"{int(eficiencia_trafo * 100)}%"
        },
        "tablero_principal": {
            "potencia_total_kw": potencia_total_kw,
            "corriente_diseno_a": i_acometida_primario,
            "alimentador_awg": cable_acometida,
            "caida_acometida_pct": caida_acometida_pct,
            "breaker_principal": {
                "amperios": breaker_primario_amp,
                "polos": fases_primario,
                "capacidad_interrupcion_ka": 10 if v_primario <= 220 else 18,
                "curva": "C"
            }
        },
        "cuadro_cargas_circuitos": cuadro_circuitos
    }
