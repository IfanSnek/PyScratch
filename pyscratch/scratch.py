"""
scratch.py
====================================
The script to create a `.sb3` file dynamically.
"""

import json
import os
from zipfile import ZipFile


class Block:
    """A Block object represents a single Scratch block, whether it is a loop, event, or parameter. This object is
    responsible for containing different data about the Scratch block that can be accessed and modified by the Scratch
    class."""

    def __init__(self, block_id, opcode, inputs, fields):
        # Every block has a block id. This id is used in the project.json file to be referenced by other blocks.
        self.block_id = block_id

        # An opcode is a short code representing what type of block this block is. They usually follow the format
        # category_blockname where catergory is the type of block it is (eg. motion, looks, control).
        self.opcode = opcode

        # Block inputs are parameters the block takes. For example, the 'move steps' block takes the number of steps
        # to move. Block inputs are a dictionary with its key being the name of the parameter, and a value that is an
        # list of: A) a number representing if the input is static (1) or variable (2), and B) The value of the data.
        # For static data, this is another array which's first element is a number representing the data type (
        # string, integer etc.) and the value.
        self.inputs = inputs

        # Block fields are json objects, often used for dropdown menus or other types of fields. In a dropdown menu,
        # the format is {field name: [field value, optional id for value]}
        self.fields = fields

        # This boolean determines if this block it at the top of its stack, or if it is hooked onto another block.
        # top level blocks won't run unless attached to an event type block.
        self.is_top = False

        # Some blocks, like control loops, can be a nest for other blocks. This boolean determines if this block is a
        # nest that contains other blocks or nests.
        self.is_nest = False

        # Some blocks, like if/else, have two 'substacks' in their nest. This boolean determines if the block has a
        # second nest. This can only be true if there is a first.
        self.has_nest2 = False

        # These two lists contain the Block objects for any blocks nested in this block. Nest2 should be none unless
        # has_nest2 is true.
        self.nest = None
        self.nest2 = None

        # In most blocks accepting parameters, the parameter name is different every time. Sometimes the name is NUM,
        # or sometimes if there are two parameters, the names are NUM1 and NUM2. Because the names are inconsistent,
        # this value holds the format for the parameter names. The format for single parameters is just 'NAME'. For
        # multiple, it is 'NAME' (which becomes NAME1, NAME2, ...) OR 'FIRST/SECOND' (which directly becomes FIRST,
        # SECOND).
        self.override_operand_name = None

        # When a block's parameter is a boolean or a variable, the format for self.inputs is a bit different. This lets
        # the block have a custom input format.
        self.override_input = []


