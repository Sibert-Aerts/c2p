for test in arithmetic array assignment bool call cast default_init everything expressions for for_all if loop pointers printf promotion rec simple string var_scopes while
do
    echo RUNNING TEST $test
    python3 main.py test/${test}.c
    ./Pmachine code.p
    echo FINISHED TEST $test
    echo
    echo
done
