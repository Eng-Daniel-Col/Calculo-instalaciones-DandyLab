# Tabla inicial de conductores de cobre.
#
# IMPORTANTE:
# Los valores de ampacidad son una base inicial del sistema.
# La selección definitiva deberá considerar la norma,
# temperatura, método de instalación, número de conductores,
# correcciones y condiciones reales de la instalación.


CONDUCTORES_COBRE = [
    {
        "awg": "14 AWG",
        "area_mm2": 2.08,
        "ampacidad_base": 15,
    },
    {
        "awg": "12 AWG",
        "area_mm2": 3.31,
        "ampacidad_base": 20,
    },
    {
        "awg": "10 AWG",
        "area_mm2": 5.26,
        "ampacidad_base": 30,
    },
    {
        "awg": "8 AWG",
        "area_mm2": 8.37,
        "ampacidad_base": 40,
    },
    {
        "awg": "6 AWG",
        "area_mm2": 13.30,
        "ampacidad_base": 55,
    },
    {
        "awg": "4 AWG",
        "area_mm2": 21.15,
        "ampacidad_base": 70,
    },
    {
        "awg": "3 AWG",
        "area_mm2": 26.67,
        "ampacidad_base": 85,
    },
    {
        "awg": "2 AWG",
        "area_mm2": 33.62,
        "ampacidad_base": 95,
    },
    {
        "awg": "1 AWG",
        "area_mm2": 42.41,
        "ampacidad_base": 110,
    },
    {
        "awg": "1/0 AWG",
        "area_mm2": 53.49,
        "ampacidad_base": 125,
    },
    {
        "awg": "2/0 AWG",
        "area_mm2": 67.43,
        "ampacidad_base": 145,
    },
    {
        "awg": "3/0 AWG",
        "area_mm2": 85.01,
        "ampacidad_base": 165,
    },
    {
        "awg": "4/0 AWG",
        "area_mm2": 107.20,
        "ampacidad_base": 195,
    },
]


def obtener_conductores_cobre():
    """
    Devuelve la tabla de conductores de cobre.
    """

    return CONDUCTORES_COBRE


def buscar_conductor_por_awg(awg):
    """
    Busca un conductor específico por su calibre AWG.
    """

    for conductor in CONDUCTORES_COBRE:

        if conductor["awg"] == awg:
            return conductor

    return None


def seleccionar_por_ampacidad(
    corriente_diseno,
):
    """
    Selecciona el primer conductor cuya
    ampacidad base sea igual o superior
    a la corriente de diseño.
    """

    if corriente_diseno <= 0:
        raise ValueError(
            "La corriente de diseño debe ser mayor que cero."
        )

    for conductor in CONDUCTORES_COBRE:

        if (
            conductor["ampacidad_base"]
            >= corriente_diseno
        ):
            return conductor

    raise ValueError(
        "La corriente supera la tabla disponible."
    )


def seleccionar_por_caida_tension(
    corriente,
    tension,
    longitud,
    sistema,
    limite_caida=3.0,
):
    """
    Busca el conductor que cumpla el límite
    de caída de tensión.

    Devuelve el primer conductor que cumple.
    """

    from modules.calculo_electrico import (
        calcular_caida_tension,
        calcular_porcentaje_caida,
    )

    if tension <= 0:
        raise ValueError(
            "La tensión debe ser mayor que cero."
        )

    if longitud <= 0:
        raise ValueError(
            "La longitud debe ser mayor que cero."
        )

    if limite_caida <= 0:
        raise ValueError(
            "El límite de caída debe ser mayor que cero."
        )

    for conductor in CONDUCTORES_COBRE:

        caida_voltios = calcular_caida_tension(
            corriente= corriente,
            longitud= longitud,
            area_mm2= conductor["area_mm2"],
            sistema= sistema,
        )

        porcentaje = calcular_porcentaje_caida(
            caida_voltios= caida_voltios,
            tension= tension,
        )

        if porcentaje <= limite_caida:

            resultado = conductor.copy()

            resultado["caida_voltios"] = (
                caida_voltios
            )

            resultado["caida_porcentaje"] = (
                porcentaje
            )

            return resultado

    raise ValueError(
        "Ningún conductor de la tabla cumple "
        "el límite de caída de tensión."
    )
