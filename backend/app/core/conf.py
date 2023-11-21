#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    # DateTime
    DATETIME_TIMEZONE: str = 'Asia/Shanghai'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
