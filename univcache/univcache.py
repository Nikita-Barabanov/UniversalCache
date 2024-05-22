"""User Interface"""

from store.objects import DependencyGraph
from univcache.topology import get_jobs_order
import networkx as nx

from univcache.log import get_logger

from store.objects import stored_results
from univcache.parse import fields
from univcache.make import build_target
from univcache.clean import clean_target

working_graph = DependencyGraph()


def build(result_type: type):
    for func_name, func_info in fields.funcs_info.items():
        working_graph.add_func(func_info)

    return build_target(result_type, working_graph)


def clean(result_type: type):
    for func_name, func_info in fields.funcs_info.items():
        working_graph.add_func(func_info)

    clean_target(result_type, working_graph)
