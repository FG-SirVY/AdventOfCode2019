###############################################################################
# Day x, Task y                                                               #
###############################################################################

import aoc_util
import itertools, collections


year = 2019
day = 7
data_str = """3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"""


MAX_PARAM_COUNT = 5


class PipeEntry:
    def __init__(self):
        self.exit = None


    def connect_to(self, exit):
        self.exit = exit


    def write(self, val):
        if self.exit:
            self.exit.write(val)


class PipeExit:
    def __init__(self):
        self.queue = collections.deque()


    def write(self, val):
        self.queue.append(val)


    def read(self):
        if len(self.queue) == 0:
            return (-1, 0)
            
        return (0, self.queue.popleft())


class Interpreter:
    def __init__(self, instr_list):
        self.instr_list = instr_list
        self.instr_ptr = 0
        self.in_pipe = PipeExit()
        self.out_pipe = PipeEntry()
        self.input_index = -1
        self.outputs = []
        self.terminated = False


    def run(self):
        while 1:
            instr = Instruction(self)
            if not instr.execute():
                self.terminated = instr.terminating
                return


class Instruction:
    def __init__(self, memory: Interpreter):
        self.param_modes = []
        self.memory = memory

        opcode = memory.instr_list[self.memory.instr_ptr]
        self.original = opcode

        self.op = opcode % 100
        opcode -= self.op
        self.all_immediate = False

        self.terminating = False

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
        input = self.memory.in_pipe.read()

        if input[0] == -1:
            return -1

        self.set_value(target, input[1])
        self.memory.instr_ptr += 2

        return 0


    def output(self):
        source = self.get_param(0)

        self.memory.out_pipe.write(source)
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
            if self.input() == -1:
                return False
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
            self.terminating = True
            return False
        
        return True


def test_thrust_setting(thruster_setting, fresh_program):
    thrust_input = 0
    amplifiers = []

    for index, setting in enumerate(thruster_setting):
        program = fresh_program.copy()
        amplifier = Interpreter(program)

        amplifier.in_pipe.write(setting)
        if index == 0:
            amplifier.in_pipe.write(0)
        else:
            amplifiers[index - 1].out_pipe.connect_to(amplifier.in_pipe)
            if index == len(thruster_setting) - 1:
                amplifier.out_pipe.connect_to(amplifiers[0].in_pipe)
        amplifiers.append(amplifier)


    while 1:
        for a in amplifiers:
            a.run()

        if amplifiers[-1].terminated:
            return amplifiers[0].in_pipe.read()[1]


def task(data_set: list[str]) -> int:
    fresh_program = [int(x) for x in data_set[0].split(",")]

    max_val = 0
    
    for thruster_setting in itertools.permutations([5, 6, 7, 8, 9]):
        val = test_thrust_setting(thruster_setting, fresh_program)
        if val > max_val:
            max_val = val
    
    return max_val


aoc_util.run_with_data_str(task, data_str)
aoc_util.run_with_data_set(task, year, day)
