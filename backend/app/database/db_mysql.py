#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from backend.app.core.conf import settings

SQLALCHEMY_DATABASE_URL = (
    f'mysql+asyncmy://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:'
    f'{settings.DB_PORT}/{settings.DB_DATABASE}?charset={settings.DB_CHARSET}'
)

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=settings.DB_ECHO, future=True, pool_pre_ping=True)


async def create_table():
    """创建数据库表"""
    async with async_engine.begin() as coon:
        await coon.run_sync(SQLModel.metadata.create_all)
