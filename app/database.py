from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import setting
# from psycopg2.extras import RealDictCursor;
# import psycopg2;


SQL_ALCHEMY_DATABASE = f'postgresql://{setting.DATABASE_USERNAME}:{setting.DATABASE_PASSWORD}@{setting.DATABASE_HOSTNAME}:{setting.DATABASE_PORT}/{setting.DATABASE_NAME}';


# try:
#     conn = psycopg2.connect(host='localhost', database='SMP Apis Database', user='postgres', password='03412959275', cursor_factory=RealDictCursor);
#     cursor = conn.cursor();
#     print("DB connection successful Alhumdulilah")
# except Exception as error:
#     raise Exception("Error connecting:", error);


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


engine = create_engine(SQL_ALCHEMY_DATABASE);

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine);

Base = declarative_base();