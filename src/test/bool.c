#include <stdio.h>

int main(){
    bool t_, f_, a, b, c, d, e, f;
    t_ = true;          // t_ = true
    f_ = false;         // f_ = false
    
    a = true || t_;     // a = true
    b = true && t_;     // b = true
    c = false || t_;    // c = true
    d = true && f_;     // d = false
    e = !true;          // e = false
    f = !(!(true && false) && (a && (!b || !d)));   // f = false
}
