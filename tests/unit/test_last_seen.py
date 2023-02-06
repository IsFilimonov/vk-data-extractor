import pytest

from vextractor.vk.dataclasses import LastSeen
from vextractor.vk.enumerates import Platform


def test_last_seen_valid_platform_id():
    last_seen = LastSeen(platform=1, time=1234567890)
    assert last_seen.platform == Platform.MOBILE
    assert last_seen.time == 1234567890


def test_last_seen_valid_platform_enum():
    last_seen = LastSeen(platform=Platform.MOBILE, time=1234567890)
    assert last_seen.platform == Platform.MOBILE
    assert last_seen.time == 1234567890


def test_last_seen_invalid_platform_id():
    with pytest.raises(AssertionError, match=r"Unsupported platform id: -1"):
        LastSeen(platform=-1, time=1234567890)

    with pytest.raises(AssertionError, match=r"Unsupported platform id: 8"):
        LastSeen(platform=8, time=1234567890)
