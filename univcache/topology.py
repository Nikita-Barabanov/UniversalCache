"""Topological sorting and graph validation"""

from store.objects import DependencyGraph, GraphNode
import networkx as nx

from univcache.log import get_logger


def get_jobs_order(result_type: type, graph: DependencyGraph) -> list[GraphNode]:
    graph_node = graph.type_to_node.get(result_type, None)
    if graph_node is None:
        get_logger(__name__).info(f"There is no such {result_type} type in dependency graph")
        return []
    jobs = graph.graph
    ancestors = nx.ancestors(jobs, graph_node)
    ancestors_subgraph = jobs.subgraph(ancestors)
    ancestors_topological_order = list(nx.topological_sort(ancestors_subgraph))
    ancestors_topological_order.append(graph_node)
    return ancestors_topological_order
