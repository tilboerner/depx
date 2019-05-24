from jinja2 import Template
import json
import networkx as nx
from networkx.readwrite import json_graph
from networkx.drawing.nx_agraph import write_dot


def create_graph_from(dependencies):
    graph = nx.DiGraph()

    for dependency in dependencies:
        try:
            weight = graph[dependency['from_module']][dependency['to_module']]['weight']
            weight += 1
            graph[dependency['from_module']][dependency['to_module']]['weight'] = weight
        except KeyError:
            graph.add_edge(dependency['from_module'], dependency['to_module'], weight=1)
    return graph


def to_html(**kwargs):
    data = json_graph.node_link_data(kwargs['graph'])

    with open('depx/template.html') as file_:
        template = Template(file_.read())

        filename = 'graph.html'
        with open(filename, 'w') as report_file:
            report_file.write(template.render(data=data, path=kwargs['path']))
    return filename


def to_graphml(**kwargs):
    filename = 'graph.graphml'
    nx.write_graphml(kwargs['graph'], filename)
    return filename


def to_dotfile(**kwargs):
    filename = 'graph.dot'
    write_dot(kwargs['graph'], 'graph.dot')
    return filename


def to_json(**kwargs):
    return json.dumps(kwargs['dependencies'], indent=4)
