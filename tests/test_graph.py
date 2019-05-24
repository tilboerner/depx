from depx.graph import (
    create_graph_from, to_html, to_graphml, to_dotfile, to_json
)
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

    to_html(graph=graph, path=os.getcwd())

    assert 'graph.html' in os.listdir()

    os.remove('graph.html')


def test_format_to_graphml(dependencies):
    graph = create_graph_from(dependencies)

    to_graphml(graph=graph, path=os.getcwd())

    assert 'graph.graphml' in os.listdir()

    os.remove('graph.graphml')


def test_format_to_dotfile(dependencies):
    graph = create_graph_from(dependencies)

    to_dotfile(graph=graph, path=os.getcwd())

    assert 'graph.dot' in os.listdir()

    os.remove('graph.dot')


def test_format_to_json(dependencies):
    graph_json = to_json(dependencies=dependencies)

    assert isinstance(graph_json, str)
