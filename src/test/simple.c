#include <stdio.h>

int x = 10;

int c(int r){
    int d;
    x = r;
}

int main(){
    int a = 10, b = 20, c;
    float x = 10.0, y = 20.0, z;
    // c = 230
    c = a + b - a * b / a * -a;
    // z = 230.0
    z = x + y - x * y / x * -x;
    
    {
        int a = 12345;
    }
    
    {
        float x = 5678.9;
    }
}
