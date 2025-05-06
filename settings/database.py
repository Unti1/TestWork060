from datetime import datetime
from typing import Annotated, Generator, List, Self

from sqlalchemy import BigInteger, String, func, select
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from settings.config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# connection decorator
def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    create_at: Mapped[datetime] = mapped_column(default=func.now())
    update_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

    @classmethod
    @connection
    async def get(cls, session: AsyncSession = None, **creterias) -> None | Self:
        """Возвращает искомый объет базы данных по переданным creterias

        Args:
            session (Session, optional): Сессия запроса(подставляется автоматически). Defaults to None.
        Returns:
            None|Self: Объект или None
        """
        query = select(cls).filter_by(**creterias)
        rows = await session.execute(query)
        return rows.scalar_one_or_none()

    @classmethod
    @connection
    async def get_all_by_creterias(
        cls, session: AsyncSession = None, **creterias
    ) -> list[Self]:
        """Возвращает искомые объеты базы данных по переданным creterias

        Args:
            session (Session, optional): Сессия запроса(подставляется автоматически). Defaults to None.

        Returns:
            list[Self]: Список найденных объектов
        """
        query = select(cls).filter_by(**creterias)
        rows = await session.execute(query)
        return rows.scalars().all()

    @classmethod
    @connection
    async def get_all(cls, session: AsyncSession = None) -> list[Self]:
        """Выводит все строки таблицы

        Args:
            session (Session, optional): Сессия запроса(подставляется автоматически). Defaults to None.

        Returns:
            list[Self]: _description_
        """
        query = select(cls)
        rows = await session.execute(query)
        return rows.scalars().all()

    @classmethod
    @connection
    async def create(
        cls,
        session: AsyncSession = None,
        **data,
    ) -> int:
        """Создание новой строки в БД, по переданным data

        Args:
            session (Session, optional): Сессия запроса(подставляется автоматически). Defaults to None.

        Returns:
            Self
        """
        new_row = cls(**data)
        session.add(new_row)
        await session.commit()
        return new_row.id

    @classmethod
    @connection
    async def create_many(
        cls,
        datas: list[dict],
        session: AsyncSession = None,
    ) -> Generator[int]:
        """Создает несколько объектов за раз

        Args:
            datas (list[dict]): Список данных для каждой строки БД
            session (Session, optional): Сессия запроса(подставляется автоматически). Defaults to None.

        Returns:
            list[Self]
        """
        new_rows = [cls(**data) for data in datas]
        session.add_all(new_rows)
        await session.commit()
        return (new_row.id for new_row in new_rows)

    @classmethod
    @connection
    async def update(cls, id: int, session: AsyncSession = None, **data) -> Self:
        """Обновление данных для одного объекта

        Args:
            id (int): Идентификатор объекта
            session (Session, optional): Сессия запроса(подставляется автоматически). Defaults to None.

        Raises:
            ValueError: если нет колонки или строки с переданным id

        Returns:
            Self
        """
        query = select(cls).where(cls.id == id).with_for_update()
        rows = await session.execute(query)
        concrete_row = rows.scalar_one_or_none()

        if not concrete_row:
            raise ValueError(
                f"Данные с таким id в таблице {cls.__tablename__} не найдены"
            )

        for key, value in data.items():
            if key not in concrete_row.__dict__:
                raise ValueError(f'Колонки "{key}" нету в таблице {cls.__tablename__}')
            if getattr(concrete_row, key) != value:
                setattr(concrete_row, key, value)

        await session.commit()
        return concrete_row

    @classmethod
    @connection
    async def delete(
        cls,
        id: int,
        session: AsyncSession = None,
    ) -> bool:
        """Удаление строки данных

        Args:
            id (int): Идентификатор объекта(по полю id)
            session (Session, optional): Сессия запроса(подставляется автоматически). Defaults to None.

        Returns:
            bool
        """
        query = select(cls).where(cls.id == id)
        rows = await session.execute(query)
        row = rows.unique().scalar_one_or_none()
        if row:
            await session.delete(row)
            await session.commit()
            return True
        return False


# Annotated types
array_or_none_an = Annotated[List[str] | None, mapped_column(ARRAY(String))]
