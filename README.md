# 🧠 Backend Calendarios – Arquitectura Hexagonal

Este repositorio implementa un sistema backend para la gestión de calendarios empresariales, procesos y hitos asociados a clientes, respetando los principios de la **arquitectura hexagonal (puertos y adaptadores)** y **principios SOLID**.

---

## 📦 Estructura de Carpetas

```plaintext
calendarios_back_hexagonal/
│
├── app/
│   ├── domain/                       
│   │   ├── entities/                 
│   │   └── repositories/            
│   │
│   ├── application/                 
│   │   └── use_cases/
│   │       ├── procesos/
│   │       ├── hitos/
│   │       ├── clientes/
│   │       ├── plantilla/
│   │       ├── plantilla_proceso/
│   │       ├── cliente_proceso/
│   │       └── cliente_proceso_hito/
│   │
│   ├── infrastructure/              
│   │   ├── db/
│   │   │   ├── database.py          
│   │   │   ├── models/              
│   │   │   └── repositories/        
│   │   └── api/
│   │       └── v1/
│   │           └── endpoints/       
│   │
│   └── main.py                      
│
├── tests/                           
├── scripts/                         
│   ├── mock_data.py
│   └── test_endpoints.py
│
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## ⚙️ Flujo de una Petición

1. El cliente lanza una petición a un endpoint de FastAPI (`/v1/...`)
2. El endpoint recibe la solicitud, extrae los datos y llama a un **caso de uso**
3. El caso de uso invoca a un repositorio **abstracto**
4. Este es inyectado por su implementación concreta (`*_repository_sql.py`)
5. El repositorio ejecuta operaciones con la BBDD a través del ORM SQLAlchemy
6. El resultado se devuelve hacia el cliente

---

## 🧠 Entidades Disponibles

| Entidad                  | Descripción                                      |
|--------------------------|--------------------------------------------------|
| **Proceso**              | Flujo empresarial recurrente                     |
| **Hito**                 | Evento o tarea específica de un proceso          |
| **Plantilla**            | Configuración base con procesos predefinidos     |
| **Cliente**              | Entidad externa consumida desde otra plataforma |
| **ProcesoHitoMaestro**   | Relación entre procesos e hitos base             |
| **PlantillaProceso**     | Asociación entre plantilla y procesos            |
| **ClienteProceso**       | Asignación de procesos a clientes                |
| **ClienteProcesoHito**   | Hitos derivados del cliente_proceso             |

---

## 🔗 Relaciones entre Tablas

```plaintext
Plantilla ⟷ PlantillaProceso ⟶ Proceso
Proceso ⟷ ProcesoHitoMaestro ⟶ Hito

Cliente ⟶ ClienteProceso ⟶ Proceso
ClienteProceso ⟶ ClienteProcesoHito ⟶ Hito (vía ProcesoHitoMaestro)
```

---

## 📆 Generación de Calendarios por Temporalidad

Este sistema permite crear automáticamente registros de `ClienteProceso` en función de la `temporalidad` y `frecuencia` definidas en un `Proceso` maestro.

---

### 🧠 Diseño aplicado

Se ha implementado el **Patrón Estrategia** para separar la lógica de cada tipo de temporalidad en clases individuales, y un **módulo fábrica** para seleccionar dinámicamente la estrategia adecuada.

Ventajas:
- Abierto a nuevas temporalidades sin romper el código existente (Open/Closed).
- Testeable por unidad.
- Código limpio y mantenible.

---

### 📁 Ubicación del código

La lógica de generación se encuentra en:

```
app/application/services/generadores_temporalidad/
```

Contiene:

- `base_generador.py`: Interfaz base (abstracta).
- `factory.py`: Fábrica para obtener el generador según la temporalidad.
- `generador_mensual.py`: Lógica para temporalidad "mes".
- `generador_semanal.py`: Lógica para "semana".
- `generador_diario.py`: Lógica para "día".
- `generador_quincenal.py`: Cada 15 días.
- `generador_trimestral.py`: Tramos fijos de 3 meses.

---

### 🔁 Temporalidades soportadas

| Temporalidad  | Descripción                         |
|---------------|-------------------------------------|
| `dia`         | Procesos generados cada X días      |
| `semana`      | Procesos generados cada X semanas   |
| `quincena`    | Procesos cada 15 días exactos       |
| `mes`         | Procesos cada X meses               |
| `trimestre`   | Procesos cada 3 meses (fijo)        |

---

### ⚙️ Cómo se usa

Desde el use case:

```python
from app.application.services.generadores_temporalidad.factory import obtener_generador

