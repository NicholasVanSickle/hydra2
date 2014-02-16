class Command:
    def __init__(self, fn):
        self._fn = fn
        self.obj = None

    def fn(self, *args, **kw):
        if not self.obj:
            self._fn(*args, **kw)
        self._fn(self.obj, *args, **kw)
        
    def __call__(self, *args, **kw):
        self.fn(*args, **kw)

    def __get__(self, instance, owner):
        self.obj = instance
        return self

class _SmartCommand(Command):
    def __init__(self, fn, *args):
        Command.__init__(self, fn)
        self.format = args

    def __call__(self, *args, **kw):
        self.fn(*[f(x) for f, x in zip(self.format, args[2:])], **kw)

def SmartCommand(*args):
    def inner(fn):
        return _SmartCommand(fn, *args)
    return inner
        
class RawCommand(Command):
    def __call__(self, *args, **kw):
        self.fn(args[0][len(args[1]):].lstrip(), **kw)
    
def get_commands(scope):
    return {name.lower():command for name,command in scope.items() if isinstance(command,Command)}

class HydraParser:
    def __init__(self):
        self.commands = {m.lower(): m for m in dir(self) if isinstance(getattr(self, m), Command)}

    def _print(self, x):
        print(x)

    def print(self, *args):
        self._print(' '.join([str(x) for x in args]))

    def execute(self, line):
        args = parse(line)
        if args[0].lower() in self.commands:
            try:
                getattr(self, self.commands[args[0].lower()])(*([line]+args))
            except:
                self.print("Invalid usage of %s." % args[0].upper())
        else:
            self.print("No command %s found." % args[0].upper())

def parse(line):
    chunks = []
    prev = None
    state = None
    buffer = ''
    
    quotes = ['"', "'"]
    for c in line.lstrip():
        if state in quotes:
            if c == state and prev != '\\':
                state = None
            else:
                buffer += c
        else:
            if c == ' ':
                chunks.append(buffer)
                buffer = ''
            elif c in quotes:          
                state = c
            else:
                buffer += c
        prev = c
    chunks.append(buffer)
    
    return chunks
    
if __name__ == '__main__':
    commands = get_commands(locals())
    while True:
        line = input('> ')
        args = parse(line)
        if args[0].lower() in commands:
            commands[args[0].lower()](*([line]+args))
        else:
            print("Command not found %s" % args[0].lower())