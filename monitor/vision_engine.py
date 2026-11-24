import random
import cv2
import numpy as np


def detectar_flujo_anonimo_cuadrantes():
    codigos = ["P-01", "P-02", "P-03", "P-04"]
    conteo = {c: 0 for c in codigos}

    cap = cv2.VideoCapture(0)
    if cap is not None and cap.isOpened():
        ret1, frame1 = cap.read()
        ret2, frame2 = cap.read()
        cap.release()

        if ret1 and ret2 and frame1 is not None and frame2 is not None:
            f1 = cv2.GaussianBlur(cv2.cvtColor(cv2.resize(frame1, (320, 240)), cv2.COLOR_BGR2GRAY), (25, 25), 0)
            f2 = cv2.GaussianBlur(cv2.cvtColor(cv2.resize(frame2, (320, 240)), cv2.COLOR_BGR2GRAY), (25, 25), 0)
            delta = cv2.absdiff(f1, f2)
            _, umbral = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)
            umbral = cv2.dilate(umbral, None, iterations=2)

            h, w = umbral.shape
            cuadrantes = {
                "P-01": umbral[0:h // 2, 0:w // 2],
                "P-02": umbral[0:h // 2, w // 2:w],
                "P-03": umbral[h // 2:h, 0:w // 2],
                "P-04": umbral[h // 2:h, w // 2:w],
            }
            for codigo, region in cuadrantes.items():
                if cv2.countNonZero(region) > 900:
                    conteo[codigo] = 1
            return conteo, "Cámara Anónima en Memoria Volátil (OpenCV)"

    pesos = {"P-01": 0.45, "P-02": 0.30, "P-03": 0.35, "P-04": 0.20}
    for codigo, prob in pesos.items():
        if random.random() < prob:
            conteo[codigo] = 1
    return conteo, "Simulador Óptico por Zonas (Sin Almacenamiento)"