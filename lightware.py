#!/usr/bin/env python3
import logging
import subprocess
import argparse

LIGHTWARE_GPIO_VALUE_LOW = '0'
LIGHTWARE_GPIO_VALUE_HIGH = '1'
LIGHTWARE_BASE_PATH = '/sys/class/gpio'
LIGHTWARE_GPIO_PATH = LIGHTWARE_BASE_PATH + '/gpio{0}'
LIGHTWARE_EXPORT_PATH = LIGHTWARE_BASE_PATH + '/export'
LIGHTWARE_GPIO_VALUE_PATH = LIGHTWARE_GPIO_PATH + '/value'
LIGHTWARE_UNEXPORT_PATH = LIGHTWARE_BASE_PATH + '/unexport'
LIGHTWARE_GPIO_DIRECTION_PATH = LIGHTWARE_GPIO_PATH + '/direction'


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='system.log')


logging.debug('Running')


class LightWare:
    def __init__(self, num):
        self._number = num
        self._direction = 'out'
        try:
            self._f = open(self._lightware_gpio_value_path(), 'r+')
        except FileNotFoundError:
            logging.debug('FileNotFoundError:' + self._lightware_gpio_value_path())

    def _lightware_gpio_direction_path(self):
        return LIGHTWARE_GPIO_DIRECTION_PATH.format(self._number)

    def _lightware_gpio_value_path(self):
        return LIGHTWARE_GPIO_VALUE_PATH.format(self._number)

    def on(self):
        self._f.write(LIGHTWARE_GPIO_VALUE_HIGH)
        self._f.seek(0)
        self._f.close()

    def off(self):
        self._f.write(LIGHTWARE_GPIO_VALUE_LOW)
        self._f.seek(0)
        self._f.close()

    def read(self):
        val = self._f.read()
        self._f.seek(0)
        self._f.close()
        return int(val)


def lightware_dimmer(channel, value):

    if (int(value) < 0) or (int(value) > 100):
        raise ValueError
    else:
        subprocess.call(["dimmer.py", channel, value])  # doesn't capture output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("channel", help="channel num", type=int)
    parser.add_argument("state", help="channel state", type=int)
    args = parser.parse_args()
    if args.state == 0:
        LightWare(args.channel).off()
    else:
        LightWare(args.channel).on()
