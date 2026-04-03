#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 张诚成
@Contact: 941177402@qq.com
@Time: 2026-04-03
@File: fu_auth.py
@Desc: 分页工具
"""
from typing import Any, List

from ninja import Field, Schema
from ninja.pagination import PaginationBase
from ninja.types import DictStrAny


class MyPagination(PaginationBase):
    class Input(Schema):
        pageSize: int = Field(10, gt=0)
        page: int = Field(1, gt=-1)

    class Output(Schema):
        items: List[Any]
        total: int

    def paginate_queryset(
            self,
            queryset,
            pagination: Input,
            **params: DictStrAny,
    ) -> Any:
        offset = pagination.pageSize * (pagination.page - 1)
        limit: int = pagination.pageSize
        return {
            "page": offset,
            "limit": limit,
            "items": queryset[offset: offset + limit],
            "total": self._items_count(queryset),
        }  # noqa: E203
