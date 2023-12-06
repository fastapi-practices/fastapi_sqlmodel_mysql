#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlmodel import Field, SQLModel

from backend.app.models.base import id_key
from backend.app.utils.generate_string import get_uuid4_str
from backend.app.utils.timezone import timezone


class User(SQLModel, table=True):
    """用户表"""

    id: int = id_key
    uuid: str = Field(max_length=50, exclude=True, default_factory=get_uuid4_str, unique=True)
    username: str = Field(max_length=20, unique=True, index=True, description='用户名')
    password: str = Field(max_length=255, description='密码')
    email: str = Field(max_length=50, unique=True, index=True, description='邮箱')
    status: int = Field(default=1, description='用户账号状态(0停用 1正常)')
    is_superuser: bool = Field(default=False, description='超级权限(0否 1是)')
    avatar: str | None = Field(max_length=255, default=None, description='头像')
    phone: str | None = Field(max_length=11, default=None, description='手机号')
    join_time: datetime = Field(exclude=True, default_factory=timezone.now, description='注册时间')
    last_login_time: datetime | None = Field(
        exclude=True, sa_column_kwargs={'onupdate': timezone.now}, description='上次登录'
    )
