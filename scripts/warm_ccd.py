#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import re
import time

from dbus.mainloop.glib import DBusGMainLoop  # NOQA: F811
import dbus  # NOQA: F811

ccd_regex = re.compile('(.*)?CCD.*')
temp = 20


class NoDevicesError(Exception):
    pass


def main():
    # Create a session bus.
    bus = dbus.SessionBus(mainloop=DBusGMainLoop(set_as_default=True))

    # Create an object that will proxy for a particular remote object.
    dbus_object = bus.get_object(
        'org.kde.kstars',
        '/KStars/INDI'
    )

    indi = dbus.Interface(dbus_object, 'org.kde.kstars.INDI')
    devices = indi.getDevices()
    print('Found devices: ', devices)
    ccd_devices = []
    # look for ccd cameras
    for d in devices:
        if ccd_regex.match(d):
            ccd_devices.append(d)

    if not ccd_devices:
        raise NoDevicesError('No CCD device found')

    for ccd in ccd_devices:
        # Set the CCD temperature to 20° this doesn't warm up the sensor
        # but it makes sure we reach the outside temperature
        indi.setNumber(ccd, 'CCD_TEMPERATURE', 'CCD_TEMPERATURE_VALUE', temp)
        # It seems QHY needs a COOLER ON otherwise it just turns off the cooling
        if 'QHY' in ccd:
            indi.setSwitch(ccd, 'CCD_COOLER', 'COOLER_ON', 'On')
            indi.sendProperty(ccd, 'CCD_COOLER')
        indi.sendProperty(ccd, 'CCD_TEMPERATURE')

    # Wait 5 seconds for indi to process the command
    time.sleep(5)

    # Loop and check if temperature has been reached
    while ccd_devices:
        for ccd in ccd_devices:
            actual_ccd_temp = indi.getNumber(ccd, 'CCD_TEMPERATURE', 'CCD_TEMPERATURE_VALUE')
            print(ccd, f'{actual_ccd_temp}°')
            if actual_ccd_temp > temp or temp - actual_ccd_temp <= 1:
                print('temp reached, removing ', ccd)
                ccd_devices.remove(ccd)

        time.sleep(5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExiting the program, bye!')
