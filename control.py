#!/usr/bin/env python3
from os import path

PIN_NUM = [5, 6, 13, 19, 26, 12, 16, 20]


def export_pin(number):
    try:
        if not path.isdir('/sys/class/gpio/gpio{0}'.format(number)):
            with open('/sys/class/gpio/export', 'w') as export:
                export.write('{0}'.format(number))

        if path.exists('/sys/class/gpio/gpio{0}/direction'.format(number)):
            with open('/sys/class/gpio/gpio{0}/direction'.format(number), 'w') as gpio_dir:
                gpio_dir.write('out')

    except Exception as e:
        print(e)

if __name__ == "__main__":
    for pin in PIN_NUM:
        export_pin(pin)
