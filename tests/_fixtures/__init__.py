import os
import pytest
from mock import patch


@pytest.fixture(autouse=True)
def env_patch_fixture():
    with patch.dict(os.environ, {'ADVENT_SESSION_COOKIE': '',
                                 'ADVENT_PRIV_BOARDS': '1111111',
                                 'ADVENT_DISABLE_TERMCOLOR': '1'}):
        yield
