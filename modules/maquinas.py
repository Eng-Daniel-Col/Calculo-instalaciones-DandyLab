from database.database import get_connection


def crear_maquina(
    cliente_id,
    marca,
    modelo,
    numero_serie="",
    tipo="",
    potencia=None,
    tension=None,
    corriente=None,
    frecuencia=None,
):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO maquinas (
            cliente_id,
            marca,
            modelo,
            numero_serie,
            tipo,
            potencia,
            tension,
            corriente,
            frecuencia
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            cliente_id,
            marca,
            modelo,
            numero_serie,
            tipo,
            potencia,
            tension,
            corriente,
            frecuencia,
        ),
    )

    connection.commit()

    maquina_id = cursor.lastrowid

    connection.close()

    return maquina_id
