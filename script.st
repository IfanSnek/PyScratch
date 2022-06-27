def run (rot) and jump (times) {
   move (times) steps
   turn right (subtract (add (times) to (rot)) from (times)) degrees
}

forever {
run and jump (10) (2)
}