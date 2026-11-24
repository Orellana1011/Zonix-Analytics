from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegistroFlujoForm
from .models import Pasillo, RegistroFlujo
from .vision_engine import detectar_flujo_anonimo_cuadrantes


PASILLOS_BASE = [
    {"codigo": "P-01", "nombre": "Frutas y Verduras", "visitas": 142, "tiempo_promedio_seg": 45.0, "fila": 1, "columna": 1},
    {"codigo": "P-02", "nombre": "Bebidas y Lácteos", "visitas": 98, "tiempo_promedio_seg": 25.0, "fila": 1, "columna": 2},
    {"codigo": "P-03", "nombre": "Abarrotes y Granos", "visitas": 120, "tiempo_promedio_seg": 35.0, "fila": 2, "columna": 1},
    {"codigo": "P-04", "nombre": "Cuidado Personal", "visitas": 45, "tiempo_promedio_seg": 15.0, "fila": 2, "columna": 2},
]


def asegurar_pasillos_iniciales():
    if not Pasillo.objects.exists():
        for data in PASILLOS_BASE:
            Pasillo.objects.create(**data)


def _aplicar_flujo_a_pasillo(pasillo, visitas_sumadas, permanencia_seg, origen):
    total_visitas = pasillo.visitas + visitas_sumadas
    if total_visitas > 0:
        promedio_actual = (pasillo.visitas * pasillo.tiempo_promedio_seg) + (visitas_sumadas * permanencia_seg)
        pasillo.tiempo_promedio_seg = round(promedio_actual / total_visitas, 1)
    pasillo.visitas = total_visitas
    pasillo.save()

    RegistroFlujo.objects.create(
        pasillo=pasillo,
        visitas_sumadas=visitas_sumadas,
        permanencia_seg=permanencia_seg,
        origen=origen,
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session["visitas_sesion_demo"] = 0
            messages.success(request, f"Bienvenido a ZONIX, {user.username}.")
            return redirect("dashboard")
        messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "monitor/login.html")


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect("login")


@login_required(login_url="login")
def dashboard_view(request):
    asegurar_pasillos_iniciales()

    filtro_zona = request.GET.get("zona")
    if filtro_zona in {"caliente", "templada", "fria", "todas"}:
        request.session["filtro_zona_zonix"] = filtro_zona
    filtro_activo = request.session.get("filtro_zona_zonix", "todas")

    todos_pasillos = list(Pasillo.objects.all())
    if filtro_activo != "todas":
        pasillos_mostrados = [p for p in todos_pasillos if p.zona_termica == filtro_activo]
    else:
        pasillos_mostrados = todos_pasillos

    if request.method == "POST":
        form = RegistroFlujoForm(request.POST)
        if form.is_valid():
            pasillo = form.cleaned_data["pasillo"]
            visitas = form.cleaned_data["visitas_sumadas"]
            permanencia = form.cleaned_data["permanencia_seg"]
            _aplicar_flujo_a_pasillo(pasillo, visitas, permanencia, "MANUAL")
            request.session["visitas_sesion_demo"] = request.session.get("visitas_sesion_demo", 0) + visitas
            messages.success(request, f"Se registraron +{visitas} visitas en {pasillo.codigo}.")
            return redirect("dashboard")
        messages.warning(request, "Revise los datos ingresados en el formulario.")
    else:
        form = RegistroFlujoForm()

    estrella = max(todos_pasillos, key=lambda p: p.indice_atencion) if todos_pasillos else None
    zona_fria = min(todos_pasillos, key=lambda p: p.indice_atencion) if todos_pasillos else None
    total_visitas = sum(p.visitas for p in todos_pasillos)
    historial = RegistroFlujo.objects.select_related("pasillo")[:15]

    contexto = {
        "pasillos": pasillos_mostrados,
        "todos_pasillos": todos_pasillos,
        "form": form,
        "historial": historial,
        "estrella": estrella,
        "zona_fria": zona_fria,
        "total_visitas": total_visitas,
        "filtro_activo": filtro_activo,
        "visitas_sesion_demo": request.session.get("visitas_sesion_demo", 0),
        "puede_ejecutar_vision": request.user.has_perm("monitor.add_registroflujo") or request.user.is_staff,
    }
    return render(request, "monitor/dashboard.html", contexto)


@login_required(login_url="login")
def capturar_vision_view(request):
    asegurar_pasillos_iniciales()
    if request.method != "POST":
        return redirect("dashboard")

    if not (request.user.has_perm("monitor.add_registroflujo") or request.user.is_staff):
        messages.error(request, "No tienes permisos para ejecutar capturas de visión.")
        return redirect("dashboard")

    conteo, modo = detectar_flujo_anonimo_cuadrantes()
    detectados = 0
    for codigo, incremento in conteo.items():
        if incremento > 0:
            pasillo = Pasillo.objects.filter(codigo=codigo).first()
            if pasillo:
                _aplicar_flujo_a_pasillo(pasillo, incremento, 28.0, "VISION_ANONIMA")
                detectados += incremento

    request.session["visitas_sesion_demo"] = request.session.get("visitas_sesion_demo", 0) + detectados
    request.session["ultimo_modo_vision"] = modo

    if detectados > 0:
        messages.success(request, f"{modo}: +{detectados} flujo(s) anónimo(s) registrado(s).")
    else:
        messages.info(request, f"{modo}: ciclo analizado sin nuevos flujos en este instante.")

    return redirect("dashboard")