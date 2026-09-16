# modules/normas.py
from typing import Dict, Any

NORMATIVAS_DISPONIBLES = {
    "COLOMBIA": {
        "codigo": "RETIE / NTC 2050",
        "pais": "Colombia",
        "frecuencia_hz": 60,
        "caida_max_derivado_pct": 3.0,
        "caida_max_total_pct": 5.0,  # Acometida + circuito derivado
        "factor_carga_continua": 1.25,
        "temperatura_diseno_c": 75,
        "exige_capacidad_interrupcion": True,
        "requiere_rotulado_ka": True,
        "unidad_longitud": "metros"
    },
    "MEXICO": {
        "codigo": "NOM-001-SEDE-2012",
        "pais": "México",
        "frecuencia_hz": 60,
        "caida_max_derivado_pct": 3.0,
        "caida_max_total_pct": 5.0,
        "factor_carga_continua": 1.25,
        "temperatura_diseno_c": 75,
        "exige_capacidad_interrupcion": True,
        "requiere_rotulado_ka": True,
        "unidad_longitud": "metros"
    },
    "EEUU": {
        "codigo": "NEC (NFPA 70)",
        "pais": "Estados Unidos",
        "frecuencia_hz": 60,
        "caida_max_derivado_pct": 3.0,
        "caida_max_total_pct": 5.0,
        "factor_carga_continua": 1.25,
        "temperatura_diseno_c": 75,
        "exige_capacidad_interrupcion": True,
        "requiere_rotulado_ka": True,
        "unidad_longitud": "pies"
    }
}


class NormativaElectrica:
    """
    Clase encargada de gestionar las reglas y límites según el país de instalación.
    """
    def __init__(self, codigo_pais: str = "COLOMBIA"):
        pais_upper = codigo_pais.upper()
        if pais_upper not in NORMATIVAS_DISPONIBLES:
            raise ValueError(f"Normativa '{codigo_pais}' no soportada. Opciones: {list(NORMATIVAS_DISPONIBLES.keys())}")
        
        self.config = NORMATIVAS_DISPONIBLES[pais_upper]

    def obtener_configuracion(self) -> Dict[str, Any]:
        """Devuelve todos los parámetros del estándar seleccionado."""
        return self.config

    def validar_caida_tension(self, porcentaje_caida: float, es_alimentador: bool = False) -> Dict[str, Any]:
        """
        Evalúa si la caída de tensión cumple con los límites de la norma activa.
        """
        limite = self.config["caida_max_total_pct"] if es_alimentador else self.config["caida_max_derivado_pct"]
        cumple = porcentaje_caida <= limite

        return {
            "cumple": cumple,
            "porcentaje_evaluado": porcentaje_caida,
            "limite_permitido_pct": limite,
            "mensaje": f"Cumple con {self.config['codigo']}" if cumple else f"Excede el máximo permitido ({limite}%) según {self.config['codigo']}"
        }

    def obtener_factor_diseno(self) -> float:
        """Devuelve el factor de sobrecorriente para cargas continuas (125%)."""
        return self.config["factor_carga_continua"]
