import pathlib
from lark import Lark, Token
from lark import Transformer
from pyscratch.scratch import Scratch, Block

name_map = {}

with open(str(pathlib.Path(__file__).parent.resolve()) + "/block_name_mapping.csv", "r") as file:
    contents = file.read()
    for line in contents.split("\n"):
        key, value = line.split(",")
        name_map[key] = value


def find_function(block_name, block_args):
    try:
        return name_map[block_name], block_args
    except KeyError:
        if block_args:
            # We are setting an undefined variable
            return "setvariableto", [block_name, block_args[0]]
        else:
            # We are getting a variable
            return "_variable", [block_name]


class ScratchTextTransformer(Transformer):
    def __init__(self):
        super(ScratchTextTransformer, self).__init__()
        self.scratch = Scratch()

    def variable(self, items):
        name = items[0].value.replace("\"", "")
        return self.scratch._variable(name)

    def loop(self, items):
        name = ""
        stack = []
        args = []
        for item in items:
            try:
                if item.type == "WORD":
                    name += str(item)
            except AttributeError:
                if item is not None:
                    # This item mey be a parameter.
                    if type(item) == Block:
                        # Item is a block parameter
                        stack.append(item)
                    elif type(item) == list:
                        if len(item) == 3:
                            # Item is a variable parameter
                            args.append(item)
                        elif len(item) > 0:
                            # Item is a static parameter
                            args.append(item[0])

        try:
            function_name, args = find_function(name, args)
            block_func = getattr(self.scratch, function_name)
            try:
                block = block_func(*args, stack)
                return block
            except:
                print(
                    f"The args and or stack supplied in block {function_name}, '{*args, stack}', do not match the syntax.")
        except KeyError:
            print(f"Block name '{function_name}' does not exist!")
        return None

    def block(self, items):
        name = ""
        args = []
        if len(items) > 0:
            for item in items:
                try:
                    if item.type == "WORD":
                        name += str(item)
                except AttributeError:
                    if item is not None:
                        if type(item) == Block:
                            # This block was already computed as a function, so return directly
                            return item
                        elif type(item) == list:
                            if len(item) == 3:
                                # Item is a variable parameter
                                args.append(item)
                            elif len(item) > 0:
                                # Item is a static parameter
                                args.append(item[0])
        if name == "":
            # The 'block' was actually a newline
            return
        try:
            function_name, args = find_function(name, args)
            block_func = getattr(self.scratch, function_name)
            try:
                block = block_func(*args)
                return block
            except IOError:
                print(f"The args supplied, '{args}', do not match the syntax.")
                print(name)
        except KeyError:
            print(f"Block name '{name}' does not exist!")
        return None

    def param(self, items):
        args = []
        for item in items:
            if type(item) == Block:
                args.append([item])
            elif type(item) == list:
                # This item was already computed as a variable, so return directly
                return item
            elif item is not None:
                if item.type == "STRING":
                    args.append(str(item[1:-1]))
                elif item.type == "NUMBER":
                    args.append(float(item))
        return args

    def start(self, items):
        stack = [self.scratch.greenflag()]
        for item in items:
            if item is not None:
                stack.append(item)
        self.scratch.stack(stack)
        self.scratch.compile()
        return " ".join(item.opcode for item in stack)


def parse(filepath):
    file = open(str(pathlib.Path(__file__).parent.resolve()) + "/scratchtext.ebnf")
    scratchtext_parser = Lark(file.read(), start='start', parser="lalr")
    transformer = ScratchTextTransformer()
    transformer.transform(scratchtext_parser.parse(open(filepath).read()))
