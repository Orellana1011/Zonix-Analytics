# Módulo de datos y estructura de pasillos para Zonix
# Autor: Héctor Alexander Fuentes Zuleta

pasillos_tienda = [
    {"id_pasillo": "P-01", "nombre": "Frutas y Verduras (Frescos)", "visitas": 142, "tiempo_promedio_seg": 45},
    {"id_pasillo": "P-02", "nombre": "Bebidas y Lácteos", "visitas": 98, "tiempo_promedio_seg": 25},
    {"id_pasillo": "P-03", "nombre": "Abarrotes y Granos Básicos", "visitas": 120, "tiempo_promedio_seg": 35},
    {"id_pasillo": "P-04", "nombre": "Cuidado Personal y Limpieza", "visitas": 45, "tiempo_promedio_seg": 15}
]

def obtener_pasillos():
    return pasillos_tienda

def actualizar_visitas_pasillo(codigo, nuevas_visitas):
    for p in pasillos_tienda:
        if p["id_pasillo"] == codigo.upper():
            p["visitas"] += nuevas_visitas
            return True
    return False
