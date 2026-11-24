# Módulo de Visión por Computador Anónima (Detección de Flujo por Zonas) - ZONIX
# Autor: Felipe Neftalí Orellana Delgado
import random
import cv2
import numpy as np


class AnalizadorVisionAnonima:
    def __init__(self):
        self.cap = None
        self.modo_camara = False
        self.frame_anterior = None

    def iniciar(self):
        self.cap = cv2.VideoCapture(0)
        if self.cap is not None and self.cap.isOpened():
            self.modo_camara = True
        else:
            self.modo_camara = False
            if self.cap is not None:
                self.cap.release()
            self.cap = None
        self.frame_anterior = None
        return self.modo_camara

    def detener(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.modo_camara = False
        self.frame_anterior = None

    def procesar_fotograma(self):
        """
        Procesa un fotograma volátil en memoria (sin guardar imagen ni identificar personas)
        y devuelve (frame_rgb_anotado, conteo_por_pasillo).
        """
        conteo = {"P-01": 0, "P-02": 0, "P-03": 0, "P-04": 0}

        if self.modo_camara and self.cap is not None:
            ret, frame = self.cap.read()
            if not ret:
                self.detener()
                return self._generar_frame_simulado()

            frame = cv2.resize(frame, (480, 320))
            # Aplicar desenfoque gaussiano fuerte para garantizar anonimato visual
            gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gris = cv2.GaussianBlur(gris, (25, 25), 0)
            frame_visual = cv2.GaussianBlur(frame, (21, 21), 0)

            if self.frame_anterior is None:
                self.frame_anterior = gris
            else:
                delta = cv2.absdiff(self.frame_anterior, gris)
                umbral = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
                umbral = cv2.dilate(umbral, None, iterations=2)
                self.frame_anterior = gris

                h, w = umbral.shape
                mitad_h, mitad_w = h // 2, w // 2
                cuadrantes = {
                    "P-01": umbral[0:mitad_h, 0:mitad_w],
                    "P-02": umbral[0:mitad_h, mitad_w:w],
                    "P-03": umbral[mitad_h:h, 0:mitad_w],
                    "P-04": umbral[mitad_h:h, mitad_w:w],
                }
                for pid, region in cuadrantes.items():
                    pixeles_activos = cv2.countNonZero(region)
                    if pixeles_activos > 1200:
                        conteo[pid] = 1

            self._dibujar_cuadricula(frame_visual, conteo, "CAMARA EN VIVO (ANONIMIZADA)")
            frame_rgb = cv2.cvtColor(frame_visual, cv2.COLOR_BGR2RGB)
            return frame_rgb, conteo

        return self._generar_frame_simulado()

    def _generar_frame_simulado(self):
        lienzo = np.zeros((320, 480, 3), dtype=np.uint8)
        lienzo[:] = (22, 33, 52)

        pesos = [("P-01", 0.35), ("P-02", 0.25), ("P-03", 0.30), ("P-04", 0.12)]
        conteo = {}
        for pid, prob in pesos:
            conteo[pid] = 1 if random.random() < prob else 0

        coords_centro = {
            "P-01": (120, 80),
            "P-02": (360, 80),
            "P-03": (120, 240),
            "P-04": (360, 240),
        }
        for pid, activo in conteo.items():
            if activo:
                cx, cy = coords_centro[pid]
                cv2.circle(lienzo, (cx, cy), 34, (0, 229, 255), -1)
                cv2.circle(lienzo, (cx, cy), 46, (16, 185, 129), 2)

        self._dibujar_cuadricula(lienzo, conteo, "MODO SIMULADOR DE SENSOR OPTICO")
        frame_rgb = cv2.cvtColor(lienzo, cv2.COLOR_BGR2RGB)
        return frame_rgb, conteo

    def _dibujar_cuadricula(self, img, conteo, etiqueta_modo):
        h, w, _ = img.shape
        mitad_h, mitad_w = h // 2, w // 2
        cv2.line(img, (mitad_w, 0), (mitad_w, h), (0, 229, 255), 2)
        cv2.line(img, (0, mitad_h), (w, mitad_h), (0, 229, 255), 2)

        etiquetas = [
            ("P-01: Frutas/Verduras", (12, 24), conteo["P-01"]),
            ("P-02: Bebidas/Lacteos", (mitad_w + 12, 24), conteo["P-02"]),
            ("P-03: Abarrotes/Granos", (12, mitad_h + 24), conteo["P-03"]),
            ("P-04: Cuidado Personal", (mitad_w + 12, mitad_h + 24), conteo["P-04"]),
        ]
        for texto, pos, activo in etiquetas:
            color = (0, 255, 136) if activo else (200, 210, 225)
            estado = " [FLUJO]" if activo else ""
            cv2.putText(img, texto + estado, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)

        cv2.putText(img, etiqueta_modo, (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 229, 255), 1, cv2.LINE_AA)
