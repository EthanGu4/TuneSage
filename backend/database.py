import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tunesage.db")

# SQLite needs connect_args
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()


# import os
# from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, JSON, select
# from sqlalchemy.exc import SQLAlchemyError


# DATABASE_URL = os.getenv("DATABASE_URL")


# engine = None
# metadata = MetaData()


# tracks_table = Table(
# "tracks",
# metadata,
# Column("id", String, primary_key=True),
# Column("payload", JSON),
# )




# def init_db():
#     global engine
#     if not DATABASE_URL:
#         return None
#     engine = create_engine(DATABASE_URL)
#     metadata.create_all(engine)
#     return engine


# def cache_tracks(track_dicts):
#     if engine is None:
#         return
#     conn = engine.connect()
#     try:
#         for t in track_dicts:
#             stmt = tracks_table.insert().prefix_with("OR REPLACE").values(id=t['id'], payload=t)
#             conn.execute(stmt)
#         conn.commit()
#     except SQLAlchemyError:
#         pass
#     finally:
#         conn.close()


# def get_cached_track(track_id):
#     if engine is None:
#         return None
#     conn = engine.connect()
#     try:
#         stmt = select([tracks_table.c.payload]).where(tracks_table.c.id == track_id)
#         r = conn.execute(stmt).fetchone()
#         if r:
#             return r[0]
#     except SQLAlchemyError:
#         return None
#     finally:
#         conn.close()