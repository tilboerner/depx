from jinja2 import Template
import json
import networkx as nx
from networkx.readwrite import json_graph


def create_from(dependencies):
    G = nx.DiGraph()

    modules = {}
    for dependency in dependencies:
        try:
            weight = G[dependency['from_module']][dependency['to_module']]['weight']
            weight += 1
            G[dependency['from_module']][dependency['to_module']]['weight'] = weight
        except KeyError:
            G.add_edge(dependency['from_module'], dependency['to_module'], weight=1)
    return G


def export_to(G, export_format):
    filename = "graph.graphml"
    nx.write_graphml(G, filename)
    return filename


def report(G):
    # WIP
    data = json_graph.node_link_data(G)

    # weight -> value

    # import ipdb; ipdb.set_trace()
    with open('depx/template.html') as file_:
        template = Template(file_.read())

        filename = "report.html"
        with open(filename, "w") as f:
            f.write(template.render(content='bla', path='.'))
    return filename
