# Módulo de persistencia e historial cronológico - ZONIX
# Autor: Juan Antonio Campos Mejía
import datetime
import json
import os

ARCHIVO_DB = "historial_zonix.json"
historial_registros = []


def cargar_historial():
    global historial_registros
    if os.path.exists(ARCHIVO_DB):
        try:
            with open(ARCHIVO_DB, "r", encoding="utf-8") as f:
                historial_registros = json.load(f)
        except (json.JSONDecodeError, OSError):
            historial_registros = []
    return historial_registros


def guardar_historial():
    try:
        with open(ARCHIVO_DB, "w", encoding="utf-8") as f:
            json.dump(historial_registros, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def registrar_evento_base(pasillo_id, nombre_pasillo, visitas, permanencia, origen="Manual/Simulación"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    evento = {
        "fecha_hora": timestamp,
        "pasillo_id": pasillo_id,
        "nombre_pasillo": nombre_pasillo,
        "visitas_sumadas": visitas,
        "permanencia_seg": permanencia,
        "origen": origen,
    }
    historial_registros.insert(0, evento)
    guardar_historial()
    return evento


def obtener_historial():
    if not historial_registros:
        cargar_historial()
    return historial_registros
