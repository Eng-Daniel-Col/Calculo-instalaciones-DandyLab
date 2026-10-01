# modules/cuadro_cargas.py

def calcular_cuadro_completo(equipos, v_primario=220, v_secundario=380, pf=0.85, f_simultaneidad=1.0):
    potencia_total_kw = sum(eq.get("potencia_kw", 0.0) for eq in equipos)
    potencia_simultanea_kw = potencia_total_kw * f_simultaneidad
    potencia_aparente_kva = potencia_simultanea_kw / pf if pf > 0 else potencia_simultanea_kw

    # Lado Secundario (Máquina)
    i_nom_sec = (potencia_simultanea_kw * 1000) / (1.732 * v_secundario * pf) if v_secundario > 0 else 0
    i_diseno_sec = i_nom_sec * 1.25

    # Lado Primario (Red Cliente - Eficiencia ~95%)
    potencia_primario_kw = potencia_simultanea_kw / 0.95
    i_nom_prim = (potencia_primario_kw * 1000) / (1.732 * v_primario * pf) if v_primario > 0 else 0
    i_diseno_prim = i_nom_prim * 1.25

    # Transformador comercial sugerido
    kvas_estandar = [5, 7.5, 10, 12, 15, 20, 25, 30, 45, 75, 112.5]
    transf_rec_kva = next((k for k in kvas_estandar if k >= potencia_aparente_kva * 1.2), round(potencia_aparente_kva * 1.25, 1))

    breaker_prim = seleccionar_breaker(i_diseno_prim)
    cable_prim = seleccionar_cable(i_diseno_prim)

    # Derivados por equipo
    circuitos_derivados = []
    for eq in equipos:
        p_kw = eq.get("potencia_kw", 0.0)
        i_nom = (p_kw * 1000) / (1.732 * v_secundario * pf) if v_secundario > 0 else 0
        i_dis = i_nom * 1.25
        circuitos_derivados.append({
            "nombre": eq.get("nombre", "Componente"),
            "potencia_kw": round(p_kw, 2),
            "i_nom_a": round(i_nom, 2),
            "i_diseno_a": round(i_dis, 2),
            "breaker": f"{seleccionar_breaker(i_dis)}A/3P",
            "cable": seleccionar_cable(i_dis)
        })

    return {
        "potencia_total_kw": round(potencia_total_kw, 2),
        "potencia_aparente_kva": round(potencia_aparente_kva, 2),
        "transformador_kva": transf_rec_kva,
        "v_primario": v_primario,
        "v_secundario": v_secundario,
        "i_nom_primario": round(i_nom_prim, 2),
        "i_diseno_primario": round(i_diseno_prim, 2),
        "breaker_primario": f"{breaker_prim}A / 3 Polos",
        "cable_primario": cable_prim,
        "circuitos_derivados": circuitos_derivados
    }

# Alias para mantener compatibilidad con la importación en app.py
def generar_cuadro_de_cargas(equipos, v_primario=220, v_secundario=380, pf=0.85):
    return calcular_cuadro_completo(equipos, v_primario, v_secundario, pf)

def seleccionar_breaker(corriente_a):
    breakers = [10, 15, 20, 30, 40, 50, 60, 70, 80, 100, 125, 150, 175, 200, 225, 250, 300, 400]
    return next((b for b in breakers if b >= corriente_a), 400)

def seleccionar_cable(corriente_a):
    if corriente_a <= 15: return "14 AWG"
    if corriente_a <= 20: return "12 AWG"
    if corriente_a <= 30: return "10 AWG"
    if corriente_a <= 50: return "8 AWG"
    if corriente_a <= 65: return "6 AWG"
    if corriente_a <= 85: return "4 AWG"
    if corriente_a <= 115: return "2 AWG"
    if corriente_a <= 130: return "1 AWG"
    if corriente_a <= 150: return "1/0 AWG"
    if corriente_a <= 175: return "2/0 AWG"
    if corriente_a <= 200: return "3/0 AWG"
    return "4/0 AWG"
