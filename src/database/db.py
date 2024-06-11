import contextlib
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from src.conf.config import config  # Импортируем наш конфиг

class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)  # Создаем асинхронный движок SQLAlchemy
        self._session_maker: async_sessionmaker = async_sessionmaker(autoflush=False, autocommit=False,
                                                                     bind=self._engine)  # Создаем фабрику сессий

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Session is not initialized")  # Выбрасываем исключение, если сессия не инициализирована
        session = self._session_maker()  # Создаем асинхронную сессию
        try:
            yield session  # Передаем сессию в контекст управления
        except Exception as err:
            print(err)  # Выводим ошибку
            await session.rollback()  # Откатываем транзакцию при ошибке
        finally:
            await session.close()  # Закрываем сессию

# Создаем менеджер сессий для нашей базы данных с использованием конфигурационного URL
sessionmanager = DatabaseSessionManager(config.DB_URL)

# Функция для получения асинхронной сессии базы данных
async def get_db():
    async with sessionmanager.session() as session:
        yield session  # Возвращаем сессию базы данных
