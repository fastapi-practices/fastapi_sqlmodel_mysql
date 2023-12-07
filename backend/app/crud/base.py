#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Dict, Generic, Type, TypeVar

from pydantic import BaseModel
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar('ModelType', bound=SQLModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, *, pk: int | None = None) -> ModelType | None:
        """
        通过主键 id 获取一条数据

        :param db:
        :param pk:
        :return:
        """
        model = await db.exec(select(self.model).where(self.model.id == pk))
        return model.first()

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType, user_id: int | None = None) -> None:
        """
        新增一条数据

        :param db:
        :param obj_in: Pydantic 模型类
        :param user_id:
        :return:
        """
        if user_id:
            create_data = self.model(**obj_in.model_dump(), create_user=user_id)
        else:
            create_data = self.model(**obj_in.model_dump())
        db.add(create_data)
        await db.commit()

    async def update(
        self, db: AsyncSession, pk: int, obj_in: UpdateSchemaType | Dict[str, Any], user_id: int | None = None
    ) -> None:
        """
        通过主键 id 更新一条数据

        :param db:
        :param pk:
        :param obj_in: Pydantic模型类 or 对应数据库字段的字典
        :param user_id:
        :return:
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if user_id:
            update_data.update({'update_user': user_id})
        result = await db.exec(select(self.model).where(self.model.id == pk))
        model = result.one()
        for key, value in update_data.items():
            setattr(model, key, value)
        await db.commit()
        await db.refresh(model)

    async def delete(self, db: AsyncSession, pk: int) -> None:
        """
        通过主键 id 删除一条数据

        :param db:
        :param pk:
        :return:
        """

        result = await db.exec(select(self.model).where(self.model.id == pk))
        model = result.one()
        await db.delete(model)
        await db.commit()
