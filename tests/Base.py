import pytest
import pytest_asyncio
from typing import TypeAlias

LOOP_SCOPE = 'module'

MovieType : TypeAlias = dict[str, str | list[str] | dict[str, int]]


class TestBase:
    
    def __init_subclass__(cls) -> None:
        for _method_name in cls().__dir__():
            if not _method_name.startswith('_'):
                _method = getattr(cls, _method_name)
                if str(_method.__class__) == "<class 'function'>":
                    _method = pytest.mark.asyncio(loop_scope = LOOP_SCOPE)(_method)
                    
                    

def fixture(*args, **kwargs):
    loop_scope = kwargs.pop('loop_scope', LOOP_SCOPE)
    return pytest_asyncio.fixture(*args, loop_scope = loop_scope, **kwargs)