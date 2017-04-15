#include <stdio.h>

int main(){
    int a = 10;
    int *b = &a;    // b = 14* (changes with code)
    int c = *b;     // c = 10
    *b = 20;        // a = 20
}
