import pytest

from vextractor.vk.enumerates import Platform


def test_enum_values():
    assert Platform.MOBILE.value == 1
    assert Platform.IPHONE.value == 2
    assert Platform.IPAD.value == 3
    assert Platform.ANDROID.value == 4
    assert Platform.WINDOWS_PHONE.value == 5
    assert Platform.WINDOWS_10.value == 6
    assert Platform.FULL.value == 7


def test_enum_names():
    assert Platform.MOBILE.name == "MOBILE"
    assert Platform.IPHONE.name == "IPHONE"
    assert Platform.IPAD.name == "IPAD"
    assert Platform.ANDROID.name == "ANDROID"
    assert Platform.WINDOWS_PHONE.name == "WINDOWS_PHONE"
    assert Platform.WINDOWS_10.name == "WINDOWS_10"
    assert Platform.FULL.name == "FULL"


def test_enum_members():
    assert Platform.MOBILE in Platform
    assert Platform.IPHONE in Platform
    assert Platform.IPAD in Platform
    assert Platform.ANDROID in Platform
    assert Platform.WINDOWS_PHONE in Platform
    assert Platform.WINDOWS_10 in Platform
    assert Platform.FULL in Platform


def test_invalid_enum_member():
    with pytest.raises(ValueError):
        Platform(8)
        Platform(-1)


def test_enum_comparison():
    assert Platform.MOBILE < Platform.IPHONE
    assert Platform.IPHONE > Platform.MOBILE
    assert Platform.IPAD != Platform.MOBILE


def test_enum_iteration():
    platforms = [p.name for p in Platform]
    assert platforms == [
        "MOBILE",
        "IPHONE",
        "IPAD",
        "ANDROID",
        "WINDOWS_PHONE",
        "WINDOWS_10",
        "FULL",
    ]
