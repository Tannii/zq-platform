#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 张诚成
@Contact: 941177402@qq.com
@Time: 2026-04-03
@File: manage.py
@Desc: Django's command-line utility for administrative tasks. - import os
"""
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
