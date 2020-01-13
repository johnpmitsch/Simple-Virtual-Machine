#!/usr/bin/env python3

from vm import VirtualMachine
from programs import add

c = VirtualMachine(add)
c.run()

assert c.output()[0] == 0x22