def generar_calendario_cliente_proceso(...):
    generador = obtener_generador(proceso_maestro.temporalidad)
    return generador.generar(data, proceso_maestro, repo)
```

---

### 🧩 Añadir nuevas temporalidades

1. Crear `generador_mitemporalidad.py` en `generadores_temporalidad/`.
2. Heredar de `GeneradorTemporalidad` e implementar `generar(...)`.
3. Registrar en `factory.py`:

```python
elif temporalidad == "mitemporalidad":
    return GeneradorMiTemporalidad()
```

---

## ✍️ Proceso para Agregar Nuevas Entidades

1. **Dominio**
   - Crear clase en `entities/`
   - Crear interfaz abstracta en `repositories/`

2. **Casos de Uso**
   - Crear funciones específicas en `use_cases/<entidad>/`

3. **Infraestructura**
   - Crear modelo en `models/`
   - Crear repositorio en `repositories/`

4. **API**
   - Crear endpoint en `endpoints/`

5. **Mocks y Test**
   - Agregar mocks en `scripts/mock_data.py`
   - Agregar pruebas en `scripts/test_endpoints.py`

---

## 🛠️ Cambio de Motor de Base de Datos

1. Crear una nueva clase repositorio implementando la interfaz
2. Sustituir la inyección en los endpoints
3. ¡El dominio y casos de uso no se tocan! ✅

---

## 🧪 Scripts Disponibles

| Script                | Descripción                            |
|-----------------------|----------------------------------------|
| `mock_data.py`        | Inserta datos simulados en la BBDD     |
| `test_endpoints.py`   | Ejecuta tests para todos los endpoints |

---

## ✅ Buenas Prácticas Aplicadas

- Arquitectura hexagonal limpia
- Responsabilidad única y principios SOLID
- Separación entre lógica de negocio, aplicación y persistencia
- Fácil testeo, mantenimiento y escalabilidad

---

# 🔐 Autenticación API por API Key + JWT

Este proyecto implementa un sistema de autenticación simple y seguro basado en creación de clientes API, generación de claves y uso de JWTs para acceder a rutas protegidas.

---

## 1️⃣ Crear un nuevo cliente API

**Endpoint:**  
`POST /admin/api-clientes`

**Headers:**
- `x-admin-key: <CLAVE_SECRETA_ADMIN>`

**Body (JSON):**
```json
{
  "nombre_cliente": "cliente_demo"
}
```

**Respuesta:**
```json
{
  "mensaje": "Cliente creado",
  "api_key": "KZURpV7R2Fn0L3DKGk8vdHjZyNqUs9kEIxDdSytaz",
  "cliente": "cliente_demo"
}
```

⚠️ **IMPORTANTE:** La `api_key` se muestra **una sola vez**.  
Esta clave sirve como contraseña del cliente. No se almacena en texto plano en la base de datos.

---

## 2️⃣ Obtener un token JWT

**Endpoint:**  
`POST /token`

**Headers:**
- `Content-Type: application/x-www-form-urlencoded`

**Body (form-data):**
```
username=cliente_demo
password=KZURpV7R2Fn0L3DKGk8vdHjZyNqUs9kEIxDdSytaz
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 3️⃣ Acceder a endpoints protegidos

Una vez con el `access_token`, inclúyelo en la cabecera:

**Ejemplo de request:**
```http
GET /clientes
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...
```

---

## 4️⃣ Manejo de errores

Si el token es inválido o ha expirado, se devuelve:

```json
{
  "detail": "Token inválido o expirado"
}
```

Esto permite al cliente frontend detectar el estado de la sesión y redirigir al login si es necesario.

---

## 🧪 Ejemplo de uso con curl

```bash
# Crear cliente API (admin)
curl -X POST http://localhost:8088/admin/api-clientes   -H "x-admin-key: <CLAVE_ADMIN>"   -H "Content-Type: application/json"   -d '{"nombre_cliente": "cliente_demo"}'

# Obtener token
curl -X POST http://localhost:8088/token   -H "Content-Type: application/x-www-form-urlencoded"   -d "username=cliente_demo"   -d "password=<CLAVE_ENTREGADA>"

# Usar token
curl http://localhost:8088/clientes   -H "Authorization: Bearer <ACCESS_TOKEN>"

#### Endpoints disponibles

| Método | Ruta                          | Acción                                      |
|--------|-------------------------------|---------------------------------------------|
| GET    | `/admin/api-clientes`         | Lista todos los clientes API                |
| POST   | `/admin/api-clientes`         | Crea un nuevo cliente y genera su API Key   |
| PUT    | `/admin/api-clientes/{id}`    | Activa o desactiva una clave existente      |

