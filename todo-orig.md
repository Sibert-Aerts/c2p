# To do

## Language

1. **Types (mandatory)**  
Minimally, there should be support for the primitive data types `char`, `float`, `int`, and pointer types.

2. **Import (mandatory)**  
The import of stdio should be supported (`#include <stdio.h>`).  
Furthermore, only the functions `int printf(char *format, ...)` and `int scanf(const char *format, ...)` must be supported, as defined in [11]: the format string allows interpretation of sequences of the form `%[width][code]` (width only in case of output). Provide support for at least for the type codes `d`, `i`, `s` and `c`. You may consider the `char*` types to be `char` arrays. Flags and modifiers, as described in [14], do not need to be supported.  
The behavior of scanf is well documented in the man pages [15, 10].

3. **Reserved words (mandatory)**  
Minimally `if`, `else`, `return` and `while` must be supported, next to the types `char`, `int`, `float` and `void`.

  1. (optional) `for`.
  1. (optional) `const`.
  1. (optional) `break`.
  1. (optional) `continue`.

  If you want to go beyond these, a full list can be found in [2, 16].

4. **Local and global variables (mandatory)**

5. **Comments (mandatory)**  
Support for single line (and multi-line) comments.

6. **Functions (mandatory)**  
This feature is mandatory and entails the definition and calling of functions and procedures, including support for passing parameters of basic types by value as well as by reference (pointers). Moreover, consistency of a return statement with the type of the enclosing function must be checked. You should also verify consistency between forward declarations and function definition signatures. 
  1. (optional) Check whether all paths in a function body end with a return statement (not required for procedures that return `void`).

7. **Arrays (mandatory)**  
Array variables should be supported, as well as operations on individual array elements. Mind the correct use of dimensions and indices. Support for 1-dimensional static arrays is a mandatory feature; support for multi-dimensional arrays is optional, as well as dynamic arrays and assignments of complete arrays or array rows.
  1. (optional) multi-dimensional arrays.
  1. (optional) assignments of complete arrays or array rows in case of multi-dimensional arrays.
  1. (optional) dynamic arrays.
  
8. **Conversions** (optional)  
As a first extension you can support implicit conversions. Consider the following order on the basic types: `float isRicherThan int isRicherThan char`  
Implicit conversions of a richer to a poorer type (e.g. assignment of an int to a char variable) should cause a warning indicating possible loss of information. Another extension could be support for explicit casts (i.e. the cast operator). This enables the programmer to indicate he is aware of possible information loss. Hence the compiler should not yield a warning anymore.



## Error Analysis

The compiler is allowed to stop when it encounters a syntax error. An indication of the location of the syntax error should be displayed, but diagnostic information about the type of error is optional (and non-trivial). For semantical errors, it is necessary to output more specific information about the encountered error. For example, for usage of a variable of the wrong type, you might output: “[ Error ] line 54, position 13: variable x has type y while it should be z”. When in doubt, the Gnu C Compiler [6] with options `ansi` and `pedantic` is the reference.


## Target Language: P

This language is the machine language of the virtual P stack machine from the course material, augmented with input, output and halt instructions. Documentation on this stack machine, as well as executables, can be found on the compilers website [1]. Remarks for code generation from C to P:

* Initialization of variables without initializer. By default, initialize variables without initializer to 0. This is also possible for char. Obviously this has a negative effect on performance, especially with arrays, which is why initialization is usually performed dynamically in a loop. Hence, it is possible, as optional optimization, not to implement default initialization of array elements and generate a warning when an array is read from before its elements have been
initialized. Note that a warning should be generated for variables which are initialized with themselves.

* scanf and strings. For a `scanf("%s", ...)` statement, generate a loop of *in c* instructions. Exit the loop upon reading the escape character (ascii code 27). 


## Optimisations

Apart from correctness, some attention can be paid to the performance of your compiler, e.g. the runtime performance of the generated stack machine program, or the size of your target code in terms of primitive P instructions. Through static evaluation of constants, you can already obtain a large speedup. Apart from that, you might implement diverse “peephole optimisations”. Such optimisations are optional; if you add any, do remember to carefully document which optimisations you developed and elaborate on the rationale.


## AST Visualization

You should construct an explicit AST from the parse tree generated by ANTLR. To show your AST structure, provide a listener or visitor for your AST that prints the tree in the dot format. This way it can be visualized by Graphviz. For a reference on the dot format, see [18].
