# A program to model a CPU and memory as a virtual machine. The programs are loaded as bytes in "memory", which is an array the the class initalizes with
#
# The instruction set is as follows:
# load_word   0x01
# store_word  0x02
# add         0x03
# sub         0x04
# halt        0xff
#
# Which does the following
#
# load_word  reg (addr)  # Load value at given address into register
# store_word reg (addr)  # Store the value in register at the given address
# add reg1 reg2          # Set reg1 = reg1 + reg2
# sub reg1 reg2          # Set reg1 = reg1 - reg2
# halt
#


class VirtualMachine:
    def __init__(self, memory):
        self.memory = memory
        self.internal_memory = [0x00, 0x00, 0x00]

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

    def run(self):
        while self.program_counter() < len(self.instructions()):
            self.run_instruction()
            self.increment()
