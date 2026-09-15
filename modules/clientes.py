from database.database import get_connection


def crear_cliente(
    nombre,
    identificacion="",
    telefono="",
    email="",
    direccion="",
    ciudad="",
):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO clientes (
            nombre,
            identificacion,
            telefono,
            email,
            direccion,
            ciudad
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            nombre,
            identificacion,
            telefono,
            email,
            direccion,
            ciudad,
        ),
    )

    connection.commit()

    cliente_id = cursor.lastrowid

    connection.close()

    return cliente_id
