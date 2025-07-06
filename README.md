# Easy Interfaces

> **Project that shows how easy it is to create a project using AI and Cursor tool.**

A modern full-stack application demonstrating the power of AI-assisted development with Cursor IDE. This project showcases a complete contribuinte (taxpayer) management system built from scratch using AI collaboration.

## 🚀 Tech Stack

### Backend
- **Python 3.11+** - Modern Python with type hints
- **FastAPI** - High-performance web framework for building APIs
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - Lightning-fast ASGI server

### Frontend
- **React 18** - Modern JavaScript library for building user interfaces
- **React Router** - Declarative routing for React
- **Axios** - Promise-based HTTP client
- **date-fns** - Modern JavaScript date utility library

## 📋 Features

### Core Functionality
- **Contribuinte Management** - Full CRUD operations for taxpayer records
- **Date-based Filtering** - Real-time data filtering by process date
- **Responsive Design** - Mobile-friendly interface
- **RESTful API** - Clean, documented API endpoints
- **Database Integration** - PostgreSQL with SQLAlchemy ORM

### User Interface
- **Modern UI/UX** - Beautiful gradient designs and smooth animations
- **Interactive Data Grid** - Sortable and filterable data tables
- **Real-time Updates** - Instant data fetching and display
- **Error Handling** - User-friendly error messages and loading states

### Development Features
- **Auto-generated API Docs** - Interactive Swagger/OpenAPI documentation
- **CORS Support** - Cross-origin resource sharing enabled
- **Environment Configuration** - Flexible configuration management
- **Type Safety** - Full type hints and validation

## 🏗️ Project Structure

```
cursor-easy/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration settings
│   │   ├── database.py      # Database setup
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── routers/
│   │       ├── __init__.py
│   │       └── contribuinte.py  # API routes
│   ├── main.py              # FastAPI application
│   ├── start.py             # Startup script
│   ├── requirements.txt     # Python dependencies
│   ├── env.example          # Environment template
│   └── README.md            # Backend documentation
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── HomePage.js
│   │   │   ├── HomePage.css
│   │   │   ├── ContribuintePage.js
│   │   │   ├── ContribuintePage.css
│   │   │   ├── WorkInProgressPage.js
│   │   │   └── WorkInProgressPage.css
│   │   ├── App.js           # Main React component
│   │   ├── App.css          # Global styles
│   │   └── index.js         # React entry point
│   ├── package.json         # Node.js dependencies
│   └── README.md            # Frontend documentation
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Node.js 16+**
- **PostgreSQL 15+**
- **Git**

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/cursor-easy.git
cd cursor-easy
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your PostgreSQL credentials

# Create PostgreSQL database and table
psql -U postgres -d postgres -c "
CREATE TABLE contribuinte (
    ref_id SERIAL PRIMARY KEY,
    dat_proce DATE NOT NULL,
    cpf_cnpj VARCHAR(14) NOT NULL,
    cliente VARCHAR(80) NOT NULL,
    email VARCHAR(255) UNIQUE,
    dat_cadastro DATE 
);"

# Start the backend server
python start.py
```

The backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### 3. Frontend Setup

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at: http://localhost:3000

## 📚 API Endpoints

### Contribuinte Management
- `GET /contribuinte/` - List all contribuintes
- `POST /contribuinte/` - Create a new contribuinte
- `GET /contribuinte/{ref_id}` - Get specific contribuinte by ID
- `GET /contribuinte/cpf/{cpf_cnpj}` - Get contribuinte by CPF/CNPJ
- `GET /contribuinte/by-date/{dat_proce}` - Get all contribuintes by process date
- `PUT /contribuinte/{ref_id}` - Update contribuinte
- `DELETE /contribuinte/{ref_id}` - Delete contribuinte

### Health Check
- `GET /health` - Application health status
- `GET /` - Welcome message and API info

## 🎯 How to Use

1. **Access the Application**: Open http://localhost:3000
2. **Main Menu**: You'll see "Easy Interfaces" with three options
3. **Contribuinte Management**: Click on "Contribuinte" to manage records
4. **Date Filtering**: Select a date to filter contribuinte records
5. **View Results**: Data is displayed in a responsive table format

## 🔧 Configuration

### Environment Variables (backend/.env)
```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres

# App Settings
DEBUG=True
```

### Database Schema
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

## 🤖 AI-Assisted Development

This project was created using **Cursor IDE** with AI assistance, demonstrating:

- **Rapid Prototyping** - Complete full-stack application in minutes
- **Code Generation** - AI-assisted component and API creation
- **Best Practices** - Industry-standard patterns and conventions
- **Error Resolution** - AI-powered debugging and problem-solving
- **Documentation** - Auto-generated comprehensive documentation

## 🛠️ Development

### Backend Development
```bash
cd backend
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
# Install dependencies
npm install

# Start development server
npm start
```

### Database Management
```bash
# Connect to PostgreSQL
psql -U postgres -d postgres

# View contribuinte table
SELECT * FROM contribuinte;
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Cursor IDE** - For making AI-assisted development accessible
- **FastAPI** - For the excellent Python web framework
- **React** - For the powerful frontend library
- **PostgreSQL** - For the reliable database system

## 📞 Support

If you have any questions or need help with this project:

- **Issues**: Create an issue on GitHub
- **Documentation**: Check the API docs at http://localhost:8000/docs
- **Backend README**: See `backend/README.md` for detailed backend documentation

---

**Built with ❤️ using AI and Cursor IDE**

*This project demonstrates the future of software development - where human creativity meets AI assistance to create amazing applications faster than ever before.* 