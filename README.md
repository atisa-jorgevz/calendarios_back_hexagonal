
# Arquitectura Hexagonal – Proyecto Backend Calendarios

Este proyecto sigue el patrón de **arquitectura hexagonal (puertos y adaptadores)**.

---

## 🧱 Estructura de Carpetas

```plaintext
calendarios_back_hexagonal/
│
├── app/
│   ├── domain/                       # Núcleo de dominio
│   │   ├── entities/                 # Entidades del negocio
│   │   │   └── proceso.py
│   │   └── repositories/            # Interfaces (puertos de salida)
│   │       └── proceso_repository.py
│   │
│   ├── application/                 # Casos de uso (lógica de aplicación)
│   │   └── use_cases/
│   │       ├── procesos/            # Casos de uso por entidad
│   │       │   ├── crear_proceso.py
│   │       │   ├── listar_procesos.py
│   │       │   └── ...
│   │       └── hitos/
│   │           └── ...
│   │
│   ├── infrastructure/              # Adaptadores (puertos de entrada/salida)
│   │   ├── db/
│   │   │   ├── database.py          # Config SQLAlchemy
│   │   │   ├── models/              # Modelos ORM
│   │   │   │   └── proceso_model.py
│   │   │   └── repositories/        # Repositorios implementados
│   │   │       └── proceso_repository_sql.py
│   │   └── api/
│   │       └── v1/
│   │           └── endpoints/       # Endpoints FastAPI
│   │               └── proceso.py
│   │
│   └── main.py                      # Arranque FastAPI
│
├── tests/                           # (Opcional) Pruebas unitarias
│
├── scripts/                         # Mock de datos y test funcionales
│   ├── mock_data.py
│   └── test_endpoints.py
│
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## ⚙️ Flujo de una Petición

1. **Petición** desde el cliente a un endpoint (e.g. `/procesos`)
2. **Endpoint** en `infrastructure/api/v1/endpoints` recibe y extrae los datos
3. Se inyecta el repositorio correspondiente (`ProcesoRepositorySQL`)
4. Se **invoca un caso de uso** en `application/use_cases/procesos/...`
5. El caso de uso invoca la interfaz del repositorio (`domain.repositories`)
6. Se ejecuta la lógica real desde `infrastructure.db.repositories`
7. Se devuelve el resultado al endpoint → cliente

---

## 🔄 Cambio de Motor de Base de Datos

Para migrar de SQL Server a PostgreSQL ( por ejemplo ):

1. Crear un nuevo repositorio `ProcesoRepositoryPostgres` implementando la misma interfaz.
2. Sustituir la dependencia en los endpoints (`get_repo()`).
3. No hay que modificar lógica de dominio ni casos de uso. 💪

---

## 🧪 Tests y Scripts

- `mock_data.py`: rellena la base con datos de prueba.
- `test_endpoints.py`: testea el CRUD completo de procesos e hitos.

---

## ✅ Buenas Prácticas

- Separación clara entre dominio, casos de uso y adaptadores.
- Aplicación de los principios SOLID.
- Bajo acoplamiento = fácil mantenimiento y escalabilidad.

---


