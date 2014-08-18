#!/usr/bin/env python

import serial
import usb.core
import pyudev
from time import sleep
import itertools

try:
    _unicode = unicode
except:
    _unicode = str

_udev_ctx = pyudev.Context()

class Device(object):
    def _wait(self):
        sleep(0.01)

    def __find_usbdev(self, udev):
        for dev in udev.ancestors:
            if (dev.driver == 'usb' and dev.subsystem == 'usb' and
                'BUSNUM' in dev and 'DEVNUM' in dev):
                return usb.core.find(bus=int(dev['BUSNUM']),
                                     address=int(dev['DEVNUM']))

    def __init_dev(self, dev):
        udev = pyudev.Device.from_device_file(_udev_ctx, dev)
        usb_dev = self.__find_usbdev(udev)
        if usb_dev is None:
            raise RuntimeError('Cannot find usb device.')
        usb_dev.reset()
        self._wait()
        for child in itertools.chain(udev, *udev.children):
            if udev.subsystem == 'tty':
                return '/dev/' + udev.sys_name

    @property
    def _port(self):
        return self.__port

    @property
    def _serial(self):
        return self.__serial

    def __init__(self, dev):
        self.__port = self.__init_dev(dev)
        self.__serial = serial.Serial(self.__port, timeout=0.01,
                                      writeTimeout=0.01, parity='N',
                                      stopbits=1, bytesize=7)

    def _send_cmd(self, s):
        if isinstance(s, _unicode):
            s = s.encode()
        self.__serial.write(s)
        res = self.__serial.read(4096).decode()
        self._wait()
        return res
