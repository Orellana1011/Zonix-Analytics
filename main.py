import sys

# Datos base del prototipo inicial de Zonix
pasillos_tienda = [
    {"id_pasillo": "P-01", "nombre": "Frutas y Verduras (Frescos)", "visitas": 142, "tiempo_promedio_seg": 45},
    {"id_pasillo": "P-02", "nombre": "Bebidas y Lácteos", "visitas": 98, "tiempo_promedio_seg": 25},
    {"id_pasillo": "P-03", "nombre": "Abarrotes y Granos Básicos", "visitas": 120, "tiempo_promedio_seg": 35},
    {"id_pasillo": "P-04", "nombre": "Cuidado Personal y Limpieza", "visitas": 45, "tiempo_promedio_seg": 15}
]

def mostrar_mapa_calor():
    print("\n==================================================")
    print("      ZONIX - MAPA DE CALOR Y FLUJO EN PASILLOS   ")
    print("==================================================")
    print(f"{'Código':<8} | {'Nombre del Pasillo':<30} | {'Visitas':<8} | {'Permanencia':<12} | {'Nivel de Interés'}")
    print("-" * 78)
    
    for p in pasillos_tienda:
        if p["visitas"] > 110 and p["tiempo_promedio_seg"] > 30:
            nivel = "🔥 Zona Caliente (Alta Venta)"
        elif p["visitas"] > 80:
            nivel = "🟡 Zona Templada (Tráfico Moderado)"
        else:
            nivel = "❄️ Zona Fría (Baja Atención)"
            
        print(f"{p['id_pasillo']:<8} | {p['nombre']:<30} | {p['visitas']:<8} | {p['tiempo_promedio_seg']} seg      | {nivel}")

def generar_recomendacion_comercial():
    print("\n--- RECOMENDACIONES DE OPTIMIZACIÓN COMERCIAL ---")
    zona_fria = min(pasillos_tienda, key=lambda x: x["visitas"])
    zona_caliente = max(pasillos_tienda, key=lambda x: x["visitas"])
    
    print(f"1. Pasillo Estrella: '{zona_caliente['nombre']}' concentra la mayor retención. Ideal para productos de impulso.")
    print(f"2. Alerta de Zona Fría: '{zona_fria['nombre']}' registra menor flujo ({zona_fria['visitas']} visitas). Sugerencia: Reubicar ofertas o mejorar iluminación.")

def menu():
    while True:
        print("\n========================================")
        print("   ZONIX - SISTEMA DE ANALÍTICA RETAIL  ")
        print("========================================")
        print("1. Ver listado de pasillos monitoreados")
        print("2. Mostrar mapa de calor (Funcionalidad Central)")
        print("3. Generar recomendaciones comerciales")
        print("4. Salir")
        
        opcion = input("Seleccione una opción (1-4): ")
        
        if opcion == "1":
            print("\n--- PASILLOS MONITOREADOS ---")
            for p in pasillos_tienda:
                print(f"- [{p['id_pasillo']}] {p['nombre']} (Visitas base: {p['visitas']})")
        elif opcion == "2":
            mostrar_mapa_calor()
        elif opcion == "3":
            generar_recomendacion_comercial()
        elif opcion == "4":
            print("\nSaliendo del prototipo de Zonix. ¡Listos para el avance!")
            sys.exit()
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()