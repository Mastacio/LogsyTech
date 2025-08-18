# Sistema de Cotizaciones - CotizApp

Un sistema completo de gestión de cotizaciones desarrollado en Django para desarrolladores de software y consultores.

## 🚀 Características Principales

### 📋 Gestión de Clientes
- Registro completo de clientes con información de contacto
- Búsqueda y filtrado de clientes
- Historial de cotizaciones por cliente
- Gestión de estados activo/inactivo

### 🛠️ Gestión de Servicios
- Catálogo de servicios con tarifas por hora
- Categorización por tipo de servicio (Desarrollo, Mantenimiento, Consultoría, etc.)
- Configuración flexible de tarifas
- Estados activo/inactivo

### 💰 Sistema de Cotizaciones
- **Modalidades de Pago**: Mensual, Anual, Pago único
- **Cálculo Automático**: Horas × Tarifa por hora
- **Descuentos**: Porcentajes configurables
- **IVA**: Configuración automática de impuestos
- **Estados**: Borrador, Enviada, Aprobada, Rechazada, Cancelada
- **Numeración Automática**: Sistema de numeración secuencial

### 📊 Dashboard Interactivo
- Estadísticas en tiempo real
- Gráficos de cotizaciones por estado
- Cotizaciones recientes
- Métricas de rendimiento

### 📄 Generación de PDFs
- Reportes profesionales en PDF
- Incluye toda la información de la cotización
- Diseño limpio y profesional
- Descarga directa desde la aplicación

### 🎨 Interfaz Moderna
- Diseño responsive con Bootstrap 5
- Navegación intuitiva
- Iconografía Font Awesome
- Tema personalizado con gradientes

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.2.5
- **Base de Datos**: SQLite (configurable para PostgreSQL/MySQL)
- **Frontend**: Bootstrap 5, jQuery
- **PDF**: ReportLab
- **Formularios**: Django Crispy Forms
- **Iconos**: Font Awesome 6

## 📦 Instalación

### Prerrequisitos
- Python 3.8+
- pip
- git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd Cotizaciones
```

2. **Crear entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar la base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crear superusuario**
```bash
python manage.py createsuperuser
```

6. **Ejecutar el servidor**
```bash
python manage.py runserver
```

7. **Acceder a la aplicación**
- Aplicación principal: http://localhost:8000
- Panel de administración: http://localhost:8000/admin

## 📋 Estructura del Proyecto

```
Cotizaciones/
├── manage.py
├── quotes/                 # Configuración principal del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── cotizaciones/          # Aplicación principal
│   ├── models.py         # Modelos de datos
│   ├── views.py          # Vistas y lógica de negocio
│   ├── forms.py          # Formularios
│   ├── admin.py          # Configuración del admin
│   ├── urls.py           # URLs de la aplicación
│   └── templates/        # Plantillas HTML
│       └── cotizaciones/
├── static/               # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── images/
└── media/               # Archivos subidos por usuarios
```

## 🗄️ Modelos de Datos

### Cliente
- Información personal y de contacto
- Datos empresariales
- Estado activo/inactivo

### Servicio
- Nombre y descripción
- Tipo de servicio
- Tarifa por hora
- Estado activo/inactivo

### Cotización
- Número único automático
- Cliente asociado
- Modalidad de pago
- Estado de la cotización
- Cálculos automáticos (subtotal, descuento, IVA, total)
- Fechas de creación y vencimiento

### DetalleCotización
- Servicio específico
- Descripción del trabajo
- Horas estimadas
- Tarifa por hora
- Subtotal calculado automáticamente

## 🚀 Funcionalidades Principales

### 1. Crear Cotización
1. Seleccionar cliente
2. Configurar modalidad de pago
3. Establecer fechas y descuentos
4. Agregar servicios y horas
5. Generar PDF automáticamente

### 2. Gestión de Servicios
- Crear catálogo de servicios
- Configurar tarifas por hora
- Categorizar por tipo
- Mantener histórico

### 3. Dashboard
- Vista general del negocio
- Estadísticas en tiempo real
- Acceso rápido a funciones principales

### 4. Generación de PDFs
- Formato profesional
- Incluye todos los detalles
- Descarga directa
- Personalizable

## 🔧 Configuración

### Variables de Entorno
Crear un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Configuración de Base de Datos
Para usar PostgreSQL o MySQL, modificar `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cotizaciones_db',
        'USER': 'usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📱 Uso de la Aplicación

### Flujo de Trabajo Típico

1. **Configuración Inicial**
   - Crear servicios con tarifas
   - Registrar clientes
   - Configurar parámetros de IVA

2. **Crear Cotización**
   - Seleccionar cliente
   - Agregar servicios y horas
   - Configurar descuentos si aplica
   - Generar PDF

3. **Seguimiento**
   - Actualizar estados de cotizaciones
   - Revisar dashboard
   - Generar reportes

### Roles de Usuario

- **Administrador**: Acceso completo al sistema
- **Usuario**: Gestión de cotizaciones y clientes

## 🔒 Seguridad

- Autenticación de usuarios
- Protección CSRF
- Validación de formularios
- Sanitización de datos
- Logs de auditoría

## 📈 Escalabilidad

El sistema está diseñado para escalar:

- **Base de Datos**: Fácil migración a PostgreSQL/MySQL
- **Caché**: Configurable con Redis
- **Archivos Estáticos**: Servidos por CDN
- **Deployment**: Compatible con Docker

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para nueva funcionalidad
3. Commit los cambios
4. Push a la rama
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Para soporte técnico o consultas:
- Crear un issue en GitHub
- Contactar al equipo de desarrollo
- Revisar la documentación

## 🔄 Actualizaciones

### v1.0.0 (Actual)
- Sistema básico de cotizaciones
- Gestión de clientes y servicios
- Generación de PDFs
- Dashboard interactivo

### Próximas Versiones
- Integración con sistemas de facturación
- API REST para integraciones
- Notificaciones por email
- Reportes avanzados
- Múltiples monedas
- Plantillas personalizables

---

**Desarrollado con ❤️ para facilitar la gestión de cotizaciones de desarrollo de software.**

