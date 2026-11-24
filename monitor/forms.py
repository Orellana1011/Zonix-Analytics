from django import forms
from .models import Pasillo


class RegistroFlujoForm(forms.Form):
    pasillo = forms.ModelChoiceField(
        queryset=Pasillo.objects.all(),
        label="Pasillo",
        widget=forms.Select(attrs={"class": "input-dark"}),
    )
    visitas_sumadas = forms.IntegerField(
        label="Visitas detectadas",
        min_value=1,
        max_value=500,
        widget=forms.NumberInput(attrs={"class": "input-dark", "placeholder": "Ej. 12"}),
    )
    permanencia_seg = forms.FloatField(
        label="Permanencia promedio (seg)",
        min_value=1.0,
        max_value=3600.0,
        widget=forms.NumberInput(attrs={"class": "input-dark", "step": "0.5", "placeholder": "Ej. 30"}),
    )

    def clean_visitas_sumadas(self):
        visitas = self.cleaned_data["visitas_sumadas"]
        if visitas <= 0:
            raise forms.ValidationError("Las visitas deben ser mayores a cero.")
        return visitas