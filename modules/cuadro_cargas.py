# modules/cuadro_cargas.py
from typing import List, Dict, Any
from .normas import NormativaElectrica
from .calculo_electrico import calcular_corrientes  # Asumiendo función base
from .conductores import seleccionar_conductor
from .protecciones import calcular_breaker_circuito, calcular_breaker_principal_tablero

def generar_cuadro_de_cargas(
    datos_tablero: Dict[str, Any],
    lista_equipos: List[Dict[str, Any]],
    pais_norma: str = "COLOMBIA"
) -> Dict[str, Any]:
    norma = NormativaElectrica(pais_norma)
    circuitos_procesados = []
    
    potencia_total_w = 0.0
    
    # 1. Procesar cada circuito derivado
    for eq in lista_equipos:
        potencia_w = eq["potencia_w"]
        potencia_total_w += potencia_w
        
        # Corrientes
        c_calc = calcular_corrientes(
            potencia_w=potencia_w,
            voltaje=eq["voltaje"],
            fases=eq["fases"],
            factor_potencia=eq.get("fp", 0.85),
            eficiencia=eq.get("eficiencia", 1.0)
        )
        
        # Conductor
        cond = seleccionar_conductor(
            corriente_diseno=c_calc["corriente_diseno"],
            corriente_nominal=c_calc["corriente_nominal"],
            distancia_m=eq["distancia_m"],
            voltaje=eq["voltaje"],
            fases=eq["fases"],
            factor_potencia=eq.get("fp", 0.85)
        )
        
        # Proteccion
        prot = calcular_breaker_circuito(
            corriente_diseno=c_calc["corriente_diseno"],
            ampacidad_conductor=cond["ampacidad_soporte_a"],
            fases=eq["fases"],
            voltaje=eq["voltaje"],
            tipo_equipo=eq["nombre"]
        )
        
        circuitos_procesados.append({
            "equipo": eq["nombre"],
            "potencia_kw": round(potencia_w / 1000, 2),
            "corriente_nom_a": c_calc["corriente_nominal"],
            "corriente_diseno_a": c_calc["corriente_diseno"],
            "cable_awg": cond["calibre_awg"],
            "caida_pct": cond["porcentaje_caida"],
            "breaker": f"{prot['amperios']}A / {prot['polos']}P / {prot['capacidad_interrupcion_ka']}kA / Curva {prot['curva']}"
        })

    # 2. Procesar Tablero Principal / Alimentador
    v_tablero = datos_tablero["voltaje"]
    f_tablero = datos_tablero["fases"]
    dist_acometida = datos_tablero["distancia_acometida_m"]
    
    c_tablero = calcular_corrientes(
        potencia_w=potencia_total_w,
        voltaje=v_tablero,
        fases=f_tablero,
        factor_potencia=0.85
    )
    
    cond_alimentador = seleccionar_conductor(
        corriente_diseno=c_tablero["corriente_diseno"],
        corriente_nominal=c_tablero["corriente_nominal"],
        distancia_m=dist_acometida,
        voltaje=v_tablero,
        fases=f_tablero
    )
    
    prot_principal = calcular_breaker_principal_tablero(
        potencia_total_kw=potencia_total_w / 1000,
        corriente_nominal_total=c_tablero["corriente_nominal"],
        corriente_diseno_total=c_tablero["corriente_diseno"],
        ampacidad_alimentador=cond_alimentador["ampacidad_soporte_a"],
        fases=f_tablero,
        voltaje=v_tablero
    )

    return {
        "norma_aplicada": norma.config["codigo"],
        "tablero_principal": {
            "potencia_total_kw": round(potencia_total_w / 1000, 2),
            "corriente_nominal_a": c_tablero["corriente_nominal"],
            "corriente_diseno_a": c_tablero["corriente_diseno"],
            "alimentador_awg": cond_alimentador["calibre_awg"],
            "caida_acometida_pct": cond_alimentador["porcentaje_caida"],
            "breaker_principal": prot_principal
        },
        "cuadro_cargas_circuitos": circuitos_procesados
    }
