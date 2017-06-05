for test in arithmetic array assignment bool call cast default_init demotion everything expressions for for_all if loop pointers printf promotion rec simple string var_scopes while
do
    echo ---------------- Compiling $test ----------------
    if python3 main.py test/${test}.c -w
    then
        echo ---------------- Executing $test ----------------
        ./Pmachine code.p
        echo ---------------- Completed $test ----------------
    else
        echo ----------------- Failed $test ------------------    
    fi
    echo
    echo
done
