from jinja2 import Template
import json
import networkx as nx
from networkx.readwrite import json_graph
from networkx.drawing.nx_pydot import to_pydot
import io


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
        content = template.render(data=data, path=kwargs['path'])
        return content


def to_graphml(**kwargs):
    in_memory_file = io.BytesIO()

    nx.write_graphml(kwargs['graph'], in_memory_file)
    return in_memory_file.getvalue().decode('utf-8')


def to_dotfile(**kwargs):
    pydot = to_pydot(kwargs['graph'])
    return pydot.to_string()


def to_json(**kwargs):
    return json.dumps(kwargs['dependencies'], indent=4)
