from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:1234@localhost:5432/hacker_db', echo=True)

# Test connection
with engine.connect() as conn:
    result = conn.execute("SELECT 1")
    print(result.fetchone())