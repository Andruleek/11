from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import contextlib
from src.conf.config import create_async_engine, async_sessionmaker, SQLALCHEMY_DATABASE_URL

# Create a synchronous SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a synchronous session maker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Declare a base class for SQLAlchemy models
Base = declarative_base()

# Create an asynchronous session manager
class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False,
            autocommit=False,
            bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Session not initialized")

        async with self._session_maker() as session:
            try:
                yield session
            except Exception as err:
                print(err)
                await session.rollback()
            finally:
                await session.close()

# Create a session manager for our database using the configuration URL
sessionmanager = DatabaseSessionManager(SQLALCHEMY_DATABASE_URL)

# Function to get an asynchronous database session
async def get_db():
    async with sessionmanager.session() as session:
        yield session