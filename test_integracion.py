# test_integracion.py
from modules.cuadro_cargas import generar_cuadro_de_cargas

# 1. Configuración del Tablero Principal
datos_tablero = {
    "voltaje": 220,
    "fases": 3,
    "frecuencia": 60,
    "distancia_acometida_m": 15
}

# 2. Lista de Equipos a conectar
lista_equipos = [
    {
        "nombre": "Fuente Láser",
        "potencia_w": 6000,
        "voltaje": 220,
        "fases": 3,
        "fp": 0.90,
        "distancia_m": 10
    },
    {
        "nombre": "Chiller de Enfriamiento",
        "potencia_w": 3000,
        "voltaje": 220,
        "fases": 1,
        "fp": 0.85,
        "distancia_m": 25
    },
    {
        "nombre": "Extractor de Humos",
        "potencia_w": 1500,
        "voltaje": 220,
        "fases": 3,
        "fp": 0.85,
        "distancia_m": 15
    }
]

# 3. Ejecutar Cálculo bajo norma RETIE (Colombia)
resultado = generar_cuadro_de_cargas(
    datos_tablero=datos_tablero,
    lista_equipos=lista_equipos,
    pais_norma="COLOMBIA"
)

# 4. Imprimir Resumen en Consola
print("=" * 60)
print(f"NORMA APLICADA: {resultado['norma_aplicada']}")
print("=" * 60)
print("CUADRO DE CARGAS - CIRCUITO DERIVADOS:")
for c in resultado["cuadro_cargas_circuitos"]:
    print(f" -> {c['equipo']}: {c['potencia_kw']} kW | {c['corriente_diseno_a']} A | Cable: {c['cable_awg']} | ΔV: {c['caida_pct']}% | Breaker: {c['breaker']}")

print("\n" + "=" * 60)
tab = resultado["tablero_principal"]
bp = tab["breaker_principal"]
print("ALIMENTADOR Y TABLERO PRINCIPAL:")
print(f" -> Potencia Total: {tab['potencia_total_kw']} kW")
print(f" -> Corriente Diseño: {tab['corriente_diseno_a']} A")
print(f" -> Conductor Alimentador: {tab['alimentador_awg']} (Caída: {tab['caida_acometida_pct']}%)")
print(f" -> Breaker Principal: {bp['amperios']}A | {bp['polos']} Polos | {bp['capacidad_interrupcion_ka']} kA | Curva {bp['curva']}")
print("=" * 60)
