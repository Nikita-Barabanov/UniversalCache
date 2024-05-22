from store.objects import DependencyGraph, GraphNode
from univcache.topology import get_jobs_order
import networkx as nx

from univcache.log import get_logger

from store.objects import stored_results


def clean_target(result_type: type, graph: DependencyGraph):
    for result in stored_results.copy():
        if result == result_type:
            del stored_results[result]
