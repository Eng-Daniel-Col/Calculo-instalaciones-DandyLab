import math


def validar_datos(tension, factor_potencia):
    """Valida los datos eléctricos básicos."""

    if tension <= 0:
        raise ValueError("La tensión debe ser mayor que cero.")

    if factor_potencia <= 0 or factor_potencia > 1:
        raise ValueError(
            "El factor de potencia debe estar entre 0 y 1."
        )


def calcular_corriente_monofasica(
    potencia,
    tension,
    factor_potencia=1.0,
    eficiencia=1.0,
):
    """
    Calcula la corriente de una carga monofásica.

    I = P / (V × FP × eficiencia)
    """

    validar_datos(tension, factor_potencia)

    if eficiencia <= 0 or eficiencia > 1:
        raise ValueError(
            "La eficiencia debe estar entre 0 y 1."
        )

    return potencia / (
        tension * factor_potencia * eficiencia
    )


def calcular_corriente_trifasica(
    potencia,
    tension,
    factor_potencia=1.0,
    eficiencia=1.0,
):
    """
    Calcula la corriente de una carga trifásica.

    I = P / (√3 × V × FP × eficiencia)
    """

    validar_datos(tension, factor_potencia)

    if eficiencia <= 0 or eficiencia > 1:
        raise ValueError(
            "La eficiencia debe estar entre 0 y 1."
        )

    return potencia / (
        math.sqrt(3)
        * tension
        * factor_potencia
        * eficiencia
    )


def calcular_corriente(
    potencia,
    tension,
    sistema,
    factor_potencia=1.0,
    eficiencia=1.0,
):
    """
    Calcula automáticamente la corriente
    dependiendo del sistema seleccionado.
    """

    sistema = sistema.lower()

    if sistema in ["monofásico", "monofasico"]:
        return calcular_corriente_monofasica(
            potencia,
            tension,
            factor_potencia,
            eficiencia,
        )

    if sistema in ["trifásico", "trifasico"]:
        return calcular_corriente_trifasica(
            potencia,
            tension,
            factor_potencia,
            eficiencia,
        )

    raise ValueError(
        "Sistema eléctrico no reconocido."
    )


def calcular_corriente_diseno(
    corriente,
    factor_diseno=1.25,
):
    """
    Calcula la corriente de diseño.

    El factor se mantiene configurable
    para adaptarlo posteriormente a la
    normativa seleccionada.
    """

    if corriente < 0:
        raise ValueError(
            "La corriente no puede ser negativa."
        )

    if factor_diseno <= 0:
        raise ValueError(
            "El factor de diseño debe ser mayor que cero."
        )

    return corriente * factor_diseno


def calcular_caida_tension(
    corriente,
    longitud,
    area_mm2,
    sistema,
    resistividad=0.0175,
):
    """
    Calcula la caída de tensión aproximada
    utilizando la resistencia del conductor.

    resistividad por defecto:
    cobre a temperatura de referencia.

    longitud = distancia desde tablero hasta carga.
    """

    if corriente < 0:
        raise ValueError(
            "La corriente no puede ser negativa."
        )

    if longitud <= 0:
        raise ValueError(
            "La longitud debe ser mayor que cero."
        )

    if area_mm2 <= 0:
        raise ValueError(
            "El área del conductor debe ser mayor que cero."
        )

    if resistividad <= 0:
        raise ValueError(
            "La resistividad debe ser mayor que cero."
        )

    sistema = sistema.lower()

    resistencia = (
        resistividad * longitud / area_mm2
    )

    if sistema in ["monofásico", "monofasico"]:
        caida_voltios = (
            2 * corriente * resistencia
        )

    elif sistema in ["trifásico", "trifasico"]:
        caida_voltios = (
            math.sqrt(3)
            * corriente
            * resistencia
        )

    else:
        raise ValueError(
            "Sistema eléctrico no reconocido."
        )

    return caida_voltios


def calcular_porcentaje_caida(
    caida_voltios,
    tension,
):
    """Calcula el porcentaje de caída de tensión."""

    if tension <= 0:
        raise ValueError(
            "La tensión debe ser mayor que cero."
        )

    return (
        caida_voltios / tension
    ) * 100
