#!/usr/bin/env python3

"""Object model for dependency graph"""

import hashlib
from collections import namedtuple
from dataclasses import dataclass, astuple
from inspect import Signature
from typing import Callable

import networkx as nx

from univcache.log import get_logger


@dataclass
class FuncInfo:
    """Primary function info"""
    name: str
    func: Callable
    signature: Signature
    fields: dict[str, str]


@dataclass
class ObjInfo:
    """Primary object info"""
    name: str
    obj_type: type
    fields: dict[str, str]


class GraphNode:
    """Dependency graph node representation"""
    def __init__(self, name: str, obj_type: type, fields: dict):
        """

        :param name:
        :param obj_type:
        :param fields:
        """
        self.name = name
        self.fields = fields
        self.obj_type = obj_type

    # Хеш должен зависеть только от типа объекта, потому что fields и name зависят от правила, т.е. от грани
    def __hash__(self):
        """

        :return:
        """
        return int(hashlib.sha256(str(self.obj_type).encode()).hexdigest(), 16)

    def __repr__(self):
        """

        :return:
        """
        return f"GraphNode('{self.name}', {self.obj_type}, {self.fields})"


class GraphEdge:
    """Dependency graph edge representation"""
    def __init__(self, info: FuncInfo):
        """

        :param info:
        """
        self.info = info

    def __repr__(self):
        """

        :return:
        """
        return f"GraphEdge({self.info})"


class Versioned:
    def __init__(self, target_class, version):
        self.target_class = target_class
        self.version = version

    @classmethod
    def __class_getitem__(cls, item: tuple[type, int]):
        if isinstance(item, tuple) and len(item) == 2:
            target_class, version = item
            if isinstance(version, int) or isinstance(version, Ellipsis):
                return Versioned(target_class, version)
            else:
                raise TypeError("Version can be integer or ... only")
        else:
            raise TypeError("Expected two elements: class, version")


class DependencyGraph:
    """Dependency graph representation"""
    def __init__(self, init_graph=None):
        """

        """
        self.graph = nx.DiGraph() if init_graph is None else nx.DiGraph(init_graph)
        self.type_to_node = {}

    def add_node(self, node_info: ObjInfo) -> GraphNode:
        """Add node to graph or update if present

        :param node_info:
        :return:
        """
        if node_info.obj_type in self.type_to_node:
            node = self.type_to_node[node_info.obj_type]
            node.name_to_fields[node_info.name].update(node_info.fields)
        else:
            node = GraphNode(*astuple(node_info))
            self.graph.add_node(node)
            self.type_to_node[node_info.obj_type] = node

        return node

    def add_edge(self, first_node_info: ObjInfo, second_node_info: ObjInfo, edge_info: FuncInfo) -> None:
        """Add edge to graph

        :param first_node_info:
        :param second_node_info:
        :param edge_info:
        :return:
        """
        first_node = self.add_node(first_node_info)
        second_node = self.add_node(second_node_info)
        self.graph.add_edge(first_node,
                            second_node,
                            object=GraphEdge(edge_info))

    def add_func(self, func_info: FuncInfo) -> None:
        """

        :param func_info:
        :return:
        """

        for name, param in func_info.signature.parameters.items():
            pre = f"{name}."
            first_node = name, param.annotation, {field.removeprefix(pre): None
                                                  for field in func_info.fields.values()
                                                  if field.startswith(pre)}
            second_node = None, func_info.signature.return_annotation, func_info.fields

            self.add_edge(ObjInfo(*first_node), ObjInfo(*second_node), func_info)

    def __repr__(self):
        """

        :return:
        """
        return f"DependencyGraph({self.graph.edges})"

