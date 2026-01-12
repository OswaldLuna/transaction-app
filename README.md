# Sistema de Gestión de Transacciones

Sistema completo de gestión de transacciones con procesamiento asíncrono, notificaciones en tiempo real vía WebSocket y funcionalidad RPA para extracción de datos de Wikipedia.

## 🚀 Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno para Python
- **PostgreSQL** - Base de datos relacional
- **Redis** - Cache y message broker
- **RQ (Redis Queue)** - Sistema de colas para procesamiento asíncrono
- **SQLAlchemy** - ORM para Python
- **WebSockets** - Comunicación bidireccional en tiempo real
- **Playwright** - Automatización de navegador para RPA
- **OpenAI API** - Generación de resúmenes con IA

### Frontend
- **React 19** + **TypeScript** - Framework UI
- **Vite** - Build tool y dev server
- **Tailwind CSS v4** - Framework de estilos
- **Axios** - Cliente HTTP
- **react-hot-toast** - Sistema de notificaciones
- **WebSocket API** - Actualizaciones en tiempo real

### Infraestructura
- **Docker & Docker Compose** - Contenedorización y orquestación

## 📋 Requisitos Previos

- Docker (v20.10+)
- Docker Compose (v2.0+)
- Archivo `.env` en la raíz del proyecto

## ⚙️ Configuración

### 1. Crear archivo `.env`

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_password_seguro
POSTGRES_DB=transactions_db
DATABASE_HOST=db
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# OpenAI
OPENAI_API_KEY=tu_api_key_de_openai
```

## 🚀 Instalación y Ejecución

### Ejecutar todo con Docker Compose (Recomendado)

```bash
# Construir e iniciar todos los servicios
docker-compose up --build

# O en modo detached (segundo plano)
docker-compose up -d
```

Esto iniciará:
- **PostgreSQL** en el puerto `5432`
- **Redis** en el puerto `6379`
- **Backend API** en el puerto `8000`
- **Worker RQ** para procesamiento asíncrono
- **Frontend** en el puerto `5173`

### Verificar que todo está corriendo

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Documentación API: http://localhost:8000/docs

## 📖 Uso de la Aplicación

### Crear una Transacción

1. Accede a http://localhost:5173
2. Completa el formulario:
   - **User ID**: ID del usuario (número positivo)
   - **Monto**: Cantidad de la transacción
   - **Tipo**: Depósito o Retiro
3. Click en "Crear"

### Flujo de Procesamiento

1. **Creación**: La transacción se crea con estado `pendiente`
2. **Procesamiento Asíncrono**: 
   - Se encola automáticamente en Redis Queue
   - El worker procesa la transacción (simula 5 segundos de procesamiento)
   - El estado cambia a `procesado` o `fallido`
3. **Notificaciones en Tiempo Real**:
   - WebSocket envía actualizaciones de estado
   - Aparecen toasts informativos:
     - ✅ "Transacción #X → procesada"
     - ❌ "Transacción #X → fallida"

### Deduplicación

El sistema usa hashing para evitar transacciones duplicadas:
- Hash basado en: `user_id + amount + type`
- Si intentas crear una transacción idéntica, retorna la existente
- Si ya fue procesada, muestra: "Esta transacción #X ya fue procesada"

## 🤖 Funcionalidad RPA

El sistema incluye un script RPA para extraer información de Wikipedia:

```bash
# Ejecutar el RPA (requiere que el backend esté corriendo)
docker-compose exec backend python app/rpa/wiki_rpa.py
```

**Funcionalidad:**
1. Abre Wikipedia en español
2. Busca un término (ej: "Automatización")
3. Extrae el primer párrafo
4. Envía el texto al backend para generar un resumen con OpenAI
5. Imprime el resumen generado

## 🏗️ Estructura del Proyecto

```
transaction_technical_test/
├── backend/
│   ├── app/
│   │   ├── routers/          # Endpoints de la API
│   │   │   ├── transactions.py  # CRUD y WebSocket
│   │   │   └── assistant.py     # Integración con OpenAI
│   │   ├── workers/          # Procesamiento asíncrono
│   │   │   ├── tasks.py         # Definición de tareas
│   │   │   └── redis_conn.py    # Conexión a Redis
│   │   ├── rpa/              # Scripts de automatización
│   │   │   └── wiki_rpa.py      # Extracción de Wikipedia
│   │   ├── models.py         # Modelos SQLAlchemy
│   │   ├── schemas.py        # Schemas Pydantic
│   │   ├── db.py             # Configuración de BD
│   │   └── main.py           # Aplicación principal
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   │   ├── TransactionForm.tsx
│   │   │   └── TransactionList.tsx
│   │   ├── hooks/            # Custom hooks
│   │   │   └── useWebSocket.ts
│   │   ├── services/         # Servicios HTTP
│   │   │   └── api.ts
│   │   ├── types.ts          # Definiciones TypeScript
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── .env
```

## 📡 API Endpoints

### Transacciones

#### `POST /transactions/create`
Crea una nueva transacción (o retorna existente si es duplicada)

**Body:**
```json
{
  "user_id": 1,
  "amount": 100.50,
  "type": "deposit"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "amount": 100.50,
  "type": "deposit",
  "status": "pendiente",
  "hash": "abc123...",
  "created_at": "2026-01-11T12:00:00"
}
```

#### `POST /transactions/async-process`
Encola una transacción para procesamiento asíncrono

**Body:**
```json
{
  "transaction_id": 1
}
```

**Restricciones:**
- Solo procesa transacciones con estado `pendiente` o `fallido`
- Retorna error 400 si el estado es diferente

#### `WS /transactions/stream`
WebSocket para recibir actualizaciones en tiempo real

**Mensaje recibido:**
```json
{
  "id": 1,
  "status": "procesado"
}
```

### Asistente IA

#### `POST /assistant/summarize`
Genera un resumen de texto usando OpenAI

**Body:**
```json
{
  "text": "Texto largo a resumir..."
}
```

## 🔧 Comandos Útiles

### Docker Compose

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f worker

# Reiniciar un servicio
docker-compose restart backend
docker-compose restart worker

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes (limpia la BD)
docker-compose down -v

# Reconstruir después de cambios en requirements/package.json
docker-compose up --build
```

### Base de Datos

```bash
# Acceder a PostgreSQL
docker-compose exec db psql -U postgres -d transactions_db

# Ver todas las transacciones
SELECT * FROM transactions;
```

### Redis

```bash
# Acceder a Redis CLI
docker-compose exec redis redis-cli

# Ver trabajos encolados
LRANGE rq:queue:transq 0 -1

# Ver todos los keys
KEYS *
```

## 📝 Notas Adicionales

- **Procesamiento**: Cada transacción tarda ~5 segundos en procesarse (simulación)
- **Persistencia**: Los datos se mantienen en volúmenes de Docker
- **Hot Reload**: Tanto backend como frontend tienen recarga automática durante desarrollo
- **Worker**: Requiere reinicio manual después de cambios en `tasks.py`

## 📄 Licencia

Este proyecto es de uso educativo/técnico.
