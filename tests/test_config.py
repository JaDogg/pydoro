import sys

import pytest

from pydoro.pydoro_core.config import Configuration


@pytest.fixture
def clean_argv_env(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['pydoro'])
    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.setenv('USERPROFILE', str(tmp_path))
    monkeypatch.chdir(tmp_path)


def test_create_default_ini_in_missing_directory(
        tmp_path, monkeypatch, clean_argv_env,
):
    cfg_file = tmp_path / 'nonexistent-sub' / 'pydoro.ini'
    monkeypatch.setenv('PYDORO_CONFIG_FILE', str(cfg_file))
    config = Configuration()
    assert cfg_file.is_file()
    assert config.work_minutes == 25
    # the created file is a valid config which loads cleanly
    assert Configuration().work_minutes == 25
