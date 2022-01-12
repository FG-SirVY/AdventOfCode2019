###############################################################################
# Day x, Task y                                                               #
###############################################################################

import aoc_util
import collections


year = 2019
day = 11


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
            return None
            
        return self.queue.popleft()


class Interpreter:
    def __init__(self, instr_list):
        self.instr_list = instr_list
        self.instr_ptr = 0
        self.in_pipe = PipeExit()
        self.out_pipe = PipeEntry()
        self.relative_base = 0
        self.additional_memory = {}
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

        self.terminating = False

        opcode //= 100

        for _ in range(MAX_PARAM_COUNT):
            self.param_modes.append(opcode % 10)
            opcode //= 10


    def get_value(self, target):
        if target >= len(self.memory.instr_list):
            return self.memory.additional_memory.get(target, 0)
        else:
            return self.memory.instr_list[target]


    def get_param(self, i, dereference=True):
        if self.param_modes[i] == 0:
            addr = self.get_value(self.memory.instr_ptr + i + 1)
            if not dereference:
                return addr
            return self.get_value(addr)    
        elif self.param_modes[i] == 1:
            return self.get_value(self.memory.instr_ptr + i + 1)
        elif self.param_modes[i] == 2:
            addr = self.memory.relative_base
            addr += self.get_value(self.memory.instr_ptr + i + 1)
            if not dereference:
                return addr
            return self.get_value(addr)   

        
    def set_value(self, target, val):
        if target >= len(self.memory.instr_list):
            self.memory.additional_memory[target] = val
        else:
            self.memory.instr_list[target] = val


    def add(self):
        op1 = self.get_param(0)
        op2 = self.get_param(1)
        target = self.get_param(2, dereference=False)

        self.set_value(target, op1 + op2)
        self.memory.instr_ptr += 4


    def multiply(self):
        op1 = self.get_param(0)
        op2 = self.get_param(1)
        target = self.get_param(2, dereference=False)

        self.set_value(target, op1 * op2)
        self.memory.instr_ptr += 4


    def input(self):
        target = self.get_param(0, dereference=False)
        input = self.memory.in_pipe.read()

        if input == None:
            return False

        self.set_value(target, input)
        self.memory.instr_ptr += 2

        return True


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
        target = self.get_param(2, dereference=False)

        value = int(lhs < rhs)
        self.set_value(target, value)

        self.memory.instr_ptr += 4


    def equal(self):
        lhs = self.get_param(0)
        rhs = self.get_param(1)
        target = self.get_param(2, dereference=False)

        value = int(lhs == rhs)
        self.set_value(target, value)

        self.memory.instr_ptr += 4

    
    def rel_base(self):
        target = self.get_param(0)
        self.memory.relative_base += target

        self.memory.instr_ptr += 2


    def execute(self):
        if self.op == 1:
            self.add()
        elif self.op == 2:
            self.multiply()
        elif self.op == 3:
            if not self.input():
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
        elif self.op == 9:
            self.rel_base()
        elif self.op == 99:
            self.terminating = True
            return False
        
        return True


def task(data_set: list[str]) -> int:
    fresh_program = [int(x) for x in data_set[0].split(",")]

    white_tiles = set([(0, 0)])

    output = PipeExit()
    interpreter = Interpreter(fresh_program)
    interpreter.out_pipe.connect_to(output)

    min_x = max_x = min_y = max_y = 0

    x = 0
    y = 0

    view = 0

    while 1:
        interpreter.in_pipe.write(1 if (x, y) in white_tiles else 0)
        interpreter.run()
        if interpreter.terminated:
            break
        
        color = output.read()
        direction = output.read()

        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x
        
        if y < min_y:
            min_y = y
        elif y > max_y:
            max_y = y

        if color == 1:
            white_tiles.add((x, y))
        if direction == 0:
            view -= 1
        elif direction == 1:
            view += 1

        view %= 4

        if view == 0:
            y -= 1
        elif view == 1:
            x += 1
        elif view == 2:
            y += 1
        elif view == 3:
            x -= 1

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print("#" if (x, y) in white_tiles else " ", end="")

        print()
    

    return 0


aoc_util.run_with_data_set(task, year, day)
