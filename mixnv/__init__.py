#!/usr/bin/env python

import serial
import usb.core
import pyudev
from time import sleep

try:
    _unicode = unicode
except:
    _unicode = str

class MixNV(object):
    def __wait(self):
        sleep(0.01)

    def __reset_dev(self):
        ctx = pyudev.Context()
        udev = pyudev.Device.from_device_file(ctx, self.__port)
        # FIXME
        dev = usb.core.find(idVendor=int(udev['ID_VENDOR_ID'], base=16),
                            idProduct=int(udev['ID_MODEL_ID'], base=16))
        dev.reset()
        self.__wait()

    def __init__(self, port):
        self.__port = port
        self.__reset_dev()
        self.__serial = serial.Serial(port, timeout=0.01, writeTimeout=0.01,
                                      parity='N', stopbits=1, bytesize=7)

    def __send_cmd(self, s):
        if isinstance(s, _unicode):
            s = s.encode()
        self.__serial.write(s)
        res = self.__serial.read(4096).decode()
        self.__wait()
        return res

    @property
    def freq(self):
        return float(self.__send_cmd(b'f?'))

    @freq.setter
    def freq(self, f):
        self.__send_cmd('f%.2f' % f)

    @property
    def power(self):
        return int(self.__send_cmd(b'a?'))

    @power.setter
    def power(self, p):
        p = int(p)
        if not 0 <= p <= 7:
            raise ValueError('Power has to be a integer from 0 to 7')
        self.__send_cmd('a%d' % p)
