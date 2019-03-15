from depx import graph
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
    G = graph.create_from(dependencies)

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

@pytest.mark.skip
def test_generate_a_report(dependencies):
    G = graph.create_from(dependencies)

    graph.report(G)

    assert 'yourdepx.html' in os.listdir()
