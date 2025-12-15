# 🚗 Backend Core - Gestión de Flotas

El núcleo administrativo del **Sistema Logístico**. Este microservicio gestiona la lógica de negocio principal: recursos humanos, flota vehicular y logística de viajes.

---

## 🌟 Funcionalidades Principales
- **Gestión de Recursos:** ABM (Alta, Baja, Modificación) de Vehículos y Empleados.
- **Logística de Viajes:** Asignación de conductor + vehículo + ruta.
- **Control Documental:** Gestión de vencimientos (Licencias, Seguros, VTV).
- **Reportes:** Generación de estadísticas operativas.
- **Autenticación:** Generación de tokens JWT para inicio de sesión.

---

## 🔧 Modelado de Datos
El sistema utiliza PostgreSQL para relacionar:
- `Usuarios` (Roles y Permisos)
- `Empleados` (Datos laborales)
- `Vehículos` (Datos técnicos y estado)
- `Viajes` (Origen, destino, carga, estados)

---

## 🛡️ Stack Tecnológico
- **Lenguaje:** Python
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Base de Datos:** PostgreSQL
- **Validación:** Pydantic

---

## 🌱 Futuras Actualizaciones
- [ ] **Mantenimiento:** Módulo para programar y registrar reparaciones de vehículos.
- [ ] **Notificaciones:** Alertas automáticas por vencimiento de documentación.
- [ ] **Dashboard Analítico:** Endpoints específicos para métricas de rentabilidad.
- [ ] **Tests:** Cobertura de código con Pytest.

---

## 👤 Autor
**Brian Battauz** - [GitHub](https://github.com/Brian13b)