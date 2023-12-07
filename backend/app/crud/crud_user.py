#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.sql import Select
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.app.common import jwt
from backend.app.crud.base import CRUDBase
from backend.app.models.user import User
from backend.app.schemas.user import Avatar, CreateUser, UpdateUser


class CRUDUser(CRUDBase[User, CreateUser, UpdateUser]):
    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        user = await super().get(db, pk=user_id)
        return user

    async def get_user_by_username(self, db: AsyncSession, username: str) -> User | None:
        user = await db.exec(select(self.model).where(self.model.username == username))
        return user.first()

    async def update_user_login_time(self, db: AsyncSession, username: str, login_time: datetime) -> None:
        result = await db.exec(select(self.model).where(self.model.username == username))
        user = result.one()
        user.last_login_time = login_time

    @staticmethod
    async def create_user(db: AsyncSession, create: CreateUser) -> None:
        create.password = await jwt.get_hash_password(create.password)
        new_user = User(**create.model_dump())
        db.add(new_user)
        await db.commit()

    async def update_userinfo(self, db: AsyncSession, current_user: User, obj: UpdateUser) -> None:
        await super().update(db, current_user.id, obj)

    async def update_avatar(self, db: AsyncSession, current_user: User, avatar: Avatar) -> None:
        await super().update(db, current_user.id, {'avatar': avatar.url})

    async def delete_user(self, db: AsyncSession, user_id: int) -> None:
        await super().delete(db, user_id)

    async def check_email(self, db: AsyncSession, email: str) -> User:
        user = await db.exec(select(self.model).where(self.model.email == email))
        return user.first()

    async def reset_password(self, db: AsyncSession, username: str, password: str) -> None:
        new_password = jwt.get_hash_password(password)
        result = await db.exec(select(self.model).where((self.model.username == username)))
        user = result.one()
        user.password = new_password
        db.add(user)
        await db.commit()

    async def get_all(self, username: str = None, phone: str = None, status: int = None) -> Select:
        se = select(self.model).order_by(desc(self.model.join_time))
        where_list = []
        if username:
            where_list.append(self.model.username.like(f'%{username}%'))  # type: ignore
        if phone:
            where_list.append(self.model.phone.like(f'%{phone}%'))  # type: ignore
        if status is not None:
            where_list.append(self.model.status == status)
        if where_list:
            se = se.where(and_(*where_list))
        return se

    async def get_user_super(self, db: AsyncSession, user_id: int) -> bool:
        user = await self.get_user_by_id(db, user_id)
        return user.is_superuser

    async def get_user_status(self, db: AsyncSession, user_id: int) -> bool:
        user = await self.get_user_by_id(db, user_id)
        return user.is_active

    async def super_set(self, db: AsyncSession, user_id: int) -> None:
        super_status = await self.get_user_super(db, user_id)
        await super().update(db, user_id, {'is_superuser': False if super_status else True})

    async def status_set(self, db: AsyncSession, user_id: int) -> None:
        status = await self.get_user_status(db, user_id)
        await super().update(db, user_id, {'status': False if status else True})


UserDao: CRUDUser = CRUDUser(User)
