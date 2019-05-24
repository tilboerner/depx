import ast
import os
import re


def _dependency(*, from_module, to_module, category='', is_relative=False, **kwargs):
    dep = {
        'from_module': from_module,
        'to_module': to_module,  # currently, this could also be a symbol within a module
        'category': category,
        'is_relative': is_relative,
    }
    dep.update(kwargs)
    return dep


def _goes_local(node):
    func_defs = (ast.FunctionDef,)
    try:
        func_defs += (ast.AsyncFunctionDef,)
    except AttributeError:  # Py < 3.5
        pass
    return isinstance(node, func_defs)


def _walk(node):
    from collections import deque
    iter_child_nodes = ast.iter_child_nodes
    todo = deque([(node, False)])
    while todo:
        node, is_local = todo.popleft()
        child_local = is_local or _goes_local(node)
        todo.extend((child, child_local) for child in iter_child_nodes(node))
        yield node, is_local


def _is_package(path):
    init_path = os.path.join(path, '__init__.py')
    return os.path.isfile(init_path)


def _find_base_name(path, base_name=''):
    parent = os.path.dirname(path)
    if not _is_package(parent):
        return base_name
    parent_name = os.path.basename(parent)
    if base_name:
        base_name = parent_name + '.' + base_name
    else:
        base_name = parent_name
    return _find_base_name(parent, base_name)


def _is_module(path):
    if not os.path.isfile(path):
        return False
    if path.endswith('.py'):
        return True
    with open(path) as f:
        try:
            line = f.readline()
        except UnicodeError:
            return False
    return bool(line and re.match(r'^#!.*?python', line))


def find_imports(path):
    if _is_module(path):
        yield from find_module_imports(path)
    else:
        yield from find_imports_in_directory(path)


def find_imports_in_directory(directory_path):
    for path, subdirs, files in os.walk(directory_path):
        subdirs[:] = [
            d for d in subdirs if _is_package(os.path.join(path, d))
        ]
        for filename in files:
            module_path = os.path.join(path, filename)
            if not _is_module(module_path):
                continue
            yield from find_module_imports(module_path)


def find_module_imports(path, base_name=None):
    with open(path) as f:
        text = f.read()
    module_name = os.path.splitext(os.path.basename(path))[0]
    if base_name is None:
        base_name = _find_base_name(path)
    if base_name:
        module_name = base_name + '.' + module_name
    return find_imports_from_text(text, module_name)


def find_imports_from_text(text, base_name):
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
