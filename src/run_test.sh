for test in arithmetic array assignment bool call cast default_init everything expressions for for_all if loop pointers printf promotion rec simple string var_scopes while
do
    echo ---------------- Compiling $test ----------------
    python3 main.py test/${test}.c
    echo ---------------- Executing $test ----------------
    ./Pmachine code.p
    echo ---------------- Completed $test ----------------
    echo
    echo
done
