#!/usr/bin/env python3
#
# (c) 2020 Yoichi Tanibayashi
#
"""
Control servo motor via PCA9685
"""
__author__ = 'Yoichi Tanibayashi'
__data__   = '2020'

import Adafruit_PCA9685
import random
import time
import click
from MyLogger import get_logger
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class ServoPCA9685:
    _log = get_logger(__name__, False)

    PWM_MIN = 100
    PWM_MAX = 590
    PWM_INIT = int((PWM_MIN + PWM_MAX) / 2)

    def __init__(self, channel, debug=False):
        """
        initialize all servo motors
        """
        self._dbg = debug
        __class__._log = get_logger(__class__.__name__, self._dbg)
        self._log.debug('channel=%s', channel)
        print('%s' % channel)

        self._ch = channel

        self._pwm = [self.PWM_INIT] * len(self._ch)

        self._dev = Adafruit_PCA9685.PCA9685()
        self._dev.set_pwm_freq(60)
        self.set_pwm(self._pwm)

    def set_pwm(self, pwm):
        self._log.debug('pwm=%s', pwm)

        if len(pwm) != len(self._ch):
            self._log.error('invalid length: pwm=%s', pwm)
            return

        self._pwm = pwm

        i = 0
        for p in self._pwm:
            '''
            msg = 'channel[%d]=%s, pwm=%s' % (i, self._ch[i], p)
            print(msg)
            '''
            self._dev.set_pwm(self._ch[i], 0, p)
            i += 1


class SampleApp:
    _log = get_logger(__name__, False)

    def __init__(self, channel, interval=1.0, debug=False):
        self._dbg = debug
        __class__._log = get_logger(__class__.__name__, self._dbg)
        self._log.debug('channel=%s, interval=%s', channel, interval)

        self._ch = []
        for c in channel:
            self._ch.append(int(c))
        print('_ch=%s' % self._ch)

        self._interval = interval

        self._servo = ServoPCA9685(self._ch)
        time.sleep(1)

    def main(self):
        self._log.debug('')

        while True:
            pwm = []
            for c in self._ch:
                pwm.append(random.randint(ServoPCA9685.PWM_MIN,
                                          ServoPCA9685.PWM_MAX))
            print('pwm=%s' % pwm)
            self._servo.set_pwm(pwm)
            time.sleep(self._interval)


@click.command(context_settings=CONTEXT_SETTINGS, help='''
Test Program for ServoPCA9685 class''')
@click.argument('channel', nargs=-1)
@click.option('--interval', '-i', 'interval', type=float, default=1.0,
              help='interval sec')
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug flag')
def main(channel, interval, debug):
    _log = get_logger(__name__, debug)
    _log.debug('channel=%s, interval=%s', channel, interval)

    app = SampleApp(channel, interval, debug=debug)
    try:
        app.main()
    finally:
        _log.debug('end')


if __name__ == "__main__":
    main()
