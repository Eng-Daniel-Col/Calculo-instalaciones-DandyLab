def calcular_corriente_monofasica(
    potencia,
    tension,
    factor_potencia=1.0,
):
    if tension <= 0:
        raise ValueError("La tensión debe ser mayor que cero.")

    if factor_potencia <= 0:
        raise ValueError("El factor de potencia debe ser mayor que cero.")

    corriente = potencia / (tension * factor_potencia)

    return corriente


def calcular_corriente_trifasica(
    potencia,
    tension,
    factor_potencia=1.0,
):
    if tension <= 0:
        raise ValueError("La tensión debe ser mayor que cero.")

    if factor_potencia <= 0:
        raise ValueError("El factor de potencia debe ser mayor que cero.")

    corriente = potencia / (
        3 ** 0.5 * tension * factor_potencia
    )

    return corriente
