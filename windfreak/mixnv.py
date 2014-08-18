#!/usr/bin/env python

from ._device import Device
import weakref

class _MixNVFM(object):
    def __init__(self, dev):
        self.__dev = weakref.ref(dev)

    def _send_cmd(self, s):
        return self.__dev()._send_cmd(s)

    @property
    def deviation(self):
        return int(self._send_cmd(b'd?'))

    @deviation.setter
    def deviation(self, p):
        p = int(p)
        if not 0 <= p <= 32760:
            raise ValueError('FM deviation has to be a integer '
                             'between 0 and 32760')
        self._send_cmd('d%d' % p)

    @property
    def burst_repetitions(self):
        return int(self._send_cmd(b'r?'))

    @burst_repetitions.setter
    def burst_repetitions(self, p):
        p = int(p)
        if not 0 <= p <= 65535:
            raise ValueError('FM burst repetitions has to be a integer '
                             'between 0 and 65535')
        self._send_cmd('r%d' % p)

    @property
    def mod_step_delay(self):
        return int(self._send_cmd(b't?'))

    @mod_step_delay.setter
    def mod_step_delay(self, p):
        p = int(p)
        if not 0 <= p <= 65535:
            raise ValueError('FM mod step delay has to be a integer '
                             'between 0 and 65535')
        self._send_cmd('t%d' % p)

    @property
    def on(self):
        return bool(int(self._send_cmd(b'm?')))

    @on.setter
    def on(self, b):
        self._send_cmd('m%d' % bool(b))

    @property
    def continuous(self):
        return bool(int(self._send_cmd(b'c?')))

    @continuous.setter
    def continuous(self, b):
        self._send_cmd('c%d' % bool(b))

    @property
    def src_internal(self):
        return bool(int(self._send_cmd(b'i?')))

    @src_internal.setter
    def src_internal(self, b):
        self._send_cmd('i%d' % bool(b))

    def burst(self):
        self._send_cmd(b'b')


class MixNV(Device):
    def __init__(self, dev):
        Device.__init__(self, dev)
        self.__fm = _MixNVFM(self)

    @property
    def freq(self):
        return float(self._send_cmd(b'f?'))

    @freq.setter
    def freq(self, f):
        self._send_cmd('f%.2f' % f)

    @property
    def power(self):
        return int(self._send_cmd(b'a?'))

    @power.setter
    def power(self, p):
        p = int(p)
        if not 0 <= p <= 7:
            raise ValueError('Power has to be a integer between 0 and 7')
        self._send_cmd('a%d' % p)

    @property
    def fm(self):
        return self.__fm

    @property
    def is_mixer(self):
        return not int(self._send_cmd(b'l?'))

    @is_mixer.setter
    def is_mixer(self, b):
        self._send_cmd('l%d' % (not bool(b)))

    @property
    def ref_internal(self):
        return bool(int(self._send_cmd(b'x?')))

    @ref_internal.setter
    def ref_internal(self, b):
        self._send_cmd('x%d' % bool(b))

    def program(self):
        self._send_cmd(b'e')

    @property
    def firmware_version(self):
        return self._send_cmd(b'v')

    @property
    def model_type(self):
        return self._send_cmd(b'+')

    @property
    def serial_number(self):
        return self._send_cmd(b'-')

    @property
    def help_info(self):
        return self._send_cmd(b'?')

    @property
    def phase_locked(self):
        return bool(int(self._send_cmd(b'p')))
