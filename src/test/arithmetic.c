#include <stdio.h>

int main(){
    int a, b, c, d, e, f;
    float u, v, w, x, y, z;
        
    // ints
    a = 10;             // a = 10
    b = a + 10;         // b = 20
    c = b + b - 10;     // c = 30
    d = a * 4;          // d = 40
    e = (a * a) / 2;    // e = 50
    f =  (((2 * a) + b + - c + e) * d) / ( b * 2 ); // f = 60
        
    // floats
    u = 0.125;              // u = 0.125
    v = u + 0.125;          // v = 0.250
    w = v + v - 0.125;      // w = 0.375
    x = (v * v) * 8.0;      // x = 0.500
    y = (x * 5.0) / 4.0;    // y = 0.615
    z = (x * x * x) + (w - u) * 2.0 + y - (1.0 / 2.0);    // z = 0.750 
    
    // TODO: add mixed int/float compatibility & tests
}
