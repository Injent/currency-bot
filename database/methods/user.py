from sqlalchemy import insert

from config_data.config import config
from database.database import session_factory
from database.models import User


async def register_user(user_id: int):
    async with session_factory() as s:
        if await s.get(User, user_id):
            return
        q = insert(User).values(
            {
                'user_id': user_id,
                'base_currency': 'RUB'
            }
        )
        await s.execute(q)
        await s.commit()


async def change_user_base_currency(user_id: int, base: str):
    # Проверяем валидна ли введенная валюта, если нет, то игнорируем выполение операции
    if base not in config.currencies:
        return
    async with session_factory() as s:
        user = await s.get(User, user_id)

        if user:
            user.base_currency = base
            await s.commit()
        else:
            raise Exception(f'Не существует пользователя с id = {user_id}')


async def get_user_base_currency(user_id: int) -> str:
    async with session_factory() as s:
        user = await s.get(User, user_id)
        return user.base_currency