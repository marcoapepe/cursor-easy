#!/usr/bin/env python3
"""
Test script to verify multi-database setup
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import engine_a, engine_b, SessionLocalA, SessionLocalB
from app import models
from app.config import settings

def test_database_connections():
    """Test database connections for both modules"""
    print("Testing database connections...")
    
    # Test Module A database
    try:
        with SessionLocalA() as db:
            result = db.execute(text("SELECT 1"))
            print("✅ Module A database connection successful")
    except Exception as e:
        print(f"❌ Module A database connection failed: {e}")
        return False
    
    # Test Module B database
    try:
        with SessionLocalB() as db:
            result = db.execute(text("SELECT 1"))
            print("✅ Module B database connection successful")
    except Exception as e:
        print(f"❌ Module B database connection failed: {e}")
        return False
    
    return True

def test_table_creation():
    """Test table creation in both databases"""
    print("\nTesting table creation...")
    
    # Create tables in Module A database
    try:
        models.Base.metadata.create_all(bind=engine_a)
        print("✅ Tables created in Module A database")
    except Exception as e:
        print(f"❌ Failed to create tables in Module A database: {e}")
        return False
    
    # Create tables in Module B database
    try:
        models.Base.metadata.create_all(bind=engine_b)
        print("✅ Tables created in Module B database")
    except Exception as e:
        print(f"❌ Failed to create tables in Module B database: {e}")
        return False
    
    return True

def test_sample_data():
    """Test inserting and retrieving sample data"""
    print("\nTesting sample data operations...")
    
    # Test Module A
    try:
        with SessionLocalA() as db:
            # Insert sample data
            sample_data = models.Contribuinte(
                dat_proce="2024-01-15",
                cpf_cnpj="12345678901",
                cliente="Test Client A",
                email="testa@example.com",
                dat_cadastro="2024-01-15"
            )
            db.add(sample_data)
            db.commit()
            
            # Retrieve data
            result = db.query(models.Contribuinte).filter(
                models.Contribuinte.cpf_cnpj == "12345678901"
            ).first()
            
            if result:
                print("✅ Module A: Sample data inserted and retrieved successfully")
                # Clean up
                db.delete(result)
                db.commit()
            else:
                print("❌ Module A: Failed to retrieve sample data")
                return False
                
    except Exception as e:
        print(f"❌ Module A: Sample data test failed: {e}")
        return False
    
    # Test Module B
    try:
        with SessionLocalB() as db:
            # Insert sample data
            sample_data = models.Contribuinte(
                dat_proce="2024-01-15",
                cpf_cnpj="98765432109",
                cliente="Test Client B",
                email="testb@example.com",
                dat_cadastro="2024-01-15"
            )
            db.add(sample_data)
            db.commit()
            
            # Retrieve data
            result = db.query(models.Contribuinte).filter(
                models.Contribuinte.cpf_cnpj == "98765432109"
            ).first()
            
            if result:
                print("✅ Module B: Sample data inserted and retrieved successfully")
                # Clean up
                db.delete(result)
                db.commit()
            else:
                print("❌ Module B: Failed to retrieve sample data")
                return False
                
    except Exception as e:
        print(f"❌ Module B: Sample data test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Testing Multi-Database Setup")
    print("=" * 40)
    
    # Print current configuration
    print(f"Module A Database URL: {settings.DATABASE_URL_A}")
    print(f"Module B Database URL: {settings.DATABASE_URL_B}")
    print()
    
    # Run tests
    if not test_database_connections():
        print("\n❌ Database connection tests failed")
        sys.exit(1)
    
    if not test_table_creation():
        print("\n❌ Table creation tests failed")
        sys.exit(1)
    
    if not test_sample_data():
        print("\n❌ Sample data tests failed")
        sys.exit(1)
    
    print("\n🎉 All tests passed! Multi-database setup is working correctly.")
    print("\nYou can now start the server with:")
    print("  python start.py")
    print("  or")
    print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main() 