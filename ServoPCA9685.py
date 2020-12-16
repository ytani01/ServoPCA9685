#!/usr/bin/env python3
#
# (c) 2020 Yoichi Tanibayashi
#
"""
Control many servo motors via PCA9685
"""
__author__ = 'Yoichi Tanibayashi'
__data__   = '2020'

from pigpioPCA9685 import PCA9685
import pigpio
from MyLogger import get_logger


class ServoPCA9685:
    """
    """
    PW_OFF = 0
    PW_NOP = -1
    PW_MIN = 500
    PW_MAX = 2500
    PW_CENTER = int((PW_MIN + PW_MAX) / 2)

    _log = get_logger(__name__, False)

    def __init__(self, channel=[], pi=None, debug=False):
        """ Constractor

        Parameters
        ----------
        pi: pigpio.pi

        channel: list of int
            servo channel
        """
        self._dbg = debug
        __class__._log = get_logger(__class__.__name__, self._dbg)
        self._log.debug('channel=%s', channel)

        self._active = False

        self._ch = channel
        self._pi = pi
        self._my_pi = False
        if self._pi is None:
            self._pi = pigpio.pi()
            if not self._pi.connected:
                self._log.error('pigpio connection error')
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
        self._log.debug('ch=%s, pw=%s', ch, pw)

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
            pulse width: -1: do nothing
        """
        self._log.debug('pw=%s', pw)

        if len(pw) != len(self._ch):
            msg = 'pw:%s invalid length:%s != %s' % (
                pw, len(pw), len(self._ch))
            raise ValueError(msg)

        for i, p in enumerate(pw):
            if p < 0:
                self._log.debug('ch[%s]: do nothing', self._ch[i])
                continue

            if p != 0 and (p < self.PW_MIN or p > self.PW_MAX):
                msg = 'ch[%s]:invalid pulse width:%s.' % (self._ch[i], p)
                msg += ' specify 0 or %s .. %s .. %s' % (
                    self.PW_MIN, self.PW_CENTER, self.PW_MAX)
                raise ValueError(msg)

            self._pw[i] = p
            self._dev.set_pulse_width(self._ch[i], p)

        self._log.debug('pw=%s', self._pw)

    def all_off(self):
        """
        turn off all servo motors
        """
        self._log.debug('')

        self._dev.set_pulse_width(-1, self.PW_OFF)

    def end(self):
        """ Call at the end of program
        """
        self._log.debug('')
        self.all_off()
        time.sleep(0.5)

        if self._active:
            self._dev.cancel()
            self._active = False

        if self._my_pi:
            self._pi.stop()


import time
import random


class SampleApp:
    """ Sample application class    
    """
    PROMPT_STR = '> '
    
    _log = get_logger(__name__, False)

    def __init__(self, channel=[], interval=1.0,
                 pw_min=ServoPCA9685.PW_MIN,
                 pw_max=ServoPCA9685.PW_MAX,
                 random_flag=False, debug=False):
        self._dbg = debug
        __class__._log = get_logger(__class__.__name__, self._dbg)
        self._log.debug('channel=%s, interval=%s', channel, interval)
        self._log.debug('pw_min=%s, pw_max=%s', pw_min, pw_max)
        self._log.debug('random_flag=%s', random_flag)

        self._ch = channel
        self._interval = interval
        self._pw_min = pw_min
        self._pw_max = pw_max
        self._random_flag = random_flag

        if self._pw_min > self._pw_max:
            self._log.warning('pw_min(%s) > pw_max(%s): swap',
                              self._pw_min, self._pw_max)
            (self._pw_min, self._pw_max) = (self._pw_max, self._pw_min)

        self._pw_center = int((self._pw_min + self._pw_max) / 2)

        self._pi = pigpio.pi()
        if not self._pi.connected:
            self._log.error('pigpiod connection error')
            exit(1)

        self._servo = ServoPCA9685(self._ch, self._pi, debug=self._dbg)
        print(self._servo)

    def main(self):
        """
        main routine
        """
        self._log.debug('')

        count = 0
        while True:
            if self._random_flag:
                pw = []
                for c in self._ch:
                    pw.append(random.randint(self._pw_min, self._pw_max))
            else:
                if count % 2 == 0:
                    pw = [self._pw_min] * len(self._ch)
                else:
                    pw = [self._pw_max] * len(self._ch)

            self._servo.set_pw(pw)
            self._log.debug('_servo=%s', self._servo)

            count += 1
            time.sleep(self._interval)

    def end(self):
        self._servo.set_pw([ServoPCA9685.PW_CENTER] * len(self._ch))
        time.sleep(.5)
        self._servo.end()
        self._pi.stop()


import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS, help='''
Test Program for ServoPCA9685''')
@click.argument('channel', type=int, nargs=-1)
@click.option('--interval', '-i', 'interval', type=float, default=1.0,
              help='interval [sec]')
@click.option('--pw_min', '-min', 'pw_min', type=int,
              default=ServoPCA9685.PW_MIN,
              help='min pulse width')
@click.option('--pw_max', '-max', 'pw_max', type=int,
              default=ServoPCA9685.PW_MAX,
              help='max pulse width')
@click.option('--random', '-r', 'random_flag', is_flag=True,
              default=False,
              help='random flag')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def main(channel, interval, pw_min, pw_max, random_flag, debug):
    _log = get_logger(__name__, debug)
    _log.debug('channel=%s', channel)
    _log.debug('interval=%s', interval)
    _log.debug('pw_min=%s, pw_max=%s', pw_min, pw_max)
    _log.debug('random_flag=%s', random_flag)

    app = SampleApp(channel, interval, pw_min, pw_max, random_flag,
                    debug=debug)
    try:
        app.main()
    finally:
        _log.debug('end')
        app.end()


if __name__ == "__main__":
    main()
