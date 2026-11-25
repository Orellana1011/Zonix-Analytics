from django.contrib import admin
from .models import Pasillo, RegistroFlujo


@admin.register(Pasillo)
class PasilloAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "visitas", "tiempo_promedio_seg", "zona_termica")
    search_fields = ("codigo", "nombre")
    list_filter = ("fila", "columna")


@admin.register(RegistroFlujo)
class RegistroFlujoAdmin(admin.ModelAdmin):
    list_display = ("pasillo", "visitas_sumadas", "permanencia_seg", "origen", "creado_en")
    list_filter = ("origen", "pasillo")
