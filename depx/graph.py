from jinja2 import Template
import networkx as nx
from networkx.readwrite import json_graph


def create_from(dependencies):
    G = nx.DiGraph()

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


def report(G, path):
    data = json_graph.node_link_data(G)

    with open('depx/template.html') as file_:
        template = Template(file_.read())

        filename = "report.html"
        with open(filename, "w") as report_file:
            report_file.write(template.render(data=data, path=path))
    return filename
