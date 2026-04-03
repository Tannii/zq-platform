#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 张诚成
@Contact: 941177402@qq.com
@Time: 2026-04-03
@File: apps.py
@Desc: Core Apps - Django 应用配置
"""
"""
Core Apps - Django 应用配置
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Core 应用配置"""
    name = 'core'
    verbose_name = '核心权限管理'

    def ready(self):
        """应用初始化时执行"""
        # 导入信号处理器（如果有）
        # import core.signals
        pass
