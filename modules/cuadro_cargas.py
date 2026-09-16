# modules/cuadro_cargas.py
import math
from typing import List, Dict, Any
from .normas import NormativaElectrica
from .protecciones import calcular_breaker_circuito, calcular_breaker_principal_tablero

# Tabla de Ampacidad Cobre 75°C (NTC 2050 / RETIE / NEC 310.16)
TABLA_AMPACIDAD_COBRE = [
    {"calibre": "14 AWG",  "mm2": 2.08,  "amp": 20},
    {"calibre": "12 AWG",  "mm2": 3.31,  "amp": 25},
    {"calibre": "10 AWG",  "mm2": 5.26,  "amp": 35},
    {"calibre": "8 AWG",   "mm2": 8.37,  "amp": 50},
    {"calibre": "6 AWG",   "mm2": 13.30, "amp": 65},
    {"calibre": "4 AWG",   "mm2": 21.15, "amp": 85},
    {"calibre": "2 AWG",   "mm2": 33.62, "amp": 115},
    {"calibre": "1/0 AWG", "mm2": 53.49, "amp": 150},
    {"calibre": "2/0 AWG", "mm2": 67.43, "amp": 175},
    {"calibre": "3/0 AWG", "mm2": 85.01, "amp": 200},
    {"calibre": "4/0 AWG", "mm2": 107.22, "amp": 230},
    {"calibre": "250 kcmil", "mm2": 126.68, "amp": 255},
    {"calibre": "350 kcmil", "mm2": 177.35, "amp": 310},
    {"calibre": "500 kcmil", "mm2": 253.35, "amp": 380}
]

def _calcular_corrientes_internas(
    potencia_w: float,
    voltaje: float,
    fases: int,
    factor_potencia: float = 0.85,
    eficiencia: float = 1.0
) -> Dict[str, float]:
    if eficiencia <= 0:
        eficiencia = 1.0
    p_in = potencia_w / eficiencia
    
    if fases == 3:
        i_nom = p_in / (math.sqrt(3) * voltaje * factor_potencia)
    else:
        i_nom = p_in / (voltaje * factor_potencia)
        
    i_diseno = i_nom * 1.25  # Factor de carga continua NTC 2050
    return {"corriente_nominal": round(i_nom, 2), "corriente_diseno": round(i_diseno, 2)}

def _seleccionar_conductor_interno(
    corriente_diseno: float,
    corriente_nominal: float,
    distancia_m: float,
    voltaje: float,
    fases: int,
    factor_potencia: float = 0.85
) -> Dict[str, Any]:
    # Ampacidad
    idx = 0
    for i, c in enumerate(TABLA_AMPACIDAD_COBRE):
        if c["amp"] >= corriente_diseno:
            idx = i
            break
            
    # Caída de tensión (Max 3%)
    factor_fase = math.sqrt(3) if fases == 3 else 2.0
    caida_v = 0.0
    pct_caida = 0.0
    
    while idx < len(TABLA_AMPACIDAD_COBRE):
        cond = TABLA_AMPACIDAD_COBRE[idx]
        caida_v = (factor_fase * distancia_m * corriente_nominal * 0.018 * factor_potencia) / cond["mm2"]
        pct_caida = (caida_v / voltaje) * 100.0
        if pct_caida <= 3.0:
            break
        idx += 1
        
    idx_final = min(idx, len(TABLA_AMPACIDAD_COBRE) - 1)
    cond_final = TABLA_AMPACIDAD_COBRE[idx_final]
    
    return {
        "calibre_awg": cond_final["calibre"],
        "mm2": cond_final["mm2"],
        "ampacidad_soporte_a": cond_final["amp"],
        "porcentaje_caida": round(pct_caida, 2)
    }

def generar_cuadro_de_cargas(
    datos_tablero: Dict[str, Any],
    lista_equipos: List[Dict[str, Any]],
    pais_norma: str = "COLOMBIA"
) -> Dict[str, Any]:
    norma = NormativaElectrica(pais_norma)
    circuitos_procesados = []
    potencia_total_w = 0.0
    
    # 1. Circuitos Derivados
    for eq in lista_equipos:
        pot_w = eq["potencia_w"]
        potencia_total_w += pot_w
        
        c_calc = _calcular_corrientes_internas(
            potencia_w=pot_w,
            voltaje=eq["voltaje"],
            fases=eq["fases"],
            factor_potencia=eq.get("fp", 0.85),
            eficiencia=eq.get("eficiencia", 1.0)
        )
        
        cond = _seleccionar_conductor_interno(
            corriente_diseno=c_calc["corriente_diseno"],
            corriente_nominal=c_calc["corriente_nominal"],
            distancia_m=eq["distancia_m"],
            voltaje=eq["voltaje"],
            fases=eq["fases"],
            factor_potencia=eq.get("fp", 0.85)
        )
        
        prot = calcular_breaker_circuito(
            corriente_diseno=c_calc["corriente_diseno"],
            ampacidad_conductor=cond["ampacidad_soporte_a"],
            fases=eq["fases"],
            voltaje=eq["voltaje"],
            tipo_equipo=eq["nombre"]
        )
        
        circuitos_procesados.append({
            "equipo": eq["nombre"],
            "potencia_kw": round(pot_w / 1000, 2),
            "corriente_nom_a": c_calc["corriente_nominal"],
            "corriente_diseno_a": c_calc["corriente_diseno"],
            "cable_awg": cond["calibre_awg"],
            "caida_pct": cond["porcentaje_caida"],
            "breaker": f"{prot['amperios']}A / {prot['polos']}P / {prot['capacidad_interrupcion_ka']}kA / Curva {prot['curva']}"
        })

    # 2. Alimentador Principal
    v_tab = datos_tablero["voltaje"]
    f_tab = datos_tablero["fases"]
    dist_acometida = datos_tablero["distancia_acometida_m"]
    
    c_tab = _calcular_corrientes_internas(
        potencia_w=potencia_total_w,
        voltaje=v_tab,
        fases=f_tab,
        factor_potencia=0.85
    )
    
    cond_alim = _seleccionar_conductor_interno(
        corriente_diseno=c_tab["corriente_diseno"],
        corriente_nominal=c_tab["corriente_nominal"],
        distancia_m=dist_acometida,
        voltaje=v_tab,
        fases=f_tab
    )
    
    prot_principal = calcular_breaker_principal_tablero(
        potencia_total_kw=potencia_total_w / 1000,
        corriente_nominal_total=c_tab["corriente_nominal"],
        corriente_diseno_total=c_tab["corriente_diseno"],
        ampacidad_alimentador=cond_alim["ampacidad_soporte_a"],
        fases=f_tab,
        voltaje=v_tab
    )

    return {
        "norma_aplicada": norma.config["codigo"],
        "tablero_principal": {
            "potencia_total_kw": round(potencia_total_w / 1000, 2),
            "corriente_nominal_a": c_tab["corriente_nominal"],
            "corriente_diseno_a": c_tab["corriente_diseno"],
            "alimentador_awg": cond_alim["calibre_awg"],
            "caida_acometida_pct": cond_alim["porcentaje_caida"],
            "breaker_principal": prot_principal
        },
        "cuadro_cargas_circuitos": circuitos_procesados
    }
