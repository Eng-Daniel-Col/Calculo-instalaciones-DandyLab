# modules/cuadro_cargas.py
import math

TABLA_AWG = [
    {"awg": "14 AWG", "capacidad_a": 15},
    {"awg": "12 AWG", "capacidad_a": 20},
    {"awg": "10 AWG", "capacidad_a": 30},
    {"awg": "8 AWG",  "capacidad_a": 50},
    {"awg": "6 AWG",  "capacidad_a": 65},
    {"awg": "4 AWG",  "capacidad_a": 85},
    {"awg": "2 AWG",  "capacidad_a": 115},
    {"awg": "1/0 AWG", "capacidad_a": 150},
    {"awg": "2/0 AWG", "capacidad_a": 175},
    {"awg": "4/0 AWG", "capacidad_a": 230},
    {"awg": "250 kcmil", "capacidad_a": 255},
    {"awg": "350 kcmil", "capacidad_a": 310},
]

BREAKERS_ESTANDAR = [15, 20, 30, 40, 50, 60, 70, 80, 100, 125, 150, 175, 200, 225, 250, 300, 400, 600]

def seleccionar_cable(corriente_a: float) -> str:
    for c in TABLA_AWG:
        if c["capacidad_a"] >= corriente_a:
            return c["awg"]
    return "350 kcmil o superior"

def seleccionar_breaker(corriente_diseno_a: float) -> int:
    for b in BREAKERS_ESTANDAR:
        if b >= corriente_diseno_a:
            return b
    return BREAKERS_ESTANDAR[-1]

def calcular_caida_tension(corriente_a: float, distancia_m: float, voltaje: float, fases: int) -> float:
    # Resistencia aproximada del cobre (K = 12.9)
    if fases == 3:
        delta_v = (math.sqrt(3) * corriente_a * distancia_m * 0.002)
    else:
        delta_v = (2 * corriente_a * distancia_m * 0.002)
    return round((delta_v / voltaje) * 100, 2)

def generar_cuadro_de_cargas(datos_tablero: dict, lista_equipos: list, pais_norma: str = "COLOMBIA") -> dict:
    usar_trafo = datos_tablero.get("usar_transformador", False)
    v_primario = datos_tablero.get("voltaje_primario", 220)
    fases_primario = datos_tablero.get("fases_primario", 3)
    
    v_secundario = datos_tablero.get("voltaje_secundario", 380) if usar_trafo else datos_tablero.get("voltaje", 220)
    fases_secundario = datos_tablero.get("fases_secundario", 3)
    
    eficiencia_trafo = datos_tablero.get("eficiencia_trafo", 0.95) if usar_trafo else 1.0

    cuadro_circuitos = []
    potencia_total_w = 0.0

    # 1. CIRCUITOS DERIVADOS (Alimentados al voltaje secundario / lado máquina)
    for eq in lista_equipos:
        pot_w = eq["potencia_w"]
        volt = v_secundario
        f = eq.get("fases", fases_secundario)
        fp = eq.get("fp", 0.85)
        dist = eq.get("distancia_m", 10.0)

        potencia_total_w += pot_w

        if f == 3:
            i_nom = pot_w / (math.sqrt(3) * volt * fp)
        else:
            i_nom = pot_w / (volt * fp)

        i_diseno = i_nom * 1.25  # Factor continuo 125%
        cable = seleccionar_cable(i_diseno)
        brk = seleccionar_breaker(i_diseno)
        caida = calcular_caida_tension(i_nom, dist, volt, f)

        cuadro_circuitos.append({
            "equipo": eq["nombre"],
            "potencia_kw": round(pot_w / 1000, 2),
            "corriente_diseno_a": round(i_diseno, 2),
            "cable_awg": cable,
            "caida_pct": caida,
            "breaker": f"{brk}A / {f}P"
        })

    # 2. LADO SECUNDARIO DEL TRANSFORMADOR (Salida a Máquina - 380V Trifásico)
    fp_promedio = 0.90
    if fases_secundario == 3:
        i_secundaria_nom = potencia_total_w / (math.sqrt(3) * v_secundario * fp_promedio)
    else:
        i_secundaria_nom = potencia_total_w / (v_secundario * fp_promedio)
    i_secundaria_diseno = i_secundaria_nom * 1.25

    # 3. LADO PRIMARIO DEL TRANSFORMADOR (Acometida Red Cliente)
    potencia_primario_w = potencia_total_w / eficiencia_trafo

    if fases_primario == 3:
        i_primaria_nom = potencia_primario_w / (math.sqrt(3) * v_primario * fp_promedio)
    else:
        i_primaria_nom = potencia_primario_w / (v_primario * fp_promedio)
    
    i_primaria_diseno = i_primaria_nom * 1.25

    cable_primario = seleccionar_cable(i_primaria_diseno)
    breaker_primario = seleccionar_breaker(i_primaria_diseno)
    caida_primaria = calcular_caida_tension(i_primaria_nom, datos_tablero.get("distancia_acometida_m", 15.0), v_primario, fases_primario)

    # Margen de seguridad del 20% para el transformador
    kva_transformador = math.ceil((potencia_primario_w / 1000) * 1.2)

    return {
        "norma_aplicada": f"RETIE / NTC 2050 ({pais_norma})",
        "usar_transformador": usar_trafo,
        "cuadro_cargas_circuitos": cuadro_circuitos,
        "transformador": {
            "capacidad_sugerida_kva": kva_transformador,
            "v_primario": v_primario,
            "fases_primario": fases_primario,
            "v_secundario": v_secundario,
            "fases_secundario": fases_secundario,
            "eficiencia": f"{int(eficiencia_trafo * 100)}%"
        },
        "tablero_principal": {
            "potencia_total_kw": round(potencia_total_w / 1000, 2),
            "potencia_primario_kw": round(potencia_primario_w / 1000, 2),
            "corriente_diseno_a": round(i_primaria_diseno, 2),
            "corriente_secundaria_a": round(i_secundaria_diseno, 2),
            "alimentador_awg": cable_primario,
            "caida_acometida_pct": caida_primaria,
            "breaker_principal": {
                "amperios": breaker_primario,
                "polos": fases_primario,
                "capacidad_interrupcion_ka": 10 if i_primaria_diseno <= 100 else 18,
                "curva": "C / D"
            }
        }
    }
