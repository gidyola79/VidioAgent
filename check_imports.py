import sys

def check_imports():
    required_modules = [
        "fastapi", "uvicorn", "pydantic", "sqlalchemy", "alembic",
        "celery", "redis", "langchain", "langchain_groq", "moviepy", "PIL"
    ]
    missing = []
    print("Checking core dependencies...")
    for module in required_modules:
        try:
            __import__(module)
            print(f"[OK] {module} found")
        except ImportError:
            missing.append(module)
            print(f"[MISSING] {module} NOT found")
    
    if missing:
        print(f"\nMissing {len(missing)} libraries. Please run: pip install -r requirements.txt")
        sys.exit(1)
    else:
        print("\nAll core libraries installed successfully!")

if __name__ == "__main__":
    check_imports()
