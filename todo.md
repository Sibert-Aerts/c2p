# To do

## Language

6. **Functions**
    1. (optional) Check whether all paths in a function body end with a return statement (not required for procedures that return `void`).

7. **Arrays**
    1. (optional) assignments of complete arrays or array rows in case of multi-dimensional arrays.
    1. (optional) dynamic arrays.

## Target Language: P

* Initialization of variables without initializer. Obviously this has a negative effect on performance, especially with arrays, which is why initialization is usually performed dynamically in a loop. Hence, it is possible, as optional optimization, not to implement default initialization of array elements and generate a warning when an array is read from before its elements have been initialized. Note that a warning should be generated for variables which are initialized with themselves.


## Optimisations

Apart from correctness, some attention can be paid to the performance of your compiler, e.g. the runtime performance of the generated stack machine program, or the size of your target code in terms of primitive P instructions. Through static evaluation of constants, you can already obtain a large speedup. Apart from that, you might implement diverse “peephole optimisations”. Such optimisations are optional; if you add any, do remember to carefully document which optimisations you developed and elaborate on the rationale.
