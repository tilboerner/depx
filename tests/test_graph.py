from depx.graph import (
    create_graph_from, to_html, to_graphml, to_dotfile, to_json
)
import networkx as nx
import io
import os
import pytest


@pytest.fixture
def dependencies():
    return [
        {
            "from_module": "opportunity.models",
            "to_module": "common.utils",
            "category": "local"
        },
        {
            "from_module": "opportunity.models",
            "to_module": "common.utils",
            "category": "local"
        },
        {
            "from_module": "sales_appoinment.views",
            "to_module": "common.utils",
            "category": "local"
        },
        {
            "from_module": "common.utils",
            "to_module": "opportunity.views",
            "category": "local"
        }
    ]


def test_create_graph(dependencies):
    G = create_graph_from(dependencies)

    expected_nodes = [
        'opportunity.models',
        'common.utils',
        'sales_appoinment.views',
        'opportunity.views',
    ]
    expected_edges = [
        ('opportunity.models', 'common.utils', {'weight': 2}),
        ('common.utils', 'opportunity.views', {'weight': 1}),
        ('sales_appoinment.views', 'common.utils', {'weight': 1})
    ]
    for node in G.nodes():
        assert node in expected_nodes
        expected_nodes.remove(node)

    assert expected_nodes == []

    for edge in G.edges(data=True):
        assert edge in expected_edges
        expected_edges.remove(edge)

    assert expected_edges == []


def test_format_to_html(dependencies):
    graph = create_graph_from(dependencies)

    content = to_html(graph=graph, path=os.getcwd())

    assert '<!DOCTYPE html>' in content


def test_format_to_graphml(dependencies):
    graph = create_graph_from(dependencies)
    content = to_graphml(graph=graph, path=os.getcwd())

    exported_graph = nx.read_graphml(io.StringIO(content))

    assert exported_graph.nodes() == graph.nodes()
    assert exported_graph.edges() == graph.edges()


def test_format_to_dotfile(dependencies):
    graph = create_graph_from(dependencies)
    content = to_dotfile(graph=graph, path=os.getcwd())

    exported_graph = nx.drawing.nx_pydot.read_dot(io.StringIO(content))

    assert exported_graph.nodes() == graph.nodes()
    assert nx.to_dict_of_dicts(graph).keys() == nx.to_dict_of_dicts(exported_graph).keys()


def test_format_to_json(dependencies):
    content = to_json(dependencies=dependencies)

    assert '"from_module": "opportunity.models",' in content
