from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Pasillo, RegistroFlujo


class ZonixTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="demo_admin", password="Password123!")
        self.pasillo = Pasillo.objects.create(
            codigo="P-09",
            nombre="Pasillo de Prueba",
            visitas=120,
            tiempo_promedio_seg=40.0,
            fila=1,
            columna=1,
        )

    def test_clasificacion_zona_caliente(self):
        self.assertEqual(self.pasillo.zona_termica, "caliente")

    def test_dashboard_requiere_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_registro_flujo_valido_en_dashboard(self):
        self.client.login(username="demo_admin", password="Password123!")
        response = self.client.post(
            reverse("dashboard"),
            {
                "pasillo": self.pasillo.id,
                "visitas_sumadas": 10,
                "permanencia_seg": 30.0,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.pasillo.refresh_from_db()
        self.assertEqual(self.pasillo.visitas, 130)
        self.assertEqual(RegistroFlujo.objects.count(), 1)