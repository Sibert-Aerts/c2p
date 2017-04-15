#include <stdio.h>

int main(){
    int a, b, c, d, e, f;
    float u, v, w, x , y, z;
    
    a = 100;        // a = 100
    
    b = c = d = e = f = 100;     
    b += 100;       // b = 200    
    c -= 50;        // c = 50
    d *= 2;         // d = 200
    e /= 2;         // e = 50 
    
    f += c;
    f *= d;
    f /= 100;
    f -= 200;       // f = 100
    
    u = 0.5;        // u = 0.5
    
    v = w = x = y = z = 0.5;
    v += 0.5;       // v = 1.0
    w -= 0.25;      // w = 0.25
    x *= 0.5;       // x = 0.25
    y /= 0.5;       // y = 1.0
    
    z += v;
    z -= w + x;
    z *= ((v - x) / w);
    z /= y + x * 4.0 + v;   // z = 1.0
}
