ldc a 0
ldc a 0
ldc a 0
ldc a 0
ldc a 0
ldc a 0
ldc i 4
new
ldc c 97
sro c -4
ldc c 98
sro c -3
ldc c 99
sro c -2
ldc c 0
sro c -1
mst 0
cup 0 f_main
hlt
f_main:
ldc a -4
printf_loop:
dpl a
ind c
dpl c
ldc c 0
neq c
fjp printf_done
out c
inc a 1
ujp printf_loop
printf_done:
dpl c
equ c
fjp printf_done
dpl a
equ a
fjp printf_done
ldc i 0
retf
hlt
