from scripts.evaluate_release_tag import filter_non_alpha_releases, GitReader, DocBuildDecider
import pytest
from pep440_version_utils import Version
from typing import List
from _pytest.monkeypatch import MonkeyPatch


@pytest.mark.parametrize("releases, expected",
    [
        (
            [Version("1.1.0"), Version("2.2.0")],
            [Version("1.1.0"), Version("2.2.0")],
        ),
        (
            [Version("1.1.0"), Version("2.2.0"), Version("1.1.1a")],
            [Version("1.1.0"), Version("2.2.0")],
        ),
(
            [Version("1.1.0"), Version("2.2.0"), Version("1.1.1a1")],
            [Version("1.1.0"), Version("2.2.0")],
        )
    ],
)
def test_filter_non_alpha_releases(releases: List[Version], expected: List[Version]):
    result = filter_non_alpha_releases(releases)
    assert result == expected


@pytest.mark.parametrize("releases, tag, expected",
     [
         (
            [Version("1.1.0"), Version("2.2.0")], Version("2.3.0"), True,
         ),
         (
            [Version("1.1.0"), Version("2.2.0"), Version("2.3.0a1")], Version("2.2.1"), True,
         ),
         (
            [Version("1.1.0"), Version("2.2.0"), Version("2.3.0")], Version("1.2.0"), True,
         ),
         (
            [Version("1.1.0"), Version("1.2.0a1"), Version("2.3.0")], Version("1.1.2"), True,
         ),
         (
            [Version("1.1.0"), Version("2.2.0"), Version("2.3.0")], Version("2.2.1"), False,
         ),
         (
            [Version("1.1.0"), Version("2.2.0"), Version("2.3.0")], Version("2.2.1a1"), False,
         ),
     ],
)
def test_should_build_docs(default_git_reader: GitReader, monkeypatch: MonkeyPatch, releases: List[Version],
                           tag: Version, expected: bool):
    monkeypatch.setattr(default_git_reader, "get_existing_tag_versions", lambda: releases)
    doc_builder = DocBuildDecider(default_git_reader)
    result = doc_builder.should_build_docs(tag)
    assert result == expected
