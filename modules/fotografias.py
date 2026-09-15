from pathlib import Path


def crear_directorio_fotografias(instalacion_id):
    base = Path("data") / "fotografias" / str(instalacion_id)

    base.mkdir(
        parents=True,
        exist_ok=True,
    )

    return base
