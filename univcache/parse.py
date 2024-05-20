#!/usr/bin/env python3

"""Parses user build rules to dependency graph"""


from typing import Callable, Dict, Any
from inspect import get_annotations, signature, Signature

from store.objects import FuncInfo, DependencyGraph


class fields:
    """Decorator for function info parsing"""
    funcs_info: dict[str, FuncInfo] = {}

    def __init__(self, **func_fields: str):
        """Save function fields to object attribute

        :param func_fields:
        """
        self.func_fields = func_fields

    def __call__(self, func: callable) -> callable:
        """Save all function info to class dictionary funcs_info

        :param func:
        :return:
        """
        name = func.__name__
        info = FuncInfo(name, func, fields.parse_annotations(func), self.func_fields)
        fields.funcs_info[name] = info
        return func

    @staticmethod
    def parse_annotations(func: Callable) -> Signature:
        """Convert function to signature

        :param func:
        :return:
        """
        if callable(func):
            return signature(func)
        return Signature()

    @classmethod
    def is_origin(cls, func_info: str | Signature):
        """Check if function rule is origin

        :param func_info:
        :return:
        """
        if isinstance(func_info, Signature):
            return not func_info.parameters
        elif isinstance(func_info, str):
            if func_info in fields.funcs_info:
                return not cls.funcs_info[func_info].signature.parameters
            else:
                return None
        return None
