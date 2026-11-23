# Mundo Cartas · Sistema de Gestión de Torneos

Prototipo de aplicación web desarrollado en Django para la administración de torneos de juegos de cartas coleccionables (TCG), inscripciones, pagos, control de asistencia, resultados, rankings y recompensas para **Mundo Cartas**.

## Integrantes

| Nombre completo | Usuario de GitHub |
| :--- | :--- |
| Diego Apolinario | `juuzou-prx` |
| Adán Toro | `adantoro` |
| Rodrigo Mollo | `rodrigomollo` |

## Tecnologías utilizadas

- **Backend:** Python 3.12 o superior, Django 6.1.3
- **Frontend:** HTML5, CSS3, Bootstrap 5.3.3, Google Fonts (Jost)
- **Base de datos:** SQLite
- **Pagos:** Transbank Webpay Plus (ambiente de pruebas) mediante `transbank-sdk`
- **Librerías adicionales:** `django-crispy-forms`, `crispy-bootstrap5`, `python-dotenv`, `Pillow`

## Gestores del equipo

| App | Modelos | HU | Responsable | Rama |
| :--- | :--- | :--- | :--- | :--- |
| usuarios | Rol, Perfil | HU01-HU04 | Rodrigo Mollo | `feature/rmollo` |
| torneos | Juego, Torneo | HU05-HU11 | Diego Apolinario | `feature/dapolinario` |
| inscripciones | Inscripcion, Pago, Asistencia | HU12-HU20 | Diego Apolinario | `feature/dapolinario` |
| resultados | Resultado, Ranking | HU21-HU28 | Adán Toro | `feature/atoro` |
| recompensas | Recompensa, CanjeRecompensa | HU29-HU30 | Adán Toro | `feature/atoro` |


## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/juuzou-prx/prototipo-mundocartas.git
cd prototipo-mundocartas
```

2. Crear y activar el entorno virtual:

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. Instalar las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

4. Configurar las variables de entorno. Copia el archivo de ejemplo:

```bash
# En Windows:
copy .env.example .env
# En Linux/Mac:
cp .env.example .env
```

Abre el archivo `.env` y completa:

- `SECRET_KEY`: una clave cualquiera para desarrollo.
- `WEBPAY_API_KEY`: la clave de prueba (sandbox) de Transbank, disponible en su documentación para desarrolladores.

`WEBPAY_COMMERCE_CODE` y `WEBPAY_ENV` ya vienen con los valores de prueba.

5. Aplicar las migraciones de la base de datos:

```bash
python manage.py migrate
```

6. Crear un superusuario para acceder al panel de administración y a la gestión de torneos:

```bash
python manage.py createsuperuser
```

7. Iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

Una vez iniciado, abre tu navegador en `http://127.0.0.1:8000/`.

## Uso y roles

- **Jugador:** cualquier usuario que se registra desde el sitio. Puede ver los torneos, inscribirse, pagar su inscripción y revisar su historial en *Mis torneos*.
- **Administrador:** usuario con *Staff status* activado. Para convertir a un usuario en administrador, entra a `/admin/`, abre **Users**, selecciona el usuario y marca **Staff status**. Los administradores gestionan juegos, torneos, inscritos, pagos y asistencia desde el sitio.
- **Pagos de prueba:** el pago con Webpay funciona en el ambiente de pruebas de Transbank. Para completarlo, usa los datos de tarjeta de prueba que entrega su documentación.

## Funcionalidades principales

- **Gestión de Usuarios (`usuarios`):** registro de jugadores, inicio y cierre de sesión, perfiles y roles.
- **Juegos y Torneos (`torneos`):** mantenedor de juegos con imagen, creación, edición y cancelación de torneos, control de cupos, fechas, horarios, reglas y costos de inscripción.
- **Inscripciones, Pagos y Asistencia (`inscripciones`):** inscripción en línea a torneos con control de cupos, historial en *Mis torneos*, cancelación de la inscripción, pago en línea con Webpay Plus, registro manual del pago por el administrador, lista de inscritos y registro de asistencia.
- **Resultados y Rankings (`resultados`):** registro de resultados por torneo y tabla de posiciones (en desarrollo).
- **Sistema de Recompensas (`recompensas`):** catálogo de premios y canjes según el desempeño de los jugadores (en desarrollo).

## Flujo de trabajo

- Ramas: `main` (versión estable), `develop` (integración) y una rama `feature/<inicial><apellido>` por integrante.
- Los cambios llegan a `develop` mediante Pull Requests revisados por otro integrante.
- Los commits siguen el formato Conventional Commits, con la historia de usuario como alcance, por ejemplo `feat(HU12): agrega inscripcion a torneos`.