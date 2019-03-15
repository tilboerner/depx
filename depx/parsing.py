import ast
from pathlib import PurePath


def _dependency(*, from_module, to_module, category='', is_relative=False, **kwargs):
    return {
        'from_module': from_module,
        'to_module': to_module,  # currently, this could also be a symbol within a module
        'category': category,
        'is_relative': is_relative,
        **kwargs,
    }


def _goes_local(node):
    return isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))


def _walk(node):
    from collections import deque
    iter_child_nodes = ast.iter_child_nodes
    todo = deque([(node, False)])
    while todo:
        node, is_local = todo.popleft()
        child_local = is_local or _goes_local(node)
        todo.extend((child, child_local) for child in iter_child_nodes(node))
        yield node, is_local


def find_module_imports(path, base_name=''):
    with open(path) as f:
        text = f.read()
    module_name = PurePath(path).stem
    if base_name:
        module_name = base_name + '.' + module_name
    return find_imports(text, module_name)


def find_imports(text, base_name):
    tree = ast.parse(text)
    for node, is_local in _walk(tree):
        category = 'local' if is_local else 'module'
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield _dependency(
                    category=category,
                    from_module=base_name,
                    from_name=alias.asname or alias.name,
                    to_module=alias.name,
                    to_name=alias.name,
                )
        elif isinstance(node, ast.ImportFrom):
            level = node.level
            to_module = node.module
            for alias in node.names:
                yield _dependency(
                    category=category,
                    from_module=base_name,
                    from_name=alias.asname or alias.name,
                    to_module=to_module,
                    to_name=alias.name,
                    is_relative=bool(level),
                    level=level,
                )


if __name__ == '__main__':
    from pprint import pprint
    for x in find_module_imports(__file__):
        pprint(x)
