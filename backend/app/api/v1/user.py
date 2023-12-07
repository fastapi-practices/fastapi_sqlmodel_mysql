#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.app.common.jwt import CurrentUser, DependsJwtUser
from backend.app.common.pagination import PageDepends, paging_data
from backend.app.common.response.response_schema import response_base
from backend.app.database.db_mysql import async_engine
from backend.app.schemas.user import Avatar, CreateUser, GetUserInfo, ResetPassword, UpdateUser
from backend.app.services.user_service import UserService

router = APIRouter()


@router.post('/register', summary='用户注册')
async def user_register(obj: CreateUser):
    await UserService.register(obj=obj)
    return await response_base.success()


@router.post('/password/reset', summary='密码重置', dependencies=[DependsJwtUser])
async def password_reset(obj: ResetPassword):
    await UserService.pwd_reset(obj=obj)
    return await response_base.success()


@router.get('/{username}', summary='查看用户信息', dependencies=[DependsJwtUser])
async def get_user(username: str):
    data = await UserService.get_userinfo(username=username)
    return await response_base.success(data=data)


@router.put('/{username}', summary='更新用户信息', dependencies=[DependsJwtUser])
async def update_userinfo(username: str, obj: UpdateUser):
    await UserService.update(username=username, obj=obj)
    return await response_base.success()


@router.put('/{username}/avatar', summary='更新头像', dependencies=[DependsJwtUser])
async def update_avatar(username: str, avatar: Avatar):
    await UserService.update_avatar(username=username, avatar=avatar)
    return await response_base.success()


@router.get('', summary='（模糊条件）分页获取所有用户', dependencies=[DependsJwtUser, PageDepends])
async def get_all_users(
    username: Annotated[str | None, Query()] = None,
    phone: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
):
    async with AsyncSession(async_engine) as db:
        user_select = await UserService.get_select(username=username, phone=phone, status=status)
        page_data = await paging_data(db, user_select, GetUserInfo)
    return await response_base.success(data=page_data)


@router.put('/{pk}/super', summary='修改用户超级权限', dependencies=[DependsJwtUser])
async def super_set(current_user: CurrentUser, pk: int):
    await UserService.update_permission(current_user=current_user, pk=pk)
    return await response_base.success()


@router.put('/{pk}/status', summary='修改用户状态', dependencies=[DependsJwtUser])
async def status_set(current_user: CurrentUser, pk: int):
    await UserService.update_status(current_user=current_user, pk=pk)
    return await response_base.success()


@router.delete(
    path='/{username}',
    summary='用户注销',
    description='用户注销 != 用户登出，注销之后用户将从数据库删除',
    dependencies=[DependsJwtUser],
)
async def delete_user(current_user: CurrentUser, username: str):
    await UserService.delete(current_user=current_user, username=username)
    return await response_base.success()
