// Currently, there is only support for single line comments

// Variables can be set like this. Note that any parameter must be surrounded by parenthesis.
set (health) to (10)

// Blocks are typed as they are seen in Scratch
move (10) steps // Just remember to use parentheses for values.

// You can also put variables anywhere
move (health) steps

// You can even call an undefined variable and it will start at 0
move (my variable) steps // Note that the parser ignores spaces, so the variable will become 'myvariable'

// Loops are made with brackets
repeat (2) {
    // Indentation is not required but it is good for visibility.
    turn right (-5) degrees
}

// If-else statement use two sets of brackets
if ((2) equals (2)) then {
    turn right (1) degrees
} else {
    turn left (1) degrees
}

// Loops can be stacked infinitely
repeat(2) {
    repeat(2) {
        repeat(2) {
            turn right (4) degrees
        }
    }
}

// So can operators
turn left (add (add (add (add (add (add (1) and (1)) and (1)) and (1)) and (1)) and (1)) and (1)) degrees

// Dropdown blocks need to have their value explicitly stated
stop ("all")  // Strings still need parenthesis.