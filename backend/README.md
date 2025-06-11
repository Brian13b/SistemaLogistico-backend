# Módulo de Gestión de Flotas

Este módulo es uno de los tres componentes principales del Sistema de Gestión de Flotas. Se encarga de la administración y seguimiento de los vehículos, conductores y viajes.

## Funcionalidades

*   **Gestión de Vehículos:** Registro, actualización y eliminación de información de vehículos (marca, modelo, patente, estado, etc.).
*   **Gestión de Conductores:** Registro, actualización y eliminación de información de conductores (datos personales, licencias, etc.).
*   **Gestión de Viajes:** Creación, seguimiento y finalización de viajes, asignando vehículos y conductores.
*   **Reportes:** Generación de informes sobre el uso de vehículos, rendimiento de conductores y estadísticas de viajes.

## Tecnologías Utilizadas

*   **Backend:** Python con FastAPI
*   **Base de Datos:** PostgreSQL

## Instalación

1.  Clonar el repositorio: `git clone`
2.  Navegar al directorio del módulo: `cd Backend`
3.  Activar el entorno virtual: `.\venv\Scripts\activate`
4.  Instalar dependencias: `pip install -r requirements.txt`
5.  Iniciar el servidor: `uvicorn main:app --reload`
