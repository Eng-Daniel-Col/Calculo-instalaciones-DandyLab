from database.database import get_connection


def crear_instalacion(
    cliente_id,
    maquina_id,
    fecha_instalacion,
    tecnico="",
    estado="Pendiente",
    observaciones="",
):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO instalaciones (
            cliente_id,
            maquina_id,
            fecha_instalacion,
            tecnico,
            estado,
            observaciones
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            cliente_id,
            maquina_id,
            fecha_instalacion,
            tecnico,
            estado,
            observaciones,
        ),
    )

    connection.commit()

    instalacion_id = cursor.lastrowid

    connection.close()

    return instalacion_id
