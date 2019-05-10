import sys
from textwrap import dedent

import pytest

from depx.parsing import find_imports_from_text, _dependency


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
        'RELATIVE_IMPORT',
        'from .sibling_namespace import some_module',
        [
            _dependency(
                from_module='RELATIVE_IMPORT',
                from_name='some_module',
                to_module='sibling_namespace',
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
