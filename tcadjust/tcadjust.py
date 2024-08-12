#!/usr/bin/env python3

import sys

def tcadjust(tc):
    f = open('/etc/bitbit/tcfactor', 'r')
    tcfactor = float(f.read().strip())
    f.close()

    moves = 0
    maintime = 0
    increment = 0

    i = tc.find('/')
    if i != -1:
        moves = int(tc[:i])
        tc = tc[i + 1:]
    i = tc.find('+')
    if i != -1:
        maintime = float(tc[:i])
        increment = float(tc[i + 1:])
    else:
        maintime = tc

    tc = ''
    if moves > 0:
        tc += f'{moves}/'
    tc += f'{tcfactor * maintime}'
    if increment > 0:
        tc += f'+{tcfactor * increment}'

    return tc

def main():
    print(tcadjust(sys.argv[1]))

if __name__ == '__main__':
    main()
