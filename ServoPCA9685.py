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
    _log = get_logger(__name__, False)

    PWM_MIN = 500
    PWM_MAX = 2500
    PWM_CENTER = int((PWM_MIN + PWM_MAX) / 2)

    def __init__(self, pi, channel=[], debug=False):
        """
        initialize all servo motors
        """
        self._dbg = debug
        __class__._log = get_logger(__class__.__name__, self._dbg)
        self._log.debug('channel=%s', channel)

        self._active = False

        self._pi = pi
        self._ch = channel

        self._dev = PCA9685(self._pi, debug=self._dbg)
        self._dev.set_frequency(50)
        self._active = True

        self._pwm = [0] * len(self._ch)  # all off

    def __str__(self):
        str_val = ""
        for i, p in enumerate(self._pwm):
            str_val += 'ch[%d]:%d, ' % (self._ch[i], p)

        str_val = str_val.rstrip(', ')
        return str_val

    def set_pwm(self, pwm):
        """
        pwm: list of pulse widths
        """
        self._log.debug('pwm=%s', pwm)

        if len(pwm) != len(self._ch):
            self._log.error('invalid pwm: %s', pwm)
            return

        self._pwm = pwm

        for i, p in enumerate(self._pwm):
            if p != 0:
                if p < ServoPCA9685.PWM_MIN:
                    p = ServoPCA9685.PWM_MIN
                if p > ServoPCA9685.PWM_MAX:
                    p = ServoPCA9685.PWM_MAX

            self._dev.set_pulse_width(self._ch[i], p)

    def all_off(self):
        self._log.debug('')

        self._dev.set_pulse_width(-1, 0)

    def end(self):
        self._log.debug('')
        self.all_off()
        time.sleep(0.5)

        if self._active:
            self._dev.cancel()
            self._active = False


import time
import random


class SampleApp:
    _log = get_logger(__name__, False)

    def __init__(self, channel=[], interval=1.0,
                 pwm_min=ServoPCA9685.PWM_MIN, pwm_max=ServoPCA9685.PWM_MAX,
                 random=False, debug=False):
        self._dbg = debug
        __class__._log = get_logger(__class__.__name__, self._dbg)
        self._log.debug('channel=%s, interval=%s', channel, interval)
        self._log.debug('pwm_min=%s, pwm_max=%s', pwm_min, pwm_max)
        self._log.debug('random=%s', random)

        self._ch = channel
        self._interval = interval
        self._pwm_min = pwm_min
        self._pwm_max = pwm_max
        self._random = random

        if self._pwm_min > self._pwm_max:
            self._log.warning('pwm_min(%s) > pwm_mzx(%s): swap',
                              self._pwm_min, self._pwm_max)
            (self._pwm_min, self._pwm_max) = (self._pwm_max, self._pwm_min)

        self._pwm_center = int((self._pwm_min + self._pwm_max) / 2)

        self._pi = pigpio.pi()
        if not self._pi.connected:
            exit(0)

        self._servo = ServoPCA9685(self._pi, self._ch, self._dbg)
        print(self._servo)

    def main(self):
        self._log.debug('')

        count = 0
        while True:
            if self._random:
                pwm = []
                for c in self._ch:
                    pwm.append(random.randint(self._pwm_min, self._pwm_max))
            else:
                if count % 2 == 0:
                    pwm = [self._pwm_min] * len(self._ch)
                else:
                    pwm = [self._pwm_max] * len(self._ch)

            self._servo.set_pwm(pwm)
            self._log.debug('_servo=%s', self._servo)

            count += 1
            time.sleep(self._interval)

    def end(self):
        self._servo.set_pwm([ServoPCA9685.PWM_CENTER] * len(self._ch))
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
@click.option('--pwm_min', '-min', 'pwm_min', type=int,
              default=ServoPCA9685.PWM_MIN,
              help='min pwm value')
@click.option('--pwm_max', '-max', 'pwm_max', type=int,
              default=ServoPCA9685.PWM_MAX,
              help='max pwm value')
@click.option('--random', '-r', 'random', is_flag=True, default=False,
              help='random flag')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def main(channel, interval, pwm_min, pwm_max, random, debug):
    _log = get_logger(__name__, debug)
    _log.debug('channel=%s, interval=%s, pwm_min=%s, pwm_max=%s, random=%s',
               channel, interval, pwm_min, pwm_max, random)

    app = SampleApp(channel, interval, pwm_min, pwm_max, random, debug=debug)
    try:
        app.main()
    finally:
        _log.debug('end')
        app.end()


if __name__ == "__main__":
    main()
