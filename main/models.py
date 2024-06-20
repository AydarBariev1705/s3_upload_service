from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
import asyncio

from main.database import Base, engine


class ImageORM(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    filename: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    project_id: Mapped[str] = mapped_column(
        Integer, nullable=False,
    )
    celery_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(async_main())
