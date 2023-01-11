from scripts.evaluate_release_tag import GitReader
import pytest


@pytest.fixture
def default_git_reader() -> GitReader:
    return GitReader()
