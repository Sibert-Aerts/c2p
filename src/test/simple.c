#include <stdio.h>

int x = 10;

int c(int r){
    int d;
    x = r;
}

int main(){
    float c;
    int y;
    y = 20;
    c = 3.14;
    
    int z = y;
    int q = z + 10;
    float flub = 10.0 - 1.5;
    z = q + q + z;
    {
        int q = z;
    }
    {
        float c = 13.37;
    }
}
