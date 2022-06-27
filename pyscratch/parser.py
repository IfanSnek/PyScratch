"""
parser.py
====================================
The script to parse a ScratchText file and use `scratch.py` to make an `.sb3` file.
"""

import pathlib
import re

from lark import Lark
from lark import Transformer, Token
from pyscratch.scratch import Scratch, Block

name_map = {}

# This function loads the file that maps the ScratchText names to the Scratch opcodes. These are stored in the name_map
# dictionary.
with open(str(pathlib.Path(__file__).parent.resolve()) + "/block_name_mapping.csv", "r") as file:
    contents = file.read()
    for line in contents.split("\n"):
        key, value = line.split(",")
        name_map[key] = value


def syntax_error(message):
    raise SyntaxError(message)


class ScratchTextTransformer(Transformer):
    """The Scratch Text Transformer class is based on the Lark Transformer class, and has its method called
    when an EBNF rule with a corresponding rule is met. Each method is fed the items the EBNF rule accepts, and
    they get formatted and called with the PyScratch construction functions. The return values of these methods fill
    the place with the EBNF rules in the parser tree."""

    def __init__(self):
        super(ScratchTextTransformer, self).__init__()

        # Supply a PyScratch Scratch Class for the rest of this transformer class to use.
        self.scratch = Scratch()

    def find_function(self, block_name, block_args):
        """
        This emthod returns the name of the Scratch class function from the ScratchText name, using the `name_map`
        dictionary. If there is no such block name, an attempt to create/use a variable is made. If creating a variable
        fails, a syntax error is thrown.

        :param block_name: Name of the block function is `Scratch.py`.
        :param block_args: Arguments to supply to the function
        :returns: A list with the function reference, and the formatted arguments.
        """

        if block_name == "setto":
            # We were explicitly told to set a variable to a value.
            # If the block is setto, the first argument is the variable name, and the second is the value.
            return "setvariableto", [block_args[0], block_args[1]]

        try:
            return name_map[block_name], block_args
        except KeyError:
            if block_args:  # If we receive arguments, we are likely trying to set a variable or call a function.
                if type(block_args[0]) == list:
                    # Set variable
                    return "setvariableto", [block_name, block_args]
                else:
                    # Call a function
                    return "call", [block_name, block_args]
            else:
                return "variable_", [block_name]

    def definition(self, items):
        """ A custom function holding blocks """

        # The name of this definition block will be appended to every time there is a word token in 'items'.
        name = ""

        # The stacked blocks of this definition will also be appended to when we find block trees.
        stack = []

        # Same with args, but for parameter tokens.
        args = []

        for item in items:
            try:
                # We try to get the type of the token to see if it is a word we can concatenate to the block name.
                # This will fail if 'item' is not a token.
                if item.type == "WORD":
                    name += str(item)
                else:
                    args.append(str(item))
            except AttributeError:
                # If 'item' is not a token, it is either None, or nested blocks.
                if item is not None:
                    # Nested stack
                    stack.append(item)
        self.scratch.make_block(name, args, stack)

    def loop(self, items):
        """ A loop can be made of words, blocks, or param type tokens. A loop is converted to a Scratch block that
        supports nesting. See scratchtext.ebnf for more info. """

        # The name of this loop block will be appended to every time there is a word token in 'items'.
        name = ""

        # The stacked blocks of this loop will also be appended to when we find block trees.
        stack = []
        stack2 = []  # For the if-else

        # Same with args, but for parameter tokens.
        args = []

        for item in items:
            try:
                # We try to get the type of the token to see if it is a word we can concatenate to the block name.
                # This will fail if 'item' is not a token.
                if item.type == "WORD":
                    name += str(item)
            except AttributeError:
                # If 'item' is not a token, it is either None, a Scratch Block, or a list of parameters.
                if item is not None:
                    # If 'item' is a Scratch block, then this block is a parameter for this loop.
                    if type(item) == Block:
                        if stack:
                            # The first stack is taken, put this in the second.
                            stack2.append(item)
                        else:
                            stack.append(item)

                    # If item is a list, the list could either be a static parameter or a variable. Variables are
                    # represented by lists of three attributes.
                    elif type(item) == list:
                        if len(item) == 3:
                            # Item is a variable parameter
                            args.append(item)
                        elif len(item) > 0:
                            # Item is a static parameter
                            args.append(item[0])

        # Now that we have accumulated all the needed data, we can find the Scratch constructor name for this block.
        function_name, args = self.find_function(name, args)

        # We can use this name to find the actual function for the constructor.
        block_func = getattr(self.scratch, function_name)

        # We then call that constructor with the args and nested blocks. Only supply stack2 if it is filled.
        block = block_func(*args, *([stack, stack2] if stack2 else [stack]))
        return block

    def block(self, items):
        """A block is made of parameters and words. This function turns a ScratchText block into a Scratch block. See
        scratchtext.ebnf for more info. """

        # The name of this loop block will be appended to every time there is a word token in 'items'.
        name = ""

        # Same with args, but for parameter tokens.
        args = []

        # Is the block a statement or is it a newline?
        if len(items) > 0:
            for item in items:
                try:
                    # We try to get the type of the token to see if it is a word we can concatenate to the block name.
                    # This will fail if 'item' is not a token.
                    if item.type == "WORD":
                        name += str(item)

                except AttributeError:
                    # If 'item' is not a token, it is either None, a Scratch Block, or a list of parameters.
                    if item is not None:
                        # If 'item' is a Scratch block, then this block was already formatted, so return directly.
                        if type(item) == Block:
                            return item

                        # If item is a list, the list could either be a static parameter or a variable. Variables are
                        # represented by lists of three attributes.
                        elif type(item) == list:
                            if len(item) == 3:
                                # Item is a variable parameter
                                args.append(item)
                            elif len(item) > 0:
                                # Item is a static parameter
                                args.append(item[0])

        # The 'block' was actually a newline
        if name == "":
            return

        # Now that we have accumulated all the needed data, we can find the Scratch constructor name for this block.
        function_name, args = self.find_function(name, args)

        # We can use this name to find the actual function for the constructor.
        block_func = getattr(self.scratch, function_name)

        # We then call that constructor with the args and nested blocks.
        block = block_func(*args)
        
        return block

    def param(self, items):
        """A parameter is made of combinations of blocks, words, and strings. See scratchtext.ebnf for more info."""

        # Save the arguments for this parameter in this array
        args = []

        for item in items:
            # If our argument is a block, then this block was already formatted, so append directly.
            if type(item) == Block:
                args.append([item])

            # If this item is a list, this parameter was already computed as a variable, so return directly.
            elif type(item) == list:
                return item

            # If this item is any other non-none value, it is just a string or variable.
            elif item is not None:
                if item.type == "STRING":
                    args.append(str(item[1:-1]))  # Format as string, removing the quotes, and append.
                elif item.type == "NUMBER":
                    args.append(float(item))  # Format as float and append.
        return args

    def start(self, items):
        """Start is the entry point of the parser, so it is the last to be called. It's items have already been
        formatted by the methods above. This will wrap up the usage of the Scratch class."""

        # Initialize the stack with a green flag block, then loop over all the immediate children and append them to
        # the stack.
        stack = []
        for item in items:
            if item is not None:
                stack.append(item)

        # Finally, build the stack and compile.
        self.scratch.stack(stack)
        self.scratch.compile()

        # Return all the opcodes for optional debugging.
        return " ".join(item.opcode for item in stack)


def parse(filepath):
    """
    This function takes a file path, loads it, then sends it to the Lark parser. The resulting tree is then
    sent to the ScratchTextTransformer where it is built into scratch blocks.

    :param filepath: Filepath of the file to parse
    :return: String with all the opcodes that aren't nested.
    """

    # Load the code file and walk through dependencies.
    code = ""
    with open(filepath, "r") as f:
        text = f.read()
        for line in text.split("\n"):
            if line.startswith("include"):
                line = re.sub(r"\/\/[^\n]*", "", line)
                imports = open(line[8:], "r").read()
                code += imports + "\n"
            else:
                code += line + "\n"

    # Parse the code and send it to the ScratchTextTransformer.
    scratchtext_parser = Lark(open(str(pathlib.Path(__file__).parent.resolve()) + "/scratchtext.ebnf"),
                              start='start', parser="lalr")
    transformer = ScratchTextTransformer()
    result = transformer.transform(scratchtext_parser.parse(code))

    # Return the opcodes for debugging
    return result
