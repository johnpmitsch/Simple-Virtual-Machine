#!/usr/bin/env python3

from vm import VirtualMachine

c = VirtualMachine()
c.load_program("add_255_3.vef")
print(c.memory_offset)
print(c.memory)
c.load_program("sub_256_3.vef")
print(c.memory_offset)
print(c.memory)
c.run()

# assert c.output()[0] == 0x22

