#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 张诚成
@Contact: 941177402@qq.com
@Time: 2026-04-03
@File: fu_auth.py
@Desc: 模式工具
"""

from ninja import Schema, FilterSchema, Field


class FuFilters(FilterSchema):
    creator_id: str = Field(None, alias="creator_id")
    curr_flag: bool = Field(None, alias="curr_flag")


class UserSchema(Schema):
    id: str = None
    name: str = None


def response_success(data='success'):
    return {"detail": data}
