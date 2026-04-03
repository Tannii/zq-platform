#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 张诚成
@Contact: 941177402@qq.com
@Time: 2026-04-03
@File: dict_schema.py
@Desc: Dictionary Schema - 字典数据验证模式
"""

from typing import Optional

from ninja import ModelSchema, Field

from common.fu_model import exclude_fields
from common.fu_schema import FuFilters
from core.dict.dict_model import Dict


class DictFilters(FuFilters):
    name: Optional[str] = Field(None, q="name__contains", alias="name")
    code: Optional[str] = Field(None, q="code__contains", alias="code")
    status: Optional[bool] = Field(None, alias="status")


class DictSchemaIn(ModelSchema):
    class Config:
        model = Dict
        model_exclude = exclude_fields


class DictSchemaOut(ModelSchema):
    class Config:
        model = Dict
        model_fields = "__all__"
