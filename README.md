<p align="center">
  <img src="ZONIX%20LOGO.png" alt="Logo de ZONIX" width="400"/>
</p>

<h1 align="center">ZONIX - RetailVision Analytics</h1>

<p align="center"><strong>Analítica comercial anónima para pequeños comercios</strong></p>

## Descripción del proyecto

ZONIX es un prototipo web para registrar y visualizar flujo de visitas y tiempo de permanencia por pasillo en una tienda. El panel clasifica las zonas como calientes, templadas o frías, muestra recomendaciones comerciales básicas y conserva un historial de registros en una base de datos SQLite.

El proyecto incluye una función experimental que compara imágenes consecutivas para detectar movimiento en cuatro cuadrantes. No identifica personas ni cuenta visitantes de forma fiable. Si no hay una cámara disponible, la aplicación utiliza un simulador; las imágenes capturadas no se guardan.

## Integrantes del equipo

- Felipe Neftali Orellana Delgado (Carné: SMSS047825) — Representante
- Hector Alexander Fuentes Zuleta (Carné: SMSS072625)
- Juan Antonio Campos Mejia (Carné: SMSS037325)
- Sofia Alessandra Amaya Molina (Carné: SMSS030725)
- Edgar Alejandro Marenco Maravilla (Carné: SMSS078025)

## Tecnologías y versiones requeridas

- Python 3.10 o posterior.
- Django `>=5.2,<7.0`.
- opencv-python `>=4.10.0`.
- NumPy `>=2.1.0`.
- Pillow `>=10.4.0`.
- SQLite, incluido con Python.

Las dependencias de Python están declaradas en `requirements.txt`. La interfaz principal del proyecto es web y está construida con Django.

## Instalación y ejecución en Windows

Abre PowerShell en la carpeta donde quieres guardar el proyecto y ejecuta:

```powershell
git clone https://github.com/Orellana1011/Zonix-Analytics.git
cd Zonix-Analytics
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
```

Si PowerShell impide activar el entorno virtual, permite la ejecución de scripts solo en esa terminal y vuelve a activarlo:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Crear una cuenta

Si todavía no tienes una cuenta para iniciar sesión, crea una con:

```powershell
python manage.py createsuperuser
```

Sigue las indicaciones para elegir un nombre de usuario y contraseña. No hay credenciales predeterminadas. Si ya tienes una cuenta, puedes omitir este paso.

### Iniciar el sitio web

```powershell
python manage.py runserver
```

Abre <http://127.0.0.1:8000> en el navegador e inicia sesión. Mantén abierta la terminal mientras utilizas el sitio. Para detener el servidor, presiona `Ctrl+C`.

## Funcionalidades principales

- Inicio y cierre de sesión.
- Panel con totales, pasillos y clasificación visual de zonas.
- Filtros para consultar zonas calientes, templadas y frías.
- Registro manual de visitas y permanencia, con validación.
- Historial de registros y recomendaciones comerciales básicas.
- Análisis experimental de movimiento con cámara o simulador.
- Administración de pasillos y registros mediante Django Admin en <http://127.0.0.1:8000/admin/>.

## Qué mostrar en una demostración

1. Inicia sesión y presenta el panel principal.
2. Usa los filtros para consultar las zonas.
3. Registra visitas y permanencia en un pasillo y muestra el total y el historial actualizado.
4. Si tu usuario tiene permisos, ejecuta el análisis experimental de visión y explica si se utilizó cámara o simulador.

Los datos iniciales son de demostración y no representan mediciones de una tienda real. Los registros se guardan en `db.sqlite3` en la carpeta del proyecto.

## Ejecutar las pruebas

Con el entorno virtual activado, ejecuta:

```powershell
python manage.py test
```

## Nota de despliegue

La configuración predeterminada es para desarrollo local y demostraciones. No publiques el servidor de desarrollo directamente en Internet. Un despliegue real requiere configurar una clave secreta, dominios permitidos, HTTPS y un servidor de producción.
