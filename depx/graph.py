from jinja2 import Template
import networkx as nx
from networkx.readwrite import json_graph
from networkx.drawing.nx_agraph import write_dot


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


def export_to(G, export_format, path='.'):
    if export_format == 'html':
        return to_html(G, path)
    if export_format == 'graphml':
        return to_graphml(G)
    if export_format == 'dotfile':
        return to_dotfile(G)


def to_html(G, path):
    data = json_graph.node_link_data(G)

    with open('depx/template.html') as file_:
        template = Template(file_.read())

        filename = "report.html"
        with open(filename, "w") as report_file:
            report_file.write(template.render(data=data, path=path))
    return filename


def to_graphml(G):
    filename = "graph.graphml"
    nx.write_graphml(G, filename)
    return filename


def to_dotfile(G):
    filename = "graph.dot"
    write_dot(G, "graph.dot")
    return filename
