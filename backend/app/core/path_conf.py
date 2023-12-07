#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from pathlib import Path

# 获取项目根目录
# 或使用绝对路径，指到 backend 目录为止，例如 windows：BasePath = D:\git_project\fastapi_mysql\backend
BasePath = Path(__file__).resolve().parent.parent.parent

# 日志文件路径
LogPath = os.path.join(BasePath, 'app', 'log')
