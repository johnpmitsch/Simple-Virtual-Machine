# A program to model a CPU and memory as a virtual machine. The programs are loaded as bytes in "memory", which is an array the the class initalizes with
#
# Memory is used with the following format:
# The instructions occupy the first 14 bytes, followed by 2 bytes for output and 4 bytes for two separate 2 byte inputs:
#
# 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19
# __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __
# INSTRUCTIONS ---------------------------^ OUT-^ IN-1^ IN-2^
#
#
# The instruction set is as follows:
# load_word   0x01
# store_word  0x02
# add         0x03
# sub         0x04
# halt        0xff
#
# Which, while taking arguements, does the following
#
# load_word  reg (addr)  # Load value at given address into register
# store_word reg (addr)  # Store the value in register at the given address
# add reg1 reg2          # Set reg1 = reg1 + reg2
# sub reg1 reg2          # Set reg1 = reg1 - reg2
# halt

from itertools import repeat
from struct import pack, unpack
from collections import namedtuple


class VirtualMachine:
    def __init__(self):
        self.memory = [None] * 100
        self.internal_memory = [0x00, 0x00, 0x00]
        self.programs = {}
        self.memory_offset = 0

    def program_counter(self):
        return self.internal_memory[0]

    def registers(self):
        return self.internal_memory[1:]

    def get_register(self, reg_num):
        return self.internal_memory[reg_num]

    def instructions(self):
        return self.memory[:12]

    def inputs(self):
        return [self.memory[16:18], self.memory[18:20]]

    def output(self):
        return self.memory[14:16]

    def increment(self):
        self.internal_memory[0] += 1

    def current_value(self):
        return self.memory[self.program_counter()]

    def load_word(self):
        self.increment()
        register_index = self.current_value()
        self.increment()
        self.internal_memory[register_index] = self.current_value()

    def store_word(self):
        self.increment()
        register_value = self.get_register(self.current_value())
        self.increment()
        address = self.current_value()
        self.memory[address] = register_value

    def add(self):
        self.increment()
        first = self.get_register(self.current_value())
        self.increment()
        second = self.get_register(self.current_value())
        self.internal_memory[1] = first + second

    def subtract(self):
        self.increment()
        first = self.current_value()
        self.increment()
        second = self.current_value()
        self.internal_memory[1] = first - second

    def run_instruction(self):
        instruction = self.memory[self.program_counter()]

        if instruction == 0x01:
            self.load_word()
        elif instruction == 0x02:
            self.store_word()
        elif instruction == 0x03:
            self.add()
        elif instruction == 0x04:
            self.subtract()
        elif instruction == 0xFF:
            next()

    def load_program(self, exec_file):
        program_bytes = self.open_program(exec_file)
        segment_headers = []
        full_program_length = 0
        # The first byte is how many segments we have in the executable
        program_bytes, segment_count = self.pop_bytes(program_bytes, 1)
        # Get the segment header info and store it
        for i in repeat(None, segment_count[0]):
            program_bytes, segment_header = self.pop_bytes(program_bytes, 3)
            segment_header_data = self.get_segment_headers(segment_header)
            segment_headers.append(segment_header_data)
        # Use the segment header data to load programs into memory
        for header in segment_headers:
            start = header.location
            end = header.location + header.length
            program = program_bytes[start:end]
            full_program_length += len(program)
            # The first bit of the first byte is:
            # 0 for text segments (code)
            # 1 for data segments (input data)
            type = header.type_and_target >> 7
            # The location is the last 7 bits of the first header byte
            target_address = header.type_and_target & 0b01111111
            self.load_into_memory(program, target_address + self.memory_offset)
        self.memory_offset += full_program_length + 1

    def open_program(self, exec_file):
        with open(exec_file, "rb") as binaryfile:
            bytes = bytearray(binaryfile.read())
            return bytes

    def get_segment_headers(self, segment_header):
        SegmentHeader = namedtuple("SegmentHeader", "type_and_target length location")
        print(segment_header)
        segment_header_data = SegmentHeader._make(unpack("BBB", segment_header))
        return segment_header_data

    def pop_bytes(self, bytes, end):
        popped = bytes[0:end]
        del bytes[0:end]
        return bytes, popped

    def load_into_memory(self, program, location):
        self.memory = (
            self.memory[:location]
            + list(program)
            + self.memory[location + len(program) :]
        )

    def run(self):
        while self.program_counter() < len(self.instructions()):
            self.run_instruction()
            self.increment()
