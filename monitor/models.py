from django.db import models


class Pasillo(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    visitas = models.IntegerField(default=0)
    tiempo_promedio_seg = models.FloatField(default=0.0)
    fila = models.IntegerField(default=1)
    columna = models.IntegerField(default=1)

    class Meta:
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def indice_atencion(self):
        return round(self.visitas * self.tiempo_promedio_seg, 1)

    @property
    def zona_termica(self):
        if self.visitas >= 110 and self.tiempo_promedio_seg >= 30:
            return "caliente"
        if self.visitas >= 75:
            return "templada"
        return "fria"

    @property
    def etiqueta_zona(self):
        zonas = {
            "caliente": "Zona Caliente (Alta Retención)",
            "templada": "Zona Templada (Flujo Moderado)",
            "fria": "Zona Fría (Baja Atención)",
        }
        return zonas[self.zona_termica]


class RegistroFlujo(models.Model):
    ORIGEN_CHOICES = [
        ("MANUAL", "Registro Manual"),
        ("VISION_ANONIMA", "Visión Anónima (Memoria Volátil)"),
    ]

    pasillo = models.ForeignKey(
        Pasillo,
        on_delete=models.CASCADE,
        related_name="registros",
    )
    visitas_sumadas = models.IntegerField()
    permanencia_seg = models.FloatField()
    origen = models.CharField(max_length=20, choices=ORIGEN_CHOICES, default="MANUAL")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.pasillo.codigo} (+{self.visitas_sumadas} visitas) - {self.origen}"