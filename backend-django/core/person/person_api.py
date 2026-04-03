#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 张诚成
@Contact: 939589097@qq.com
@Time: 2026-03-26
@File: person_api.py
@Desc: Person API - 人员管理接口 - 提供人员的 CRUD 操作
"""
"""
Person API - 人员管理接口
提供人员的 CRUD 操作
"""
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.errors import HttpError
from ninja.pagination import paginate

from common.fu_crud import create, retrieve, delete, update
from common.fu_pagination import MyPagination
from common.fu_schema import response_success
from core.person.person_model import Person
from core.person.person_schema import (
    PersonSchemaOut,
    PersonSchemaIn,
    PersonSchemaPatch,
    PersonFilters,
    PersonSchemaDetail,
)

router = Router()


@router.post("/person", response=PersonSchemaOut, summary="创建人员")
def create_person(request, data: PersonSchemaIn):
    """
    创建新人员
    
    参数:
    - name: 姓名
    - gender: 性别 (0: 未知, 1: 男, 2: 女)
    - phone: 电话号码
    - destination: 目的地/所属部门
    """
    return create(request, data.dict(), Person)


@router.get("/person", response=List[PersonSchemaOut], summary="获取人员列表")
@paginate(MyPagination)
def list_persons(request, filters: PersonFilters = Query()):
    """
    获取人员列表
    
    支持分页和搜索:
    - page: 页码
    - pageSize: 每页数量
    - keyword: 关键词搜索 (搜索 name, phone, destination)
    """
    return retrieve(request, Person, filters)


@router.get("/person/{id}", response=PersonSchemaDetail, summary="获取人员详情")
def get_person_detail(request, id: str):
    """
    获取单个人员信息
    
    参数:
    - id: 人员ID
    """
    return get_object_or_404(Person, id=id)


@router.put("/person/{id}", response=PersonSchemaOut, summary="更新人员(完全替换)")
def update_person(request, id: str, data: PersonSchemaIn):
    """
    更新人员信息 (PUT - 完全替换)
    
    参数:
    - id: 人员ID
    - name: 姓名
    - gender: 性别
    - phone: 电话号码
    - destination: 目的地/所属部门
    """
    return update(request, id, data, Person)


@router.patch("/person/{id}", response=PersonSchemaOut, summary="更新人员(部分更新)")
def patch_person(request, id: str, data: PersonSchemaPatch):
    """
    部分更新人员信息 (PATCH - 只更新提供的字段)
    
    参数:
    - id: 人员ID
    - name: 姓名 (可选)
    - gender: 性别 (可选)
    - phone: 电话号码 (可选)
    - destination: 目的地/所属部门 (可选)
    """
    return update(request, id, data, Person)


@router.delete("/person/{id}", summary="删除人员")
def delete_person(request, id: str):
    """
    删除指定人员
    
    参数:
    - id: 人员ID
    """
    delete(id, Person)
    return response_success()