#include <stdio.h>

int main(){
    int a, b, c;
    float x, y, z;
    char j, k, l;
    
    // regular casting
    
    a = (int)100;       // a = 100
    b = (int)100.0;     // b = 100
    c = (int)'d';       // c = 100
    
    x = (float)100.0;   // x = 100.0
    y = (float)100;     // y = 100.0
    z = (float)'d';     // z = 100.0
    
    j = (char)'d';      // j = 'd'
    k = (char)100;      // k = 'd'
    l = (char)100.0;    // l = 'd'
    
    // pointer casting and arithmetic (UB)
    
    int one = (int)&b - (int)&a;    // one = 1
    int c2 = *(int *)((int)&a + 2); // c2 = c = 100
    
}
