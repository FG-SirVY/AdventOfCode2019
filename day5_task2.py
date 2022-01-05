###############################################################################
# Day x, Task y                                                               #
###############################################################################

import aoc_util


year = 2019
day = 5
data_str = """1,1,1,4,99,5,6,0,99"""


MAX_PARAM_COUNT = 5


class Memory:
    def __init__(self, instr_list, inputs):
        self.instr_list = instr_list
        self.instr_ptr = 0
        self.inputs = inputs
        self.input_index = -1
        self.outputs = []


    def get_input(self):
        self.input_index += 1
        return self.inputs[self.input_index]


    def set_output(self, val):
        self.outputs.append(val)


    def run(self):
        while 1:
            instr = Instruction(self)
            if not instr.execute():
                return


class Instruction:
    def __init__(self, memory: Memory):
        self.param_modes = []
        self.memory = memory

        opcode = memory.instr_list[self.memory.instr_ptr]
        self.original = opcode

        self.op = opcode % 100
        opcode -= self.op
        self.all_immediate = False

        opcode //= 100

        for _ in range(MAX_PARAM_COUNT):
            self.param_modes.append(opcode % 2)
            opcode //= 10

        pass


    def get_param(self, i, immmediate=False):
        if self.param_modes[i] == 0 and not immmediate:
            addr = self.memory.instr_list[self.memory.instr_ptr + i + 1]
            return self.memory.instr_list[addr]
        else:
            return self.memory.instr_list[self.memory.instr_ptr + i + 1]

        
    def set_value(self, target, val):
        self.memory.instr_list[target] = val


    def add(self):
        op1 = self.get_param(0)
        op2 = self.get_param(1)
        target = self.get_param(2, immmediate=True)

        self.set_value(target, op1 + op2)
        self.memory.instr_ptr += 4


    def multiply(self):
        op1 = self.get_param(0)
        op2 = self.get_param(1)
        target = self.get_param(2, immmediate=True)

        self.set_value(target, op1 * op2)
        self.memory.instr_ptr += 4


    def input(self):
        target = self.get_param(0, immmediate=True)
        input = self.memory.get_input()

        self.set_value(target, input)
        self.memory.instr_ptr += 2


    def output(self):
        source = self.get_param(0)

        self.memory.set_output(source)
        self.memory.instr_ptr += 2


    def jump_true(self):
        source = self.get_param(0)
        jump = self.get_param(1)

        if source != 0:
            self.memory.instr_ptr = jump
        else:
            self.memory.instr_ptr += 3


    def jump_false(self):
        source = self.get_param(0)
        jump = self.get_param(1)

        if source == 0:
            self.memory.instr_ptr = jump
        else:
            self.memory.instr_ptr += 3


    def less_than(self):
        lhs = self.get_param(0)
        rhs = self.get_param(1)
        target = self.get_param(2, immmediate=True)

        value = int(lhs < rhs)
        self.set_value(target, value)

        self.memory.instr_ptr += 4


    def equal(self):
        lhs = self.get_param(0)
        rhs = self.get_param(1)
        target = self.get_param(2, immmediate=True)

        value = int(lhs == rhs)
        self.set_value(target, value)

        self.memory.instr_ptr += 4


    def execute(self):
        if self.op == 1:
            self.add()
        elif self.op == 2:
            self.multiply()
        elif self.op == 3:
            self.input()
        elif self.op == 4:
            self.output()
        elif self.op == 5:
            self.jump_true()
        elif self.op == 6:
            self.jump_false()
        elif self.op == 7:
            self.less_than()
        elif self.op == 8:
            self.equal()
        elif self.op == 99:
            return False
        
        return True


def task(data_set: list[str]) -> int:
    program = [int(x) for x in data_set[0].split(",")]

    memory = Memory(program, [5])
    memory.run()

    return memory.outputs.pop()


#aoc_util.run_with_data_str(task, data_str)
aoc_util.run_with_data_set(task, year, day)
