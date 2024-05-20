import pytest

from univcache.store.objects import DependencyGraph, GraphNode, GraphEdge
from univcache.parse import fields
import networkx as nx


class TestObjectsGraph:
    def test_add_func(self):
        class Homework:
            pass

        class Solution:
            pass

        test_fields = {"user": "{hw.user}", "task": "{hw.task}"}

        @fields(**test_fields)
        def get_solution(hw: Homework) -> Solution:
            ...

        graph = DependencyGraph()
        graph.add_func(fields.funcs_info["get_solution"])
        expected_graph = DependencyGraph(
            [
                (GraphNode('hw', Homework, {}),
                 GraphNode('None', Solution, {'user': '{hw.user}', 'task': '{hw.task}'}),
                 {"object": GraphEdge(fields.funcs_info["get_solution"])})
            ]
        )
        print(expected_graph)
        # TODO: find correct graph constructor
        # assert graph == expected_graph
