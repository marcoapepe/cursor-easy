# Cursor Easy Backend

A modern FastAPI backend with PostgreSQL database integration for Contribuinte management.

## Features

- 🗄️ **PostgreSQL Database** - PostgreSQL database with SQLAlchemy ORM
- 📝 **Contribuinte Management** - Full CRUD operations for contribuintes
- 🌐 **CORS Support** - Ready for frontend integration
- 📚 **Auto-generated API Docs** - Interactive API documentation

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Setup

Copy the example environment file and configure it:

```bash
cp env.example .env
```

Edit `.env` with your settings:
- `DATABASE_URL`: PostgreSQL connection string (default: postgresql://postgres:postgres@localhost:5432/postgres)
- `DEBUG`: Set to False in production

### 3. Database Setup

Make sure PostgreSQL is running and the `contribuinte` table exists:

```sql
CREATE TABLE contribuinte (
    ref_id SERIAL PRIMARY KEY,
    dat_proce DATE NOT NULL,
    cpf_cnpj VARCHAR(14) NOT NULL,
    cliente VARCHAR(80) NOT NULL,
    email VARCHAR(255) UNIQUE,
    dat_cadastro DATE 
);
```

### 4. Run the Application

```bash
# Option 1: Using the startup script
python start.py

# Option 2: Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Contribuinte Management
- `GET /contribuinte/` - List all contribuintes
- `POST /contribuinte/` - Create a new contribuinte
- `GET /contribuinte/{ref_id}` - Get specific contribuinte by ID
- `GET /contribuinte/cpf/{cpf_cnpj}` - Get contribuinte by CPF/CNPJ
- `GET /contribuinte/by-date/{dat_proce}` - Get all contribuintes by process date
- `PUT /contribuinte/{ref_id}` - Update contribuinte
- `DELETE /contribuinte/{ref_id}` - Delete contribuinte

### Date Format
For the `/by-date/{dat_proce}` endpoint, use the YYYY-MM-DD format:
- Example: `GET /contribuinte/by-date/2024-01-15`

## Database Models

### Contribuinte (contribuinte table)
- `ref_id`: Primary key (SERIAL)
- `dat_proce`: Process date (DATE, NOT NULL)
- `cpf_cnpj`: CPF or CNPJ number (VARCHAR(14), NOT NULL)
- `cliente`: Client name (VARCHAR(80), NOT NULL)
- `email`: Email address (VARCHAR(255), UNIQUE)
- `dat_cadastro`: Registration date (DATE)

## Development

### Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database setup
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   └── routers/
│       ├── __init__.py
│       └── contribuinte.py # Contribuinte management routes
├── main.py               # FastAPI application
├── start.py              # Startup script
├── requirements.txt      # Python dependencies
├── env.example          # Environment variables template
└── README.md            # This file
```

### Adding New Features

1. **New Models**: Add to `app/models.py`
2. **New Schemas**: Add to `app/schemas.py`
3. **New Routes**: Create in `app/routers/` and include in `main.py`
4. **Database Migrations**: Use Alembic for production databases

## Security

- CORS configured for frontend integration
- Input validation with Pydantic schemas
- Unique constraints on CPF/CNPJ and email

## Production Deployment

1. Set `DEBUG=False` in environment
2. Use a production PostgreSQL database
3. Configure proper CORS origins
4. Use a production ASGI server (Gunicorn + Uvicorn)

## License

MIT License 