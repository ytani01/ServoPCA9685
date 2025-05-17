#
# (c) 2020 Yoichi Tanibayashi
#
"""
Control many servo motors via PCA9685
"""
__author__ = 'Yoichi Tanibayashi'
__data__   = '2020'

import time
import pigpio
from .pigpioPCA9685 import PCA9685
from .my_logger import get_logger


class Servo:
    """
    Servo motor driver for Music Box
    """
    PW_OFF = 0
    PW_NOP = -1
    PW_MIN = 500
    PW_MAX = 2500
    PW_CENTER = int((PW_MIN + PW_MAX) / 2)

    def __init__(self, channel=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
                 pi=None, debug=False):
        """ Constructor

        Parameters
        ----------
        channel: list of int
            servo channel
        pi: pigpio.pi
        """
        self._dbg = debug
        self.__log = get_logger(self.__class__.__name__, self._dbg)
        self.__log.debug('channel=%s', channel)

        self._active = False

        self._ch = channel
        self._pi = pi
        self._my_pi = False
        if self._pi is None:
            self._pi = pigpio.pi()
            if not self._pi.connected:
                self.__log.error('pigpio connection error')
                exit(0)
            self._my_pi = True

        self._dev = PCA9685(self._pi, debug=self._dbg)
        self._dev.set_frequency(50)
        self._active = True

        self._pw = [self.PW_OFF] * len(self._ch)  # all off
        self.all_off()

    def __str__(self):
        str_val = ""
        for i, p in enumerate(self._pw):
            str_val += 'ch[%d]:%d, ' % (self._ch[i], p)

        str_val = str_val.rstrip(', ')
        return str_val

    def set_pw1(self, ch, pw):
        """
        set pulse width of specified one servo motor

        Parameters
        ----------
        ch: int
            channe
        pw: int
            pulse width
        """
        self.__log.debug('ch=%s, pw=%s', ch, pw)

        if ch not in self._ch:
            msg = 'invalid channel number:%s.' % (ch)
            msg += ' select one of %s' % (self._ch)
            raise ValueError(msg)

        if pw != 0 and ( pw < self.PW_MIN or pw > self.PW_MAX ):
            msg = 'ch[%s]:invalid pulse width:%s.' % (ch, pw)
            msg += ' specify 0 or %s .. %s .. %s' % (
                self.PW_MIN, self.PW_CENTER, self.PW_MAX)
            raise ValueError(msg)

        self._dev.set_pulse_width(ch, pw)

    def set_pw(self, pw):
        """
        set pulse widths of all servo motors at once

        Parameters
        ----------
        pw: list of int
            list of pulse width
            pulse width: PW_NOP: do nothing
        """
        self.__log.debug('pw=%s', pw)

        if len(pw) != len(self._ch):
            msg = 'pw:%s invalid length:%s != %s' % (
                pw, len(pw), len(self._ch))
            raise ValueError(msg)

        for i, p in enumerate(pw):
            if p == self.PW_NOP:
                self.__log.debug('ch[%s]: do nothing', self._ch[i])
                continue

            if p != 0 and (p < self.PW_MIN or p > self.PW_MAX):
                msg = 'ch[%s]:invalid pulse width:%s.' % (self._ch[i], p)
                msg += ' specify 0 or %s .. %s .. %s' % (
                    self.PW_MIN, self.PW_CENTER, self.PW_MAX)
                raise ValueError(msg)

            self._pw[i] = p
            self._dev.set_pulse_width(self._ch[i], p)

        self.__log.debug('pw=%s', self._pw)

    def all_off(self):
        """
        turn off all servo motors
        """
        self.__log.debug('')

        self._dev.set_pulse_width(-1, self.PW_OFF)

    def end(self):
        """ Call at the end of program """
        self.__log.debug('')
        self.all_off()
        time.sleep(0.5)

        if self._active:
            self._dev.cancel()
            self._active = False

        if self._my_pi:
            self._pi.stop()
