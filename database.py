# Módulo de almacenamiento y registros históricos para Zonix
# Autor: Juan Antonio Campos Mejía
import datetime

historial_registros = []

def registrar_evento_base(pasillo_id, tipo_evento="Visita Registrada"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    evento = {
        "fecha_hora": timestamp,
        "pasillo": pasillo_id,
        "descripcion": tipo_evento
    }
    historial_registros.append(evento)
    return True

def obtener_historial():
    return historial_registros
