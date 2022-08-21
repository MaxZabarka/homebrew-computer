import pydot
import os
import inspect
import random
from AST_types import *

os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'

graph = pydot.Dot(graph_type="graph", bgcolor="white", rankdir="BT")


def render_node(node, parentId=False, edge=""):
    isLeaf = not hasattr(node, '__dict__') and not isinstance(node, list)

    id = str(random.random())
    graph.add_node(pydot.Node(id, shape="oval", label=name(
        node), color="blue" if isLeaf else "black"))
    if (parentId):
        graph.add_edge(pydot.Edge(id, str(parentId),
                       label=edge, fontsize="12"))

    if (hasattr(node, '__dict__')):
        for edge, child in vars(node).items():
            render_node(child, id, edge)
    elif isinstance(node, list):
        for child in node:
            render_node(child, id)


def name(obj):
    if (hasattr(obj, '__dict__')):
        return type(obj).__name__
    elif isinstance(obj, list):
        return "[]"
    else:
        return str(obj)


def draw_ast(ast):
    for node in ast:
        render_node(node)
    graph.write_png("./output.png")
