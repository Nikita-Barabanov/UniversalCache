from inspect import signature
import pytest

from univcache.parse import fields, FuncInfo


class TestsParseFields:
    def test_parsing(self):
        class Homework:
            pass

        class Solution:
            pass

        test_fields = {"user": "{hw.user}", "task": "{hw.task}"}

        @fields(**test_fields)
        def get_solution(hw: Homework) -> Solution:
            ...

        name = get_solution.__name__
        assert fields.funcs_info == {name: FuncInfo(name, get_solution, signature(get_solution), test_fields)}

