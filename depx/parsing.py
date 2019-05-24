from typed_ast import ast3, ast27
from typed_ast._ast3 import Module as ModuleAST3
from collections import deque
import logging
import os
import re


logger = logging.getLogger(__name__)


def _parse_ast(src):
    # thanks to Black
    for feature_version in (7, 6):
        try:
            return ast3.parse(src, feature_version=feature_version)
        except SyntaxError:
            continue
    return ast27.parse(src)


def _dependency(*, from_module, to_module, category='', is_relative=False, level=0, **kwargs):
    dep = {
        'from_module': from_module,
        'to_module': to_module,  # currently, this could also be a symbol within a module
        'category': category,
        'is_relative': is_relative,
        'level': level,
    }
    dep.update(kwargs)
    return dep


def _goes_local(node):
    func_defs = (ast27.FunctionDef, ast3.FunctionDef)
    try:
        func_defs += (ast3.AsyncFunctionDef,)
    except AttributeError:  # Py < 3.5
        pass
    return isinstance(node, func_defs)


def _walk(node):
    iter_child_nodes = ast3.iter_child_nodes
    if not isinstance(node, ModuleAST3):
        iter_child_nodes = ast27.iter_child_nodes

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
    tree = _parse_ast(text)
    for node, is_local in _walk(tree):
        category = 'local' if is_local else 'module'
        if isinstance(node, (ast27.Import, ast3.Import)):
            for alias in node.names:
                yield _dependency(
                    category=category,
                    from_module=base_name,
                    from_name=alias.asname or alias.name,
                    to_module=alias.name,
                    to_name=alias.name,
                )
        elif isinstance(node, (ast27.ImportFrom, ast3.ImportFrom)):
            level = node.level
            module = node.module
            for alias in node.names:
                if level:
                    to_module = module or alias.name  # module is None for 'from . import'
                    to_module = _resolve_relative_name(to_module, base_name, level)
                else:
                    to_module = module
                yield _dependency(
                    category=category,
                    from_module=base_name,
                    from_name=alias.asname or alias.name,
                    to_module=to_module,
                    to_name=alias.name,
                    is_relative=bool(level),
                    level=level,
                )


def filter_top_level_names(deps):
    for dep in deps:
        dep['from_module'] = dep['from_module'].split('.')[0]
        dep['to_module'] = dep['to_module'].split('.')[0]
        dep['from_name'] = ''
        dep['to_name'] = ''
        yield dep


def _resolve_relative_name(name, base_name, level):
    parts = base_name and base_name.split('.')
    if not (parts and all(parts)) or len(parts) < level:
        logger.warning(
            'Unable to resolve relative name %r: bad or missing basename (%r)',
            name, base_name
        )
        return name
    resolved_base = parts[:-level]
    return '.'.join(resolved_base + [name])


if __name__ == '__main__':
    from pprint import pprint
    for x in find_module_imports(__file__):
        pprint(x)
