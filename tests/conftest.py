from unittest.mock import MagicMock, patch

import dbus
import pytest


def zwo_device_only():
    array = dbus.Array()
    array.append(dbus.String('ZWO CCD 1283 some junk data'))
    return array


def qhy_device_only():
    array = dbus.Array()
    array.append(dbus.String('QHYCCD 1283 some junk data'))
    return array


@pytest.fixture(autouse=True)
def dbus_loop_mock(scope='session'):
    with patch('dbus.mainloop.glib.DBusGMainLoop') as mock:
        yield mock


@pytest.fixture(autouse=True)
def dbus_session_mock():
    with patch('dbus.SessionBus') as mock:
        yield mock


@pytest.fixture
def dbus_interface_mock():
    obj_mock = MagicMock()

    with patch('dbus.Interface') as m:
        m.return_value = obj_mock
        yield obj_mock


@pytest.fixture
def zwo_device_response(dbus_interface_mock, scope='function'):
    dbus_interface_mock.getDevices.side_effect = zwo_device_only
    return dbus_interface_mock


@pytest.fixture
def qhy_device_response(dbus_interface_mock, scope='function'):
    dbus_interface_mock.getDevices.side_effect = qhy_device_only
    return dbus_interface_mock


@pytest.fixture
def no_device_response(dbus_interface_mock, scope='function'):
    dbus_interface_mock.getDevices.side_effect = dbus.Array
    return dbus_interface_mock


@pytest.fixture(autouse=True)
def no_sleep():
    with patch('time.sleep'):
        yield
