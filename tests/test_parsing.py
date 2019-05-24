from operator import itemgetter

from depx.parsing import (
    find_imports_from_text, _dependency, find_imports, _is_package,
    _is_module, _find_base_name,
    filter_top_level_names)
import os
import pytest
import sys
from textwrap import dedent


@pytest.mark.parametrize('base_name,text,expected', [
    (
        'SINGLE_IMPORT',
        'import some_module',
        [
            _dependency(
                from_module='SINGLE_IMPORT',
                from_name='some_module',
                to_module='some_module',
                to_name='some_module',
                category='module',
            ),
        ],
    ),
    (
        'ALIAS_IMPORT',
        'import some_module as alias_name',
        [
            _dependency(
                from_module='ALIAS_IMPORT',
                from_name='alias_name',
                to_module='some_module',
                to_name='some_module',
                category='module',
            ),
        ],
    ),
    (
        'MULTI_IMPORT_ONE_LINE',
        'import some_module, other_module as other_alias',
        [
            _dependency(
                from_module='MULTI_IMPORT_ONE_LINE',
                from_name='some_module',
                to_module='some_module',
                to_name='some_module',
                category='module',
            ),
            _dependency(
                from_module='MULTI_IMPORT_ONE_LINE',
                from_name='other_alias',
                to_module='other_module',
                to_name='other_module',
                category='module',
            ),
        ],
    ),
    (
        'FROM_NAMESPACE_IMPORT_NAME',
        'from some_namespace import some_name',
        [
            _dependency(
                from_module='FROM_NAMESPACE_IMPORT_NAME',
                from_name='some_name',
                to_module='some_namespace',
                to_name='some_name',
                category='module',
                is_relative=False,
                level=0,
            ),
        ],
    ),
    (
        'FROM_NAMESPACE_IMPORT_NAME_ALIAS',
        'from some_namespace import some_name as alias_name',
        [
            _dependency(
                from_module='FROM_NAMESPACE_IMPORT_NAME_ALIAS',
                from_name='alias_name',
                to_module='some_namespace',
                to_name='some_name',
                category='module',
                is_relative=False,
                level=0,
            ),
        ],
    ),
    (
        'BASE_PACKAGE.RELATIVE_IMPORT',
        'from . import some_module',
        [
            _dependency(
                from_module='BASE_PACKAGE.RELATIVE_IMPORT',
                from_name='some_module',
                to_module='BASE_PACKAGE.some_module',
                to_name='some_module',
                category='module',
                is_relative=True,
                level=1,
            ),
        ],
    ),
    (
        'BASE_PACKAGE.RELATIVE_IMPORT_TO_SIBLING',
        'from .sibling_namespace import some_name',
        [
            _dependency(
                from_module='BASE_PACKAGE.RELATIVE_IMPORT_TO_SIBLING',
                from_name='some_name',
                to_module='BASE_PACKAGE.sibling_namespace',
                to_name='some_name',
                category='module',
                is_relative=True,
                level=1,
            ),
        ],
    ),
    (
        'RELATIVE_IMPORT_FROM_ROOT',
        'from . import some_module',
        [
            _dependency(
                from_module='RELATIVE_IMPORT_FROM_ROOT',
                from_name='some_module',
                to_module='some_module',
                to_name='some_module',
                category='module',
                is_relative=True,
                level=1,
            ),
        ],
    ),
    (
        'LOCAL_IMPORT',
        """
        def function():
            import some_module
        """,
        [
            _dependency(
                from_module='LOCAL_IMPORT',
                from_name='some_module',
                to_module='some_module',
                to_name='some_module',
                category='local',
            ),
        ],
    ),
])
def test_find_imports_from_text(base_name, text, expected):
    text = dedent(text)
    assert list(find_imports_from_text(text, base_name)) == expected


@pytest.mark.skipif(sys.version_info < (3, 5), reason='async not in older Pythons')
def test_find_imports_from_text__async_def():
    imports = list(find_imports_from_text(
        dedent("""
        async def function():
            import some_module
        """),
        base_name='TEST_MODULE',
    ))

    assert imports == [
        _dependency(
            from_module='TEST_MODULE',
            from_name='some_module',
            to_module='some_module',
            to_name='some_module',
            category='local',
        ),
    ]


@pytest.mark.parametrize('path,expected', [
    (os.getcwd() + '/tests/fake_project/another_fake_module', True),
    (os.getcwd() + '/tests/fake_project/fake_module', True),
    (os.getcwd() + '/tests/fake_project/random_folder', False),
])
def test_is_package(path, expected):
    assert _is_package(path) is expected


def test_find_imports():
    expected = [
        {
            'from_module': 'another_fake_module.missing_creativity',
            'to_module': 'fake_module.another_module',
            'category': 'module',
            'is_relative': False,
            'from_name': 'oh_nice',
            'to_name': 'oh_nice',
            'level': 0
        },
        {
            'from_module': 'another_fake_module.missing_creativity',
            'to_module': 'random',  # FIXME identify as internal
            'category': 'module',
            'is_relative': False,
            'from_name': 'random',
            'to_name': 'random',
            'level': 0
        },
        {
            'from_module': 'fake_module.__init__',
            'to_module': 'fake_module.a_module',
            'category': 'module',
            'is_relative': False,
            'from_name': 'fake_module.a_module',
            'to_name': 'fake_module.a_module',
            'level': 0
        },
        {
            'from_module': 'fake_module.__init__',
            'to_module': 'fake_module',
            'category': 'module',
            'is_relative': False,
            'from_name': 'another_module',
            'to_name': 'another_module',
            'level': 0
        },

        {
            'from_module': 'fake_module.a_module',
            'to_module': 'fake_module.another_module',
            'category': 'module',
            'is_relative': True,
            'from_name': 'oh_nice',
            'to_name': 'oh_nice',
            'level': 1
        }
    ]
    by_name = itemgetter('from_module', 'from_name', 'to_module', 'to_name')
    assert sorted(find_imports('tests/fake_project'), key=by_name) == sorted(expected, key=by_name)


@pytest.mark.parametrize('path,expected', [
    (os.getcwd() + '/tests/fake_project/another_fake_module/__init__.py', True),
    (os.getcwd() + '/tests/fake_project/another_fake_module/missing_creativity.py', True),
    (os.getcwd() + '/tests/fake_project/setup.py', True),
    (os.getcwd() + '/tests/fake_project/random_folder/python_file_without_py_extension.txt', True),
    (os.getcwd() + '/tests/fake_project/random_folder/cool_file.txt', False),
])
def test_is_module(path, expected):
    assert _is_module(path) is expected


@pytest.mark.parametrize('path,expected', [
    ('tests/fake_project/another_fake_module/__init__.py', 'another_fake_module'),
    (
        os.getcwd() + '/tests/fake_project/another_fake_module/missing_creativity.py',
        'another_fake_module'
    ),
    ('tests/fake_project/setup.py', ''),
])
def test_find_base_name(path, expected):
    assert _find_base_name(path) == expected


def test_filter_top_level_names():
    input = {
        'from_module': 'a.b',
        'to_module': 'x.y.z',
        'from_name': 'SOMETHING',
        'to_name': 'SOMETHING ELSE',
    }
    expected = {
        'from_module': 'a',
        'to_module': 'x',
        'from_name': '',
        'to_name': '',
    }
    assert list(filter_top_level_names([input])) == [expected]
