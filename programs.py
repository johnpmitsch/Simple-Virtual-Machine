# The following is an "add" program to add two numbers together. Here it is as "assembly"
#
# load_word r1 (0x10)   # Load input 1 into register 1
# load_word r2 (0x12)   # Load input 2 into register 2
# add r1 r2             # Add the two registers, store the result in register 1
# store_word r1 (0x0E)  # Store the value in register 1 to the output device
# halt

add = [
    0x01,
    0x01,
    0x10,
    0x01,
    0x02,
    0x12,
    0x03,
    0x01,
    0x02,
    0x02,
    0x01,
    0x0E,
    0xFF,
    0x00,
    0x00,
    0x00,
    0xA1,
    0x14,
    0x0C,
    0x00,
]
