#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 张诚成
@Contact: 939589097@qq.com
@Time: 2026-03-26
@File: person_model.py
@Desc: Person Model - 人员模型 - 用于管理系统人员信息
"""
"""
Person Model - 人员模型
用于管理系统人员信息
"""
from django.db import models

from common.fu_model import RootModel


class Person(RootModel):
    """
    人员模型 - 系统人员信息管理

    字段说明：
    - name: 姓名
    - gender: 性别 (0: 未知, 1: 男, 2: 女)
    - phone: 电话号码
    - destination: 目的地/所属部门
    """

    # 性别选择
    GENDER_CHOICES = [
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    ]

    # 姓名
    name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text="姓名",
        db_index=True,
    )

    # 性别
    gender = models.IntegerField(
        choices=GENDER_CHOICES,
        default=0,
        help_text="性别",
    )

    # 电话号码
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="电话号码",
        db_index=True,
    )

    # 目的地/所属部门
    destination = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="目的地/所属部门",
    )

    class Meta:
        db_table = "core_person"
        verbose_name = "人员"
        verbose_name_plural = "人员"
        ordering = ("-sys_create_datetime",)

    def __str__(self):
        return self.name or str(self.id)