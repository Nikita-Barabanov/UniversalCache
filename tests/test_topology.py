import pytest

from univcache.topology import get_jobs_order
from store.objects import DependencyGraph, GraphNode, GraphEdge
from univcache.parse import fields


class TestTopology:
    def test_job_order(self):
        class Homework:
            pass

        class Solution:
            pass

        test_fields = {"user": "{hw.user}", "task": "{hw.task}"}

        @fields(**test_fields)
        def get_solution(hw: Homework) -> Solution:
            ...

        test_graph = DependencyGraph()
        test_graph.add_func(fields.funcs_info["get_solution"])
        assert (get_jobs_order(Solution, test_graph) ==
                [test_graph.type_to_node[Homework], test_graph.type_to_node[Solution]])
