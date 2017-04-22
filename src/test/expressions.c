#include <stdio.h>

int square(int x){
    return x * x;
}

int main(){
    int a, b, c, d, e, f;
    
    // Comma
    b = a = 50, 100;  // a = 100, b = 100
    
    // Assignment
    b += 100;           // b = 200    
    a -= 50;            // a = 50
    a *= 2;             // a = 100
    b /= 2;             // b = 100
    
    // Ternary
    c = (10 > 20) ? 50 : 100;   // c = 100
    d = (c == 100) ? d == 0 ? 100 : 50 : -50;   // d = 100
    
    // Call
    e = square(10);     // e = 100
    
    // Combined
    f = (e *= 1), 200; // f = 200
    f *= 2;     // f = 400
    f /= e/100 + (100, 400) / square(20) + 2; 
    // f = 100
}
