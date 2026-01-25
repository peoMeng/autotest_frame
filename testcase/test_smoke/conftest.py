import pytest

from page.android_page import AndroidUtil


@pytest.fixture
def android_util():
    return AndroidUtil()