class Scratch:
    """The Scratch object is responsible for managing the formatting, conversion, and creation of every block created.
    There should only be one Scratch object used per project."""

    def __init__(self):
        # Here are some constants that make input data types easier to remember.
        self.number = 4
        self.positive_number = 5
        self.positive_integer = 6
        self.integer = 7
        self.angle = 8
        self.color = 9
        self.string = 10
        self.broadcast = 11
        self.variable = 12
        self.list = 13

        # These variable get incremented every time their corresponding value is used. This is useful for block id,
        # where every id must be unique, because it makes them more readable.
        self.id_counter = 0
        self.stack_counter = 0
        self.variable_counter = 0

        # Load the json file with an empty project, that can be modified and saved with this program.
        self.project = json.loads(open("./Base/base.json").read())

        # This dictionary contains a map of all the variables used, where that can be formatted and put in the top of
        # the project.json file where they are stored.
        self.variables = {}

    """
    The format for a block creation function is like this for blocks with single parameters:
    ```
    def block_name(self, param):
        opcode = "category_opcode"
        paramtypes = [self.param_datatype]
        paramcategories = [1]
        return self.process_operator_single(opcode, paramtypes, paramcategories, param, "param_name")
    ```
    like this for block with multiple parameters:
    ```
    def block_name(self, param1, param2):
        opcode = "category_opcode"
        paramtypes = [self.param1_datatype, self.param2_datatype]
        paramcategories = [1, 1]
        
        return self.process_operator(opcode, paramtypes, paramcategories, param1, param2, "param_name_format")
    ```
    and like this for block with no parameters:
    ```
    def blockname(self):
        opcode = "category_opcode"
        block = self.generate(opcode, [], [])
        return block
    ```  
    Additionally, `block.is_top = True` can be added to event blocks.
    """

    ######################
    # Events
    ######################

    def greenflag(self):
        """
        :return: A Scratch Block for an On Green Flag Press block.
        """
        opcode = "event_whenflagclicked"
        block = self.generate(opcode, [], [])
        block.is_top = True
        return block

    ######################
    # Motion
    ######################

    def movesteps(self, steps):
        """
        Make the sprite take a number of steps forward.
        :param steps: The number of steps to walk.
        :return: A Scratch Block for a Move Steps block.
        """
        opcode = "motion_movesteps"
        paramtypes = [self.number]
        paramcategories = [1]
        return self.process_params_single(opcode, paramtypes, paramcategories, steps, "steps")

    def turnright(self, degrees):
        """
        Rotato the sprite clockwise.
        :param degrees: The measure of degrees to turn clockwise.
        :return: A Scratch Block for a Turn Right block.
        """
        opcode = "motion_turnright"
        paramtypes = [self.number]
        paramcategories = [1]
        return self.process_params_single(opcode, paramtypes, paramcategories, degrees, "degrees")

    def turnleft(self, degrees):
        """
        Rotate the sprite counter-clockwise.
        :param degrees: The measure of degrees to turn counter-clockwise.
        :return: A Scratch Block for a Turn Left block.
        """
        opcode = "motion_turnleft"
        paramtypes = [self.number]
        paramcategories = [1]
        return self.process_params_single(opcode, paramtypes, paramcategories, degrees, "degrees")

    def pointindirection(self, direction):
        """
        Point the sprite in a certain direction.
        :param direction: The direction (in degrees) to have the sprite point in
        :return: A Scratch Block for a Point in Direction block.
        """
        opcode = "motion_pointindirection"
        paramtypes = [self.angle]
        paramcategories = [1]
        return self.process_params_single(opcode, paramtypes, paramcategories, direction, "direction")

    ######################
    # Control
    ######################

    def wait(self, seconds):
        """
        Wait a number of seconds before continuing.
        :param seconds: The number of seconds to wait.
        :return: A Scratch Block for a Wait block.
        """
        opcode = "control_wait"
        paramtypes = [self.positive_number]
        paramcategories = [1]
        return self.process_params_single(opcode, paramtypes, paramcategories, seconds, "duration")

    def repeat(self, times, substack):
        """
        Repeat the nested blocks a certain number of times.
        :param times: The number of times to run.
        :param substack: A list of Scratch Blocks to repeat over.
        :return: A Scratch Block for a Repeat block.
        """
        opcode = "control_repeat"
        paramtypes = [self.positive_integer]
        paramcategories = [1]
        return self.process_params_single(opcode, paramtypes, paramcategories, times, "times", nest=substack)

    def forever(self, substack):
        """
        Repeat the nested blocks forever.
        :param substack: A list of Scratch Blocks to run forever.
        :return: A Scratch Block for a Forever block.
        """
        opcode = "control_forever"
        paramtypes = []
        paramcategories = [1]
        return self.generate(opcode, paramtypes, paramcategories, nest=substack)

    def if_(self, condition, substack):
        """
        Only run the nested blocks if `condition` is met.
        :param condition: The condition needed to meet for the blocks in `substack` to run.
        :param substack: A list of blocks to run if the condition is met.
        :return: A Scratch Block for an If block.
        """
        opcode = "control_if"
        paramtypes = [self.variable]
        paramcategories = [2]
        return self.process_params_single(opcode, paramtypes, paramcategories, condition, "condition", nest=substack)

    def if_else(self, condition, substack1, substack2):
        """
        Only run the nested blocks if `condition` is met.
        :param condition: The condition needed to meet for the blocks in `substack` to run, otherwise the blocks in
        `substack2` will be run.
        :param substack1: A list of blocks to run if the condition is met.
        :param substack2 A list of blocks to run if the condition is not met.
        :return: A Scratch Block for an If/Else block.
        """
        opcode = "control_if_else"
        paramtypes = [self.variable]
        paramcategories = [2]
        return self.process_params_single(opcode, paramtypes, paramcategories, condition, "condition", nest=substack1,
                                          nest2=substack2)

    def wait_until(self, condition):
        """
        Do not continue until `condition` is met.
        :param condition: A boolean block, that when met, lets the program continue.
        :return: A Scratch Block for a Wait Until block.
        """
        opcode = "control_wait_until"
        paramtypes = [self.variable]
        paramcategories = [2]
        return self.process_params_single(opcode, paramtypes, paramcategories, [condition], "condition")

    def repeat_until(self, condition, substack):
        """
        Loop over the blocks in `substack` until `condition` is met.
        :param condition: A boolean block, that when met, will cause the block in `substack` to stop repeating.
        :param substack: A list of blocks to loop over until `condition` is met.
        :return: A Scratch Block for a Repeat Until block.
        """
        opcode = "control_repeat_until"
        paramtypes = [self.variable]
        paramcategories = [2]
        return self.process_params_single(opcode, paramtypes, paramcategories, [condition], "condition", nest=substack)

    def stop(self, stop_type):
        """
        Stop a specified portion of the program.
        :param stop_type: One of:
        * 'all'
        * 'this script'
        * 'other scripts in sprite'
        :return: A Scratch Block for a Stop block.
        """
        opcode = "control_stop"
        return self.generate(opcode, [], [], fields={"STOP_OPTION": [stop_type, None]})

    ######################
    # Operators
    ######################

    def lessthan(self, a, b):
        """
        A boolean block that will value true if `a` is less than `b`.
        :param a: A number.
        :param b: A number.
        :return: A Scratch Block for a Less Than boolean.
        """
        opcode = "operator_lt"
        paramtypes = [self.number, self.number]
        paramcategories = [1, 1]

        return self.process_params(opcode, paramtypes, paramcategories, a, b, "OPERAND")

    def greaterthan(self, a, b):
        """
        A boolean block that will value true if `a` is greater than `b`.
        :param a: A number.
        :param b: A number.
        :return: A Scratch Block for a Greater Than boolean.
        """
        opcode = "operator_gt"
        paramtypes = [self.number, self.number]
        paramcategories = [1, 1]

        return self.process_params(opcode, paramtypes, paramcategories, a, b, "OPERAND")

    def equals(self, a, b):
        """
        A boolean block that will value true if `a` is exactly the same as `b`.
        :param a: A number.
        :param b: A number.
        :return: A Scratch Block for an Equals boolean.
        """
        opcode = "operator_equals"
        paramtypes = [self.number, self.number]
        paramcategories = [1, 1]

        return self.process_params(opcode, paramtypes, paramcategories, a, b, "OPERAND")

    def and_(self, a, b):
        """
        A boolean block that will value true if boolean `a` and `b` are both met.
        :param a: Another boolean.
        :param b: Another boolean.
        :return: A Scratch Block for an And boolean.
        """
        opcode = "operator_and"
        paramtypes = [self.variable, self.variable]
        paramcategories = [2, 2]
        return self.process_params(opcode, paramtypes, paramcategories, a, b, "OPERAND")

    def or_(self, a, b):
        """
        A boolean block that will value true if either boolean `a` or `b` are met.
        :param a: Another boolean.
        :param b: Another boolean.
        :return: A Scratch Block for an Or boolean.
        """
        opcode = "operator_or"
        paramtypes = [self.variable, self.variable]
        paramcategories = [2, 2]
        return self.process_params(opcode, paramtypes, paramcategories, a, b, "OPERAND")

    def not_(self, a):
        """
        A boolean block that will value the opposite value of `a`.
        :param a: Another boolean.
        :return: A Scratch Block for a Not boolean.
        """
        opcode = "operator_not"
        paramtypes = [self.variable]
        paramcategories = [2]
        return self.process_params_single(opcode, paramtypes, paramcategories, a, "OPERAND")

    def add(self, a, b):
        """
        Finds the sum of two values.
        :param a: One addend.
        :param b: Another addend.
        :return: A Scratch Block for an Add operator.
        """
        opcode = "operator_add"
        paramtypes = [self.number, self.number]
        paramcategories = [1, 1]
        return self.process_params(opcode, paramtypes, paramcategories, a, b, "NUM")

    def subtract(self, a, b):
        """
        Finds the difference of two values.
        :param a: The minuend.
        :param b: The subtrahend.
        :return: A Scratch Block for a Subtraction operator.
        """
        opcode = "operator_subtract"
        paramtypes = [self.number, self.number]
        paramcategories = [1, 1]
        return self.process_params(opcode, paramtypes, paramcategories, a, b, "NUM")

    def multiply(self, a, b):
        """
        Finds the product of two values.
        :param a: One factor.
        :param b: Another factor.
        :return: A Scratch Block for a Multiplication operator.
        """
        opcode = "operator_multiply"
        paramtypes = [self.number, self.number]
        paramcategories = [1, 1]
        return self.process_params(opcode, paramtypes, paramcategories, a, b, "NUM")

    def divide(self, a, b):
        """
        Finds the quotient of two values.
        :param a: The dividend.
        :param b: The divisor.
        :return: A Scratch Block for a Division operator.
        """
        opcode = "operator_divide"
        paramtypes = [self.number, self.number]
        paramcategories = [1, 1]
        return self.process_params(opcode, paramtypes, paramcategories, a, b, "NUM")

    def random(self, a, b):
        """
        Chooses a random integer in the range of `a` to `b`.
        :param a: Minimum result.
        :param b: Maximum result.
        :return: A Scratch Block for a random parameter.
        """
        opcode = "operator_random"
        paramtypes = [self.number, self.number]
        paramcategories = [1, 1]
        return self.process_params(opcode, paramtypes, paramcategories, a, b, "-from/to")

    def mod(self, a, b):
        """
        Finds the remeainder when `a` and `b` are divided.
        :param a: The dividend.
        :param b: The divisor.
        :return: A Scratch Block for a parameter valuing the remainder.
        """
        opcode = "operator_mod"
        paramtypes = [self.number, self.number]
        paramcategories = [1, 1]
        return self.process_params(opcode, paramtypes, paramcategories, a, b, "NUM")

    def round(self, a):
        """
        Rounds `a` to the nearest whole number.
        :param a: A number
        :return: A Scratch Block for a Round operator.
        """
        opcode = "operator_round"
        paramtypes = [self.number]
        paramcategories = [1]
        return self.process_params_single(opcode, paramtypes, paramcategories, a, "NUM")

    def mathop(self, a, op_type):
        """
        Computes a special math operation on 'a'.
        :param a: A number
        :param op_type: One of:
        * 'abs'
        * 'floor'
        * 'ceiling'
        * 'sqrt'
        * 'sin'
        * 'cos'
        * 'tan'
        * 'asin'
        * 'acos'
        * 'atan'
        * 'ln'
        * 'e ^'
        * '10 ^'
        :return: A Scratch Block for a special operator parameter.
        """
        opcode = "operator_mathop"
        paramtypes = [self.number]
        paramcategories = [1]
        fields = {"OPERATOR": [op_type, None]}
        return self.process_params_single(opcode, paramtypes, paramcategories, a, "NUM", fields)

    def join(self, a, b):
        """
        Concatenates two strings
        :param a: Prefix string.
        :param b: Suffix string.
        :return: A Scratch Block for a Join operator.
        """
        opcode = "operator_join"
        paramtypes = [self.string, self.string]
        paramcategories = [1, 1]
        return self.process_params(opcode, paramtypes, paramcategories, a, b, "STRING")

    def letter_of(self, letter, string):
        """
        Finds the nth letter of `string`.
        :param letter: The index.
        :param string: The sliced string.
        :return: A Scratch Block for a Letter Of operator.
        """
        opcode = "operator_letter_of"
        paramtypes = [self.number, self.string]
        paramcategories = [1, 1]
        return self.process_params(opcode, paramtypes, paramcategories, letter, string, "-letter/string")

    def length(self, a):
        """
        Finds the length of a string.
        :param a: The in string.
        :return: A Scratch Block for a parameter valuing the length of `a`.
        """
        opcode = "operator_length"
        paramtypes = [self.string]
        paramcategories = [1]
        return self.process_params_single(opcode, paramtypes, paramcategories, a, "STRING")

    def contains(self, string, searchterm):
        """
        A boolean block that will value true if `searchterm` can be found within `string`.
        :param string: A string.
        :param searchterm: A string to look for within the other string.
        :return: A Scratch Block for a Contains boolean.
        """
        opcode = "operator_contains"
        paramtypes = [self.string, self.string]
        paramcategories = [1, 1]
        return self.process_params(opcode, paramtypes, paramcategories, string, searchterm, "STRING")

    ######################
    # Data
    ######################

    def variable_(self, variable_name):
        """
        Get a certain variable.
        :param variable_name: The name of the variable to get.
        :return: A list representing the variable in question.
        """
        return [12, variable_name, str(self.get_variable(variable_name)) + "-" + variable_name]

    def setvariableto(self, variable_name, value):
        """
        Sets a certain variable's value.
        :param variable_name: The name of the variable to set to a value.
        :param value: The new value of the variable.
        :return: A Scratch Block for a Set Variable To block.
        """
        opcode = "data_setvariableto"
        paramtypes = [self.string]
        paramcategories = [1]
        fields = {"VARIABLE": [variable_name, self.get_variable(variable_name)]}
        return self.process_params_single(opcode, paramtypes, paramcategories, value, "VALUE", fields)

    def changevariableby(self, variable_name, value):
        """
        Increments a certain variable by a certain amount.
        :param variable_name: The name of the variable to increment.
        :param value: The number to increment the variable by.
        :return: A Scratch Block for a Change Variable By block.
        """
        opcode = "data_changevariableby"
        paramtypes = [self.string]
        paramcategories = [1]
        fields = {"VARIABLE": [variable_name, self.get_variable(variable_name)]}
        return self.process_params_single(opcode, paramtypes, paramcategories, value, "VALUE", fields)

    ######################
    # Utilities
    ######################

    def get_variable(self, variable_name):
        """
        This function will return the variable id for the given `variable_name`.
        :param variable_name: The name of the variable to get the id of.
        :return: The id of the variable.
        """
        for variable_id in self.variables.keys():
            if variable_id.endswith(variable_name):  # We use endswith because the variable format is `number-name`
                return self.variables[variable_id]

        # If that didn't work, we create the variable and try again
        self.new_variable(variable_name, 0)
        return self.get_variable(variable_name)

    def new_variable(self, variable_name, value):
        """ This function generates a variable id and adds it to the variable list. Variable format is
        `uniquenumber-name`.
        :param variable_name: The name for the new variable.
        :param value: The initial value for the new variable.
        :return:
        """
        self.variables[str(self.variable_counter) + "-" + variable_name] = value
        self.variable_counter += 1

    def generate(self, opcode, paramtypes, paramcategories, **kwargs):
        """
        This function creates a block object out of all the data a block might need.
        :param opcode: The scratch code string for the block.
        :param paramtypes: A list of possible parameter type ids for the block.
        :param paramcategories: A list of possible parameter category ids for the block.
        :param kwargs: Key-value pairs for block attributes.
        :return: A Scratch Block for the supplied attributes.
        """

        # Because parameters are supplied as keyword args, we receive them here.
        params = dict(locals()['kwargs'])

        # The block will need a unique id, we have a counter for that, take the latest value.
        tmp_id = self.id_counter

        # Create a Block object with only an id and opcode, we update the rest of the data below.
        new_block = Block(tmp_id, opcode, {}, {})

        # Loop over all the block's parameters, and give ourselves a counter to know the index of the current parameter.
        for arg_name, param, counter in zip(params.keys(), params.values(), range(len(params))):
            if arg_name == "fields":
                # We have been given pre-formatted fields. We can assign them directly to the block.
                new_block.fields = param
            elif arg_name == "nest":
                # If we get 'nest' as our parameter name, it means this block nests other blocks, and `param` is a list
                # of the Block objects for those blocks. We will assign them to the blocks nest attribute and update
                # is_nest to reflect.
                new_block.nest = param
                new_block.is_nest = True
            elif arg_name == "nest2":
                # Same thing as above, but for if the object holds a second nest.
                new_block.nest2 = param
                new_block.has_nest2 = True
            elif paramtypes[counter] == self.variable:
                # We have gotten a parameter that doesn't follow the usual {name: [type,value]} format. This means it
                # might be a boolean or variable.
                new_block.override_input.append(param)
            else:
                # Otherwise, we have a plain parameter. We add an entry to the 'inputs' dictionary with the uppercase
                # arg_name, and the rest of data formatted properly as the value.
                new_block.inputs[str(arg_name).upper()] = [paramcategories[counter], [paramtypes[counter], str(param)]]

        # Update the unique id counter.
        self.id_counter += 1

        return new_block

    def process_params_single(self, opcode, paramtypes, paramcategories, a, operand_name, fields=None, nest=None,
                              nest2=None):
        """
        Blocks with a single parameter can easily call this function with their construction function to make
        processing parameters simple.
        :param opcode: The scratch code string for the block.
        :param paramtypes: A list of possible parameter type ids for the block.
        :param paramcategories: A list of possible parameter category ids for the block.
        :param a: The parameter for the block.
        :param operand_name: The name to put as the key in json attributes of the block.
        :param fields: Attributes for the json fields of the block.
        :param nest: A list of Scratch Blocks under this block.
        :param nest2: Another list of Scratch Blocks under this block.
        :return: A Scratch Block for the supplied attributes.
        """
        # Initialize the parameter format override as none, because it might not get used later.
        override_name = None

        if type(a) == list:
            # If we receive a list as a parameter, we are not receiving a value but instead a reference to another
            # block. If that happens, we override the parameter types and category to signify we now are using a block
            # reference for value.
            paramtypes = [self.variable]
            paramcategories = [2]  # Category 2 means block id reference.
            override_name = operand_name  # We then apply the input format override.

        # This dictionary will be passed as keyword args for the generate function. We will pass through the parameter.
        kwargs = {operand_name: a}

        # If any special attributes are defined, we pass them through.
        if fields is not None:
            kwargs["fields"] = fields
        if nest is not None:
            kwargs["nest"] = nest
        if nest2 is not None:
            kwargs["nest2"] = nest2

        # Now, we use generate to create a blck with add our data.

        block = self.generate(opcode, paramtypes, paramcategories, **kwargs)

        # Sometimes operators will have only one operand as another operator. This makes the compiler script think that
        # there is a single operand, and it should be just 'OPERAND' and not 'OPERAND1'. This overrides that behavior.
        if override_name is not None:
            block.override_operand_name = override_name.upper()

        return block

    def process_params(self, opcode, paramtypes, paramcategories, a, b, operand_name, fields=None, nest=None,
                       nest2=None):
        """
        Blocks with a multiple parameters can easily call this function with their construction function to make
        processing parameters simple.
        :param opcode: The scratch code string for the block.
        :param paramtypes: A list of possible parameter type ids for the block.
        :param paramcategories: A list of possible parameter category ids for the block.
        :param a: The first parameter for the block.
        :param b: The second parameter for the block.
        :param operand_name: The name to put as the key in json attributes of the block.
        Will result as `operand_name1, operande_name2`, unless `operand_name` has a slash, which would make
        it become `string_before_slash, string_after_slash`.
        :param fields: Attributes for the json fields of the block.
        :param nest: A list of Scratch Blocks under this block.
        :param nest2: Another list of Scratch Blocks under this block.
        :return: A Scratch Block for the supplied attributes.
        """

        # Initialize the parameter format override as none, because it might not get used later.
        override_name = None

        # This dictionary will be passed as keyword args for the generate function.
        kwargs = {}

        if operand_name.upper().startswith("-"):
            # We have a custom format for the operand names. We can parse it and assign it to 'names'.
            names = operand_name.upper()[1:].split("/")

            # If we receive a list as a parameter, we are not receiving a value but instead a reference to another
            # block. If that happens, we override the parameter types and category to signify we now are using a block
            # reference for value.
            if type(a) == list:
                paramtypes = [self.variable, paramtypes[1]]
                paramcategories = [2, paramcategories[1]]
                override_name = names[0]

            # Same thing as above but for parameter b
            if type(b) == list:
                paramtypes = [paramtypes[0], self.variable]
                paramcategories = [paramcategories[0], 2]
                override_name = names[1]

            # Pass though the parameters to kwargs
            kwargs[names[0]] = a
            kwargs[names[1]] = b

            # If any special attributes are defined, we pass them through.
            if fields is not None:
                kwargs["fields"] = fields
            if nest is not None:
                kwargs["nest"] = nest
            if nest2 is not None:
                kwargs["nest2"] = nest2

        else:
            # If the format for operand names is normal, we just do this.

            # If we receive a list as a parameter, we are not receiving a value but instead a reference to another
            # block. If that happens, we override the parameter types and category to signify we now are using a block
            # reference for value.
            if type(a) == list:
                paramtypes = [self.variable, paramtypes[1]]
                paramcategories = [2, paramcategories[1]]
                override_name = operand_name + "1"

            # Same thing as above but for parameter b
            if type(b) == list:
                paramtypes = [paramtypes[0], self.variable]
                paramcategories = [paramcategories[0], 2]
                override_name = operand_name + "2"

            # Pass though the parameters to kwargs but with identifying numbers at the end of the names.
            kwargs[operand_name.upper() + "1"] = a
            kwargs[operand_name.upper() + "2"] = b

            # If any special attributes are defined, we pass them through.
            if fields is not None:
                kwargs["fields"] = fields
            if nest is not None:
                kwargs["nest"] = nest
            if nest2 is not None:
                kwargs["nest2"] = nest2

        # Now, we use generate to create a blck with add our data.
        block = self.generate(opcode, paramtypes, paramcategories, **kwargs)

        # Sometimes operators will have only one operand as another operator. This makes the compiler script think that
        # there is a single operand, and it should be just 'OPERAND' and not 'OPERAND1'. This overrides that behavior.
        if override_name is not None:
            block.override_operand_name = override_name

        return block

    def stack(self, stack):
        """
        Take att the Scratch data and format it to json that is readable by the Scratch GUI.
        :param stack: A list of Scratch Blocks.
        :return: the id of the first block in the stack.
        """
        # We will keep track of the first block, so we can return its id.
        first_id = None

        # We will also keep track of the latest, or previous block, in the loop below.
        latest_block = None

        # Loop over the length of the stack
        for i in range(len(stack)):
            if stack[0] == 12:
                # If we get 12 as the stack's first value, Then 'stack' not a stack, but a variable reference that
                # looks like one. We just return that directly.
                return [3, stack]

            # Otherwise, we continue as normal. We make `block` become the reference to the current block we are
            # formatting.
            block = stack[i]

            # If the block is a nest, then we recursively stack the 'substack's.
            if block.is_nest:
                block.inputs["SUBSTACK"] = self.stack(block.nest)
            if block.has_nest2:
                block.inputs["SUBSTACK2"] = self.stack(block.nest2)

            block_id = str(block.block_id)

            # Block inputs won't be automatically added, so we do it here.
            if block.override_input:
                if block.override_operand_name is not None:
                    # If we have an override parameter set, then we recursively stack the input, and assign the returned
                    # value to the json object, using the custom overridden name.
                    block.inputs[block.override_operand_name] = self.stack(block.override_input[0])

                elif len(block.override_input) > 0:
                    try:
                        # If we have custom input format (for booleans and variables), we attempt to use that possible
                        # Boolean's format directly in the json object like this. We take the first item because the
                        # boolean should just be wrapped in a list.
                        block.inputs["CONDITION"] = self.stack(block.override_input[0])

                    except TypeError:
                        # If that fails, then the operand is probably a variable. and we take the direct override and
                        # apply it to the json object.
                        block.inputs["OPERAND"] = self.stack(block.override_input)

            # On first loop keep track of the block, so we can return it later.
            if i == 0:
                first_id = block_id

            # Find the next block in the stack array. Make it none if we are out of array bounds. This will also apply
            # to the json.
            try:
                next_block = stack[i + 1].block_id
            except IndexError:
                next_block = None

            #  Allocate space in the json file for this block
            block_section = self.project["targets"][1]["blocks"]
            block_section.update({block_id: {}})

            # Apply the attributes from the block to json
            block_section[block_id].update({"opcode": block.opcode})

            # Apply relations
            block_section[block_id].update({"next": str(next_block)})
            block_section[block_id].update({"parent": str(latest_block)})  # Latest_block will default as None.

            # First_stack_loops is the same, even in recursive calls. It will be set to true ont the first block call.
            block_section[block_id].update({"topLevel": block.is_top})
            if block.is_top:
                block_section[block_id].update({"x": 50})
                block_section[block_id].update({"y": 50})

            block_section[block_id].update({"shadow": False})

            # Finally, apply inputs and fields.
            block_section[block_id].update({"inputs": dict(block.inputs)})
            block_section[block_id].update({"fields": dict(block.fields)})
            latest_block = block.block_id
        return [2, str(first_id)]

    def process_data(self):
        """
        In the top of the project.json file, variables are stores. This makes sure the variables we were tracking
        makes it there.
        """

        # Find the place in the json to put these
        var_section = self.project["targets"][0]["variables"]

        # Loop over the stored variables  and format then add them to the json.
        for var_id, value in zip(self.variables.keys(), self.variables.values()):
            var_name = var_id.split("-")[1]
            var_section.update({var_id: [str(var_name), value]})

    def compile(self):
        """
        Compiles all the json and dependencies to a .SB3 file.
        :return: the JSON for `project.json`.
        """
        # Make sure the variables are included
        self.process_data()

        # Create a zip file and write the main json to a file
        zip_obj = ZipFile('./Project.sb3', 'w')
        open("./Project/project.json", "w+").write(json.dumps(self.project))

        # Add the project json and any other assets the user put into ./Project
        for file in os.listdir("./Project"):
            zip_obj.write("./Project/" + file)

        # The default assets
        zip_obj.write('./Base/0fb9be3e8397c983338cb71dc84d0b25.svg')
        zip_obj.write('./Base/bcf454acf82e4504149f7ffe07081dbc.svg')
        zip_obj.write('./Base/cd21514d0531fdffb22204e0ec5ed84a.svg')
        zip_obj.write('./Base/83a9787d4cb6f3b7632b4ddfebf74367.wav')
        zip_obj.write('./Base/83c36d806dc92327b9e7049a565c6bff.wav')

        zip_obj.close()
        return self.project
