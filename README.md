# ZONIX - RetailVision Analytics

ZONIX es un prototipo web para visualizar y registrar flujo de visitas por pasillo en una tienda. Incluye un panel de analítica, clasificación de zonas, recomendaciones y un historial guardado en SQLite.

## Requisitos

- Python 3.10 o posterior.
- Windows PowerShell (los comandos de abajo son para Windows).
- Una cámara web es opcional: el proyecto puede mostrar datos simulados si no hay una cámara disponible.

## Instalación y ejecución

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
```

Si PowerShell impide activar el entorno virtual, permite scripts solo en la terminal actual y vuelve a activarlo:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Crear el usuario para entrar

Solo necesitas crear una cuenta una vez por base de datos:

```powershell
python manage.py createsuperuser
```

Sigue las instrucciones para elegir tu usuario y contraseña. No hay credenciales predeterminadas. Si ya tienes una cuenta, omite este paso.

### Iniciar el sitio

```powershell
python manage.py runserver
```

Abre <http://127.0.0.1:8000> en el navegador e inicia sesión con la cuenta creada. Mantén abierta la terminal mientras haces la demostración. Para detener el servidor, presiona `Ctrl+C`.

## Qué mostrar en la demostración

1. Inicia sesión y presenta el panel principal.
2. Usa los filtros para ver zonas calientes, templadas y frías.
3. Registra visitas y permanencia desde el formulario; el total y el historial se actualizan.
4. Si tu usuario tiene permisos de administrador, prueba **Analizar Ciclo de Visión Anónima**.
5. Si quieres mostrar los datos en el administrador de Django, abre <http://127.0.0.1:8000/admin/>.

Los datos se guardan en `db.sqlite3` en la carpeta del proyecto. No borres ese archivo si quieres conservarlos.

## Limitaciones importantes de la visión

La cámara compara dos imágenes para detectar movimiento en cuatro cuadrantes; no identifica personas ni estima de forma fiable cuántas personas visitan una zona. Si la cámara no está disponible, el sistema usa un simulador que genera resultados aleatorios. Indica claramente cuál de los dos modos estás mostrando. Las imágenes capturadas no se guardan en la base de datos.

## Ejecutar las pruebas

Con el entorno virtual activado, ejecuta:

```powershell
python manage.py test
```

## Nota de despliegue

La configuración predeterminada es para desarrollo local y demostraciones. No publiques el servidor de desarrollo en Internet. Un despliegue real requiere configurar una clave secreta, dominios permitidos, HTTPS y un servidor de producción.

## Equipo

- Felipe Neftali Orellana Delgado (representante)
- Hector Alexander Fuentes Zuleta
- Juan Antonio Campos Mejia
- Sofia Alessandra Amaya Molina
- Edgar Alejandro Marenco Maravilla
