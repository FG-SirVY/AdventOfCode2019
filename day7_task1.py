###############################################################################
# Day x, Task y                                                               #
###############################################################################

import aoc_util
import itertools


year = 2019
day = 7
data_str = """3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"""


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


def test_thrust_setting(thuster_setting, fresh_program):
    thrust_input = 0

    for i in thuster_setting:
        program = fresh_program.copy()
        memory = Memory(program, [i, thrust_input])
        memory.run()
        thrust_input = memory.outputs[0]

    return thrust_input


def task(data_set: list[str]) -> int:
    fresh_program = [int(x) for x in data_set[0].split(",")]

    max_val = 0
    
    for thruster_setting in itertools.permutations([0, 1, 2, 3, 4]):
        val = test_thrust_setting(thruster_setting, fresh_program)
        if val > max_val:
            max_val = val
    
    return max_val


aoc_util.run_with_data_str(task, data_str)
aoc_util.run_with_data_set(task, year, day)
