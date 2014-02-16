from hydra2 import *
import ast
import random
import re

def hydraInt(x):
    return int(ast.literal_eval(x))

def hydraFloat(x):
    return float(ast.literal_eval(x))

class HydraCommands(HydraParser):
    @SmartCommand(hydraInt, hydraInt)
    def wod(self, n, again=10):
        total_successes = 0
        reroll = False
        output = ''

        def plural(s, p, n):
            if n == 1:
                return (n,s)
            return (n,s+p)

        while n or rerolls > 0:
            if not n:
                output += ' %i %s.\n' % plural('Reroll','s',rerolls)
            else:
                rerolls = n
                n = None
            pool = [random.randint(1,10) for i in range(rerolls)]
            successes = len([i for i in pool if i > 7])
            total_successes += successes
            rerolls = len([i for i in pool if i >= again])
            pool = [str(i) for i in pool]
            output += '{ %s } %i %s.' % ((', '.join(pool),)+plural('Success','es',successes))
            reroll = reroll or rerolls > 0
        if reroll:
            output += '\nTotal Successes: %i' % total_successes
        self.print(output)

    @SmartCommand(hydraFloat)
    def p(self, value):
        success = random.uniform(0,100) <= value
        self.print(success and "Success." or "Failure.")

    @RawCommand
    def roll(self, value):
        print(value)
        match = re.match(r"(\d+)(d|sr)(\d+)([+-]\d+)?", value)
        if not match:
            raise Exception("No valid dice roll.")
        count = int(match.group(1))
        sr = match.group(2).lower() == 'sr'
        pool = int(match.group(3))
        modifier = 0
        if match.group(4) and match.group(4).strip() != '':
            modifier = int(match.group(4).strip())
        rolls = [random.randint(1, sr and 6 or pool) for i in range(count)]
        line = '{ ' + ', '.join(map(lambda x: str(x), rolls)) + ' } '
        if modifier:
            line += '%s %i ' % ((modifier > 0 and '+' or '-'), abs(modifier))
        if sr:
            line += '= %i' % (sum(x > pool for x in rolls) + modifier)
        else:
            line += '= %i' % (sum(rolls) + modifier)
        self.print(line)

if __name__ == '__main__':
    cmds = HydraCommands()
    while True:
        cmds.execute(input(">"))