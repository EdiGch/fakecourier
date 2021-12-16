from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.conf import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI.replace("postgresql://", "postgresql+asyncpg://")
)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

engineSync = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocalSync = sessionmaker(autocommit=False, autoflush=False, bind=engineSync)
