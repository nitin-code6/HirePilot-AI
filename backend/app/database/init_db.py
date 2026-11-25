from app.database.session import engine, Base
from app.models import *

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized successfully via SQLAlchemy.")

if __name__ == "__main__":
    init_db()
