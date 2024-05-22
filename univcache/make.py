"""Main functionality"""


from store.objects import DependencyGraph, GraphNode
from univcache.topology import get_jobs_order
import networkx as nx

from univcache.log import get_logger

from store.objects import stored_results


def build_target(result_type: type, graph: DependencyGraph) -> list:
    jobs = get_jobs_order(result_type, graph)
    pre_job = jobs[0]
    for job in jobs[1:]:
        if graph.graph.has_edge(pre_job, job):
            edge_info = graph.graph.get_edge_data(pre_job, job)
            try:
                stored_results[pre_job.obj_type] = edge_info.info.func(stored_results[job.obj_type])
            except Exception:
                get_logger(__name__).warn(f"Incorrect {edge_info.info.name} rule processing")
        pre_job = job

    return stored_results[result_type]