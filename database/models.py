CLIENTES_TABLE = """
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    identificacion TEXT,
    telefono TEXT,
    email TEXT,
    direccion TEXT,
    ciudad TEXT,
    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


MAQUINAS_TABLE = """
CREATE TABLE IF NOT EXISTS maquinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    marca TEXT,
    modelo TEXT,
    numero_serie TEXT,
    tipo TEXT,
    potencia REAL,
    tension REAL,
    corriente REAL,
    frecuencia REAL,
    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
"""


INSTALACIONES_TABLE = """
CREATE TABLE IF NOT EXISTS instalaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    maquina_id INTEGER,
    fecha_instalacion TEXT,
    tecnico TEXT,
    estado TEXT,
    observaciones TEXT,
    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (maquina_id) REFERENCES maquinas(id)
);
"""
