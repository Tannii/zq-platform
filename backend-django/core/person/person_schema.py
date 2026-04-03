#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 张诚成
@Contact: 939589097@qq.com
@Time: 2026-03-26
@File: person_schema.py
@Desc: Person Schema - 人员数据验证模式
"""
"""
Person Schema - 人员数据验证模式
"""
from typing import Optional

from ninja import ModelSchema, Field, Schema
from pydantic import field_validator

from common.fu_schema import FuFilters
from core.person.person_model import Person


class PersonFilters(FuFilters):
    """人员过滤器"""
    name: Optional[str] = Field(None, q="name__icontains", alias="name")
    gender: Optional[int] = Field(None, q="gender", alias="gender")
    phone: Optional[str] = Field(None, q="phone__icontains", alias="phone")
    destination: Optional[str] = Field(None, q="destination__icontains", alias="destination")
    id: Optional[str] = Field(None, q="id", alias="id")


class PersonSchemaIn(ModelSchema):
    """人员输入模式"""

    @field_validator('name', check_fields=False)
    @classmethod
    def validate_name(cls, v):
        """验证姓名"""
        if len(v) > 64:
            raise ValueError('姓名长度不能超过64个字符')
        return v

    @field_validator('gender', check_fields=False)
    @classmethod
    def validate_gender(cls, v):
        """验证性别"""
        if v not in [0, 1, 2]:
            raise ValueError('性别必须为 0(未知)、1(男) 或 2(女)')
        return v

    @field_validator('phone', check_fields=False)
    @classmethod
    def validate_phone(cls, v):
        """验证电话号码"""
        if v and len(v) > 20:
            raise ValueError('电话号码长度不能超过20个字符')
        return v

    @field_validator('destination', check_fields=False)
    @classmethod
    def validate_destination(cls, v):
        """验证目的地"""
        if v and len(v) > 255:
            raise ValueError('目的地长度不能超过255个字符')
        return v

    class Config:
        model = Person
        model_exclude = ("id", "sys_creator", "sys_create_datetime", "sys_modifier", "sys_update_datetime")


class PersonSchemaPatch(ModelSchema):
    """人员更新模式"""
    name: Optional[str] = None
    gender: Optional[int] = None
    phone: Optional[str] = None
    destination: Optional[str] = None

    @field_validator('name', check_fields=False)
    @classmethod
    def validate_name(cls, v):
        """验证姓名"""
        if v and len(v) > 64:
            raise ValueError('姓名长度不能超过64个字符')
        return v

    @field_validator('gender', check_fields=False)
    @classmethod
    def validate_gender(cls, v):
        """验证性别"""
        if v is not None and v not in [0, 1, 2]:
            raise ValueError('性别必须为 0(未知)、1(男) 或 2(女)')
        return v

    @field_validator('phone', check_fields=False)
    @classmethod
    def validate_phone(cls, v):
        """验证电话号码"""
        if v and len(v) > 20:
            raise ValueError('电话号码长度不能超过20个字符')
        return v

    @field_validator('destination', check_fields=False)
    @classmethod
    def validate_destination(cls, v):
        """验证目的地"""
        if v and len(v) > 255:
            raise ValueError('目的地长度不能超过255个字符')
        return v

    class Config:
        model = Person
        model_exclude = ("id", "sys_creator", "sys_create_datetime", "sys_modifier", "sys_update_datetime")


class PersonSchemaOut(ModelSchema):
    """人员输出模式"""
    gender_display: Optional[str] = None

    class Config:
        model = Person
        model_fields = "__all__"

    @staticmethod
    def resolve_gender_display(obj):
        """解析性别显示名称"""
        return obj.get_gender_display()


class PersonSchemaDetail(PersonSchemaOut):
    """人员详情输出模式"""
    pass