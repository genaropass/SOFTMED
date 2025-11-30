# Ciclo de Vida del Software - SofMed
## Sistema de Gestión Médica

**Versión:** 1.0  
**Fecha:** 2025  
**Desarrollado por:** GenPass

---

## Índice

1. [Planificación](#1-planificación)
2. [Análisis](#2-análisis)
3. [Diseño](#3-diseño)
4. [Implementación](#4-implementación)
5. [Pruebas](#5-pruebas)
6. [Despliegue](#6-despliegue)
7. [Mantenimiento](#7-mantenimiento)

---

## 1. Planificación

### 1.1 Objetivo del Proyecto

SofMed es un sistema de gestión médica diseñado para facilitar el registro y administración de pacientes en una clínica médica. El sistema permite a los pacientes registrarse de forma autónoma y a los médicos gestionar el historial clínico completo de cada paciente.

### 1.2 Necesidades Identificadas

- **Registro de Pacientes:** Los pacientes necesitan una forma sencilla de registrarse en el sistema sin necesidad de asistencia del personal médico.
- **Gestión de Información Médica:** Los médicos requieren acceso a información completa de los pacientes, incluyendo datos personales, servicios solicitados y obra social.
- **Historial Clínico:** Es fundamental mantener un registro detallado de todas las consultas, diagnósticos, tratamientos y observaciones médicas.
- **Seguridad y Acceso:** Diferencia entre acceso público (pacientes) y acceso restringido (médicos).
- **Búsqueda y Filtrado:** Capacidad de buscar pacientes rápidamente cuando hay muchos registrados.

### 1.3 Alcance del Proyecto

**Funcionalidades Principales:**
- Registro público de pacientes (página de inicio)
- Sistema de autenticación para médicos
- Gestión completa de pacientes (solo médicos)
- Historial clínico detallado
- Búsqueda de pacientes
- Interfaz web responsive y moderna

**Tecnologías Seleccionadas:**
- **Backend:** Django 4.2+ (Python)
- **Base de Datos:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **Framework CSS:** Diseño personalizado con tema médico azul/blanco

### 1.4 Recursos Necesarios

- Servidor web (desarrollo local o producción)
- Base de datos SQLite (archivo local)
- Navegador web moderno
- Python 3.8+
- Django 4.2+

---

## 2. Análisis

### 2.1 Requisitos Funcionales

#### RF1: Registro de Pacientes
- **Descripción:** Los pacientes deben poder registrarse desde la página principal.
- **Campos Requeridos:**
  - Nombre completo (obligatorio)
  - Fecha de nacimiento (obligatorio)
  - Género (obligatorio)
  - Servicio médico solicitado (opcional)
  - Obra social (opcional)
- **Validaciones:** Nombre único, formato de fecha válido.

#### RF2: Autenticación de Médicos
- **Descripción:** Solo los médicos autenticados pueden acceder al área de gestión.
- **Requisitos:**
  - Sistema de login con contraseña
  - Sesiones persistentes
  - Protección de rutas sensibles

#### RF3: Gestión de Pacientes
- **Descripción:** Los médicos pueden ver, buscar y gestionar pacientes.
- **Funcionalidades:**
  - Listado completo de pacientes
  - Búsqueda por nombre, género, ID, servicio médico u obra social
  - Visualización de información detallada

#### RF4: Historial Clínico
- **Descripción:** Los médicos pueden agregar y consultar el historial clínico de cada paciente.
- **Campos del Historial:**
  - Fecha de consulta (obligatorio)
  - Motivo de consulta/Notas (obligatorio)
  - Diagnóstico (opcional)
  - Tratamiento (opcional)
  - Observaciones adicionales (opcional) - para lesiones, problemas médicos, etc.

#### RF5: Interfaz de Usuario
- **Descripción:** Interfaz web moderna, responsive y fácil de usar.
- **Requisitos:**
  - Diseño médico profesional (tema azul/blanco)
  - Navegación intuitiva
  - Compatible con dispositivos móviles
  - Menú hamburguesa para móviles

### 2.2 Requisitos No Funcionales

#### RNF1: Rendimiento
- Carga rápida de páginas (< 2 segundos)
- Búsqueda eficiente en base de datos
- Manejo de hasta 1000+ pacientes sin degradación

#### RNF2: Seguridad
- Protección de rutas médicas
- Validación de datos de entrada
- Prevención de inyección SQL (usando parámetros)

#### RNF3: Usabilidad
- Interfaz intuitiva
- Mensajes de error claros
- Feedback visual para acciones del usuario

#### RNF4: Mantenibilidad
- Código bien estructurado y documentado
- Separación de responsabilidades
- Fácil extensión de funcionalidades

### 2.3 Modelo de Datos

**Tabla: pacientes**
- id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- nombre (TEXT, NOT NULL, UNIQUE)
- fecha_nacimiento (DATE, NOT NULL)
- genero (TEXT, NOT NULL)
- servicio_medico (TEXT, NULLABLE)
- obra_social (TEXT, NULLABLE)

**Tabla: visitas (historial clínico)**
- id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- fecha (TEXT, NOT NULL)
- notas (TEXT, NOT NULL)
- diagnostico (TEXT, NULLABLE)
- tratamiento (TEXT, NULLABLE)
- observaciones (TEXT, NULLABLE)
- id_paciente (INTEGER, NOT NULL, FOREIGN KEY)

---

## 3. Diseño

### 3.1 Arquitectura del Sistema

```
SofMed/
├── sofmed/              # Configuración Django
│   ├── settings.py      # Configuración del proyecto
│   ├── urls.py         # Enrutamiento principal
│   └── wsgi.py         # Servidor WSGI
├── clinica/            # Aplicación principal
│   ├── views.py        # Lógica de negocio
│   ├── templates/      # Plantillas HTML
│   └── urls.py         # Rutas de la aplicación
├── funciones/          # Funciones de base de datos
│   └── db.py          # Operaciones CRUD
├── static/             # Archivos estáticos
│   └── css/
│       └── style.css   # Estilos CSS
└── historial_clinico.db # Base de datos SQLite
```

### 3.2 Diseño de Interfaz

#### Páginas Principales:

1. **Página de Inicio (`/`)**
   - Formulario de registro de pacientes
   - Acceso público
   - Tarjetas informativas

2. **Login Médico (`/login-medico/`)**
   - Formulario de autenticación
   - Validación de contraseña
   - Redirección según autenticación

3. **Registro de Pacientes (`/registro-pacientes/`)**
   - Solo accesible para médicos
   - Lista de pacientes
   - Barra de búsqueda
   - Formulario para agregar pacientes

4. **Ver Paciente (`/paciente/<id>/`)**
   - Información completa del paciente
   - Formulario para agregar historial clínico
   - Visualización del historial completo

5. **Servicios (`/servicios/`)**
   - Información sobre servicios médicos

6. **Contacto (`/contacto/`)**
   - Información de contacto

### 3.3 Diseño de Base de Datos

**Relaciones:**
- Un paciente puede tener múltiples entradas en el historial clínico (1:N)
- Cada entrada del historial pertenece a un único paciente (N:1)

**Índices:**
- Índice en `pacientes.nombre` (búsqueda rápida)
- Índice en `visitas.id_paciente` (consultas eficientes)

### 3.4 Flujo de Usuario

#### Flujo de Registro de Paciente:
```
Usuario → Página Inicio → Completa Formulario → 
Sistema Valida → Guarda en BD → Muestra Mensaje de Éxito
```

#### Flujo de Médico:
```
Médico → Login → Autenticación → Registro Pacientes → 
Selecciona Paciente → Ver Historial → Agrega Entrada → 
Guarda en BD → Actualiza Vista
```

### 3.5 Funciones Principales

**Módulo: funciones/db.py**
- `crear_base_de_datos()`: Inicializa y migra la base de datos
- `calcular_edad()`: Calcula edad a partir de fecha de nacimiento
- `listar_pacientes()`: Obtiene todos los pacientes
- `buscar_pacientes()`: Búsqueda con filtros
- `obtener_paciente_por_id()`: Obtiene un paciente específico
- `obtener_historial_clinico()`: Obtiene historial de un paciente
- `agregar_historial_clinico()`: Agrega entrada al historial

**Módulo: clinica/views.py**
- `inicio()`: Maneja registro público de pacientes
- `login_medico()`: Autenticación de médicos
- `logout_medico()`: Cierre de sesión
- `registro_pacientes()`: Lista y búsqueda de pacientes
- `ver_paciente()`: Vista detallada del paciente
- `agregar_historial()`: Agrega entrada al historial
- `@requiere_medico`: Decorador de autenticación

---

## 4. Implementación

### 4.1 Configuración Inicial

**Dependencias (requirements.txt):**
```
Django>=4.2.0,<5.0.0
```

**Estructura de Proyecto Django:**
- Proyecto: `sofmed`
- Aplicación: `clinica`
- Base de datos: SQLite (`historial_clinico.db`)

### 4.2 Implementación de Funcionalidades

#### 4.2.1 Sistema de Autenticación

**Implementación:**
- Sesiones de Django para mantener estado de autenticación
- Decorador `@requiere_medico` para proteger vistas
- Página de login con validación de contraseña
- Redirección automática si no está autenticado

**Código Clave:**
```python
def requiere_medico(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('medico_autenticado'):
            return redirect('login_medico')
        return view_func(request, *args, **kwargs)
    return wrapper
```

#### 4.2.2 Gestión de Base de Datos

**Características:**
- Migración automática de esquema
- Validación de datos antes de inserción
- Manejo de errores (IntegrityError, etc.)
- Consultas optimizadas con índices

#### 4.2.3 Interfaz de Usuario

**Tecnologías:**
- HTML5 semántico
- CSS3 con variables personalizadas
- JavaScript vanilla para interactividad
- Font Awesome para iconos
- Diseño responsive con media queries

**Tema Visual:**
- Colores principales: Azul (#0066cc) y Blanco
- Gradientes para elementos destacados
- Sombras y transiciones suaves
- Tipografía: Segoe UI

### 4.3 Características Implementadas

✅ Registro público de pacientes  
✅ Autenticación de médicos  
✅ Listado y búsqueda de pacientes  
✅ Visualización de información del paciente  
✅ Agregar y consultar historial clínico  
✅ Interfaz responsive  
✅ Validación de formularios  
✅ Mensajes de éxito/error  
✅ Protección de rutas sensibles  

---

## 5. Pruebas

### 5.1 Pruebas Funcionales

#### 5.1.1 Registro de Pacientes
- ✅ Registro exitoso con todos los campos
- ✅ Validación de campos obligatorios
- ✅ Prevención de nombres duplicados
- ✅ Cálculo correcto de edad
- ✅ Manejo de campos opcionales

#### 5.1.2 Autenticación
- ✅ Login con contraseña correcta
- ✅ Rechazo de contraseña incorrecta
- ✅ Persistencia de sesión
- ✅ Redirección después de login
- ✅ Cierre de sesión funcional

#### 5.1.3 Búsqueda de Pacientes
- ✅ Búsqueda por nombre
- ✅ Búsqueda por ID
- ✅ Búsqueda por género
- ✅ Búsqueda por servicio médico
- ✅ Búsqueda por obra social
- ✅ Limpieza de búsqueda

#### 5.1.4 Historial Clínico
- ✅ Agregar entrada al historial
- ✅ Validación de campos obligatorios
- ✅ Visualización cronológica
- ✅ Campos opcionales funcionan correctamente

### 5.2 Pruebas de Interfaz

#### 5.2.1 Responsive Design
- ✅ Visualización correcta en desktop (1920x1080)
- ✅ Visualización correcta en tablet (768px)
- ✅ Visualización correcta en móvil (375px)
- ✅ Menú hamburguesa funcional
- ✅ Formularios adaptables

#### 5.2.2 Navegación
- ✅ Enlaces funcionan correctamente
- ✅ Botones de acción responden
- ✅ Mensajes de feedback visibles
- ✅ Estados de carga apropiados

### 5.3 Pruebas de Seguridad

- ✅ Protección de rutas médicas
- ✅ Validación de entrada de datos
- ✅ Prevención de SQL Injection (parámetros)
- ✅ Manejo seguro de sesiones

### 5.4 Casos de Prueba Ejecutados

| ID | Caso de Prueba | Estado | Observaciones |
|----|----------------|--------|---------------|
| CP001 | Registro de paciente nuevo | ✅ | Funciona correctamente |
| CP002 | Registro con nombre duplicado | ✅ | Muestra error apropiado |
| CP003 | Login médico correcto | ✅ | Redirige a registro pacientes |
| CP004 | Login médico incorrecto | ✅ | Muestra mensaje de error |
| CP005 | Acceso sin autenticación | ✅ | Redirige a login |
| CP006 | Búsqueda de paciente existente | ✅ | Encuentra resultados |
| CP007 | Búsqueda sin resultados | ✅ | Muestra mensaje apropiado |
| CP008 | Agregar historial clínico | ✅ | Guarda correctamente |
| CP009 | Visualizar historial completo | ✅ | Muestra todas las entradas |

### 5.5 Errores Encontrados y Corregidos

1. **Error:** Campos opcionales no se guardaban como NULL
   - **Solución:** Uso de `or None` en las vistas

2. **Error:** Búsqueda no incluía nuevos campos
   - **Solución:** Actualización de query SQL

3. **Error:** Decorador no preservaba nombre de función
   - **Solución:** Agregado `wrapper.__name__ = view_func.__name__`

---

## 6. Despliegue

### 6.1 Requisitos del Sistema

**Servidor:**
- Python 3.8 o superior
- Django 4.2 o superior
- Espacio en disco: mínimo 100 MB
- Memoria RAM: mínimo 512 MB

**Cliente:**
- Navegador web moderno (Chrome, Firefox, Edge, Safari)
- JavaScript habilitado
- Conexión a internet (para CDN de Font Awesome)

### 6.2 Instalación

#### Paso 1: Clonar o Descargar el Proyecto
```bash
# Si está en un repositorio Git
git clone [url-del-repositorio]

# O descargar y extraer el archivo ZIP
```

#### Paso 2: Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### Paso 3: Configurar Base de Datos
```bash
# La base de datos se crea automáticamente al ejecutar
# No se requieren migraciones adicionales
```

#### Paso 4: Ejecutar Servidor de Desarrollo
```bash
python manage.py runserver
```

#### Paso 5: Acceder a la Aplicación
```
Abrir navegador en: http://127.0.0.1:8000/
```

### 6.3 Configuración de Producción

#### 6.3.1 Variables de Entorno
```python
# En settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']
SECRET_KEY = 'cambiar-por-clave-segura'
```

#### 6.3.2 Base de Datos
- Para producción, considerar migrar a PostgreSQL o MySQL
- Configurar backups automáticos
- Implementar replicación si es necesario

#### 6.3.3 Servidor Web
- **Opción 1:** Apache con mod_wsgi
- **Opción 2:** Nginx con Gunicorn
- **Opción 3:** Servicios en la nube (Heroku, AWS, etc.)

#### 6.3.4 Archivos Estáticos
```bash
python manage.py collectstatic
```

### 6.4 Seguridad en Producción

**Cambios Necesarios:**
1. Cambiar contraseña de médico en `views.py`
2. Usar variables de entorno para SECRET_KEY
3. Habilitar HTTPS
4. Configurar firewall
5. Implementar rate limiting
6. Configurar logs de seguridad

### 6.5 Monitoreo

**Métricas a Monitorear:**
- Tiempo de respuesta del servidor
- Uso de memoria y CPU
- Errores en logs
- Número de pacientes registrados
- Accesos de médicos

---

## 7. Mantenimiento

### 7.1 Mantenimiento Correctivo

**Procedimiento para Reportar Errores:**
1. Documentar el error con:
   - Descripción detallada
   - Pasos para reproducir
   - Comportamiento esperado vs. actual
   - Capturas de pantalla si aplica

2. Priorizar según:
   - Severidad (Crítico, Alto, Medio, Bajo)
   - Impacto en usuarios
   - Frecuencia de ocurrencia

3. Resolución:
   - Identificar causa raíz
   - Implementar corrección
   - Probar solución
   - Desplegar actualización

### 7.2 Mantenimiento Adaptativo

**Adaptaciones Necesarias:**
- Actualización de Django cuando haya nuevas versiones
- Actualización de dependencias de seguridad
- Adaptación a cambios en navegadores
- Compatibilidad con nuevos dispositivos

**Proceso:**
```bash
# Verificar actualizaciones
pip list --outdated

# Actualizar dependencias
pip install --upgrade django

# Probar después de actualización
python manage.py test
```

### 7.3 Mantenimiento Perfectivo

#### 7.3.1 Mejoras Planificadas

**Corto Plazo:**
- [ ] Sistema de autenticación con Django Auth
- [ ] Exportación de historial a PDF
- [ ] Notificaciones por email
- [ ] Dashboard con estadísticas

**Mediano Plazo:**
- [ ] API REST para integraciones
- [ ] Aplicación móvil
- [ ] Sistema de citas médicas
- [ ] Integración con sistemas de facturación

**Largo Plazo:**
- [ ] Inteligencia artificial para diagnósticos
- [ ] Telemedicina
- [ ] Integración con dispositivos médicos
- [ ] Análisis predictivo de salud

#### 7.3.2 Optimizaciones

**Rendimiento:**
- Implementar caché para consultas frecuentes
- Optimizar queries con select_related
- Compresión de archivos estáticos
- CDN para recursos estáticos

**Base de Datos:**
- Índices adicionales según uso
- Particionamiento de tablas grandes
- Archivo de datos antiguos

### 7.4 Documentación

**Documentación a Mantener:**
- README.md: Instrucciones de instalación
- CICLO_DE_VIDA_SOFTWARE.md: Este documento
- Comentarios en código
- Manual de usuario
- Manual técnico

### 7.5 Backup y Recuperación

**Estrategia de Backup:**
- Backup diario de base de datos
- Backup semanal completo del proyecto
- Almacenamiento en ubicación segura
- Pruebas de restauración mensuales

**Comando de Backup:**
```bash
# Backup de base de datos
cp historial_clinico.db backups/historial_clinico_$(date +%Y%m%d).db

# Backup completo
tar -czf backups/sofmed_backup_$(date +%Y%m%d).tar.gz .
```

### 7.6 Plan de Contingencia

**Escenarios:**
1. **Caída del Servidor:**
   - Tener servidor de respaldo
   - Restaurar desde último backup
   - Tiempo de recuperación: < 1 hora

2. **Corrupción de Base de Datos:**
   - Restaurar desde backup
   - Verificar integridad
   - Tiempo de recuperación: < 30 minutos

3. **Ataque de Seguridad:**
   - Aislar sistema afectado
   - Cambiar credenciales
   - Auditar logs
   - Notificar a usuarios si es necesario

### 7.7 Actualizaciones de Seguridad

**Proceso:**
1. Monitorear avisos de seguridad de Django
2. Aplicar parches críticos inmediatamente
3. Probar en ambiente de desarrollo
4. Desplegar en producción
5. Documentar cambios

---

## Conclusiones

SofMed ha sido desarrollado siguiendo un ciclo de vida de software estructurado, desde la planificación inicial hasta el despliegue y mantenimiento continuo. El sistema cumple con los requisitos funcionales y no funcionales establecidos, proporcionando una solución completa para la gestión médica.

**Logros Principales:**
- ✅ Sistema funcional y probado
- ✅ Interfaz moderna y responsive
- ✅ Seguridad implementada
- ✅ Código mantenible y documentado
- ✅ Base sólida para futuras expansiones

**Próximos Pasos:**
- Implementar mejoras planificadas
- Recopilar feedback de usuarios
- Optimizar rendimiento según uso real
- Expandir funcionalidades según necesidades

---

**Documento generado:** 2025  
**Última actualización:** 2025  
**Versión del Software:** 1.0  
**Desarrollado por:** GenPass

---

*Este documento describe el ciclo de vida completo del software SofMed. Para más información técnica, consultar el código fuente y la documentación inline.*





