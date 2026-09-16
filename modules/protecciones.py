# modules/protecciones.py
from typing import Dict, Any, List

# Breakers comerciales estándar en baja tensión (Amperios)
BREAKERS_COMERCIALES = [
    15, 20, 30, 40, 50, 60, 70, 80, 100, 125, 150, 175, 200, 225, 250, 300, 400, 500, 600
]

def determinar_polos(fases: int, voltaje: float) -> int:
    """
    Determina la cantidad de polos del interruptor según la red.
    """
    if fases == 3:
        return 3
    elif fases == 1 and voltaje >= 208:
        return 2  # Monofásico / Bifásico 220V (dos líneas vivas)
    else:
        return 1  # Monofásico 110V/120V (fase + neutro)


def seleccionar_capacidad_interrupcion(corriente_nominal: float, es_principal: bool = False) -> int:
    """
    Asigna la capacidad de interrupción en kA exigida por RETIE según el nivel de carga 
    y la ubicación (Tablero Principal vs Sub-tablero / Circuito derivado).
    """
    if es_principal:
        if corriente_nominal > 150:
            return 25  # kA para acometidas principales de alta demanda industrial
        elif corriente_nominal > 60:
            return 18  # kA para tableros principales industriales medianos
        else:
            return 10  # kA estándar mínimo para tableros generales
    else:
        # Circuitos derivados
        if corriente_nominal > 50:
            return 10  # kA
        else:
            return 6   # kA mínimo permitido en sub-distribución


def seleccionar_curva_disparo(tipo_equipo: str) -> str:
    """
    Selecciona la curva de disparo tiempo-corriente según el tipo de carga.
    - Curva B: Cargas inductivas muy bajas / electrónica sensible.
    - Curva C: Motores, extractores, chillers, cargas generales inductivas (5 a 10 In).
    - Curva D: Fuentes láser de alta inrush, transformadores, arranques pesados (10 a 20 In).
    """
    tipo = tipo_equipo.lower()
    if any(k in tipo for k in ["laser", "láser", "fuente", "transformador"]):
        return "D"
    elif any(k in tipo for k in ["chiller", "extractor", "compresor", "motor", "bomba"]):
        return "C"
    else:
        return "C"  # Curva estándar industrial por defecto


def calcular_breaker_circuito(
    corriente_diseno: float,
    ampacidad_conductor: float,
    fases: int,
    voltaje: float,
    tipo_equipo: str = "General"
) -> Dict[str, Any]:
    """
    Calcula la protección contra sobrecorriente para un circuito derivado individual.
    Garantiza la regla RETIE/NTC 2050: I_breaker <= Ampacidad del conductor.
    """
    # 1. Seleccionar el primer breaker comercial superior o igual a I_diseno (125%)
    breaker_sugerido = None
    for b in BREAKERS_COMERCIALES:
        if b >= corriente_diseno:
            breaker_sugerido = b
            break
            
    if breaker_sugerido is None:
        breaker_sugerido = BREAKERS_COMERCIALES[-1]

    # 2. Validación de seguridad RETIE: El breaker NO puede superar la ampacidad del cable
    if breaker_sugerido > ampacidad_conductor:
        # Ajusta al comercial inmediatamente inferior que proteja al conductor
        breakers_validos = [b for b in BREAKERS_COMERCIALES if b <= ampacidad_conductor]
        if breakers_validos:
            breaker_sugerido = max(breakers_validos)

    polos = determinar_polos(fases, voltaje)
    ka = seleccionar_capacidad_interrupcion(corriente_diseno, es_principal=False)
    curva = seleccionar_curva_disparo(tipo_equipo)

    return {
        "amperios": breaker_sugerido,
        "polos": polos,
        "capacidad_interrupcion_ka": ka,
        "curva": curva,
        "cumple_proteccion_conductor": breaker_sugerido <= ampacidad_conductor
    }


def calcular_breaker_principal_tablero(
    potencia_total_kw: float,
    corriente_nominal_total: float,
    corriente_diseno_total: float,
    ampacidad_alimentador: float,
    fases: int,
    voltaje: float
) -> Dict[str, Any]:
    """
    Calcula el Interruptor Principal del Tablero aplicando criterios RETIE para el alimentador.
    """
    # Seleccionar el breaker comercial para la carga total del tablero
    breaker_principal = None
    for b in BREAKERS_COMERCIALES:
        if b >= corriente_diseno_total:
            breaker_principal = b
            break

    if breaker_principal is None:
        breaker_principal = BREAKERS_COMERCIALES[-1]

    # Validación de coordinación: Breaker Principal <= Ampacidad del Alimentador
    if breaker_principal > ampacidad_alimentador:
        breakers_validos = [b for b in BREAKERS_COMERCIALES if b <= ampacidad_alimentador]
        if breakers_validos:
            breaker_principal = max(breakers_validos)

    polos = determinar_polos(fases, voltaje)
    ka = seleccionar_capacidad_interrupcion(corriente_nominal_total, es_principal=True)
    curva = "C"  # Curva principal típica para tableros de distribución

    return {
        "amperios": breaker_principal,
        "polos": polos,
        "capacidad_interrupcion_ka": ka,
        "curva": curva,
        "cumple_proteccion_alimentador": breaker_principal <= ampacidad_alimentador
    }
