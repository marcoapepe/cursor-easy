# Multi-Database Setup

This backend now supports multiple modules with different databases:

## Database Configuration

### Module A
- **Database**: `database1`
- **Connection**: `postgresql://postgres:postgres@localhost:5432/database1`
- **Environment Variable**: `DATABASE_URL_A`

### Module B
- **Database**: `database2`
- **Connection**: `postgresql://postgres:postgres@localhost:5432/database2`
- **Environment Variable**: `DATABASE_URL_B`

## Setup Instructions

### 1. Create Databases

First, create the two databases in PostgreSQL:

```sql
-- Connect to PostgreSQL as postgres user
CREATE DATABASE database1;
CREATE DATABASE database2;
```

### 2. Environment Configuration

Copy the environment variables to your `.env` file:

```bash
# Copy from env.example
cp env.example .env
```

The `.env` file should contain:

```env
# Database URLs for different modules
DATABASE_URL_A=postgresql://postgres:postgres@localhost:5432/database1
DATABASE_URL_B=postgresql://postgres:postgres@localhost:5432/database2

# Legacy support for backward compatibility
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres

# App Settings
DEBUG=True
```

### 3. Test the Setup

Run the test script to verify everything is working:

```bash
python test_multi_db.py
```

This will:
- Test database connections
- Create tables in both databases
- Test sample data operations

### 4. Start the Server

```bash
python start.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Usage

All endpoints now accept a `module` parameter to specify which database to use:

### Examples

#### Get all contribuintes from Module A
```bash
curl "http://localhost:8000/contribuinte/?module=A"
```

#### Get all contribuintes from Module B
```bash
curl "http://localhost:8000/contribuinte/?module=B"
```

#### Create a contribuinte in Module A
```bash
curl -X POST "http://localhost:8000/contribuinte/?module=A" \
  -H "Content-Type: application/json" \
  -d '{
    "dat_proce": "2024-01-15",
    "cpf_cnpj": "12345678901",
    "cliente": "Test Client",
    "email": "test@example.com",
    "dat_cadastro": "2024-01-15"
  }'
```

#### Get contribuintes by date from Module B
```bash
curl "http://localhost:8000/contribuinte/by-date/2024-01-15?module=B"
```

#### Get contribuintes by client name from Module A
```bash
curl "http://localhost:8000/contribuinte/by-client/Pepe?module=A"
```

#### Upload CSV file to Module B
```bash
curl -X POST "http://localhost:8000/contribuinte/bulk-upload?module=B" \
  -F "file=@novos_contribuintes.txt"
```

## Default Behavior

- If no `module` parameter is provided, it defaults to Module A
- The legacy database connection is maintained for backward compatibility
- All endpoints support both modules

## Database Schema

Both databases use the same schema:

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

## Frontend Integration

The frontend can now:
1. Add radio buttons to select between Module A and Module B
2. Pass the selected module as a query parameter to all API calls
3. Display data from the selected module

## Troubleshooting

### Connection Issues
- Verify PostgreSQL is running
- Check database names exist
- Verify credentials in environment variables

### Table Creation Issues
- Run the test script to verify table creation
- Check database permissions

### Data Isolation
- Each module's data is completely isolated
- No cross-module data sharing
- Each module has its own `contribuinte` table 