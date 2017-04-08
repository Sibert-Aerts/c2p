#include <stdio.h>

int main(){
    int x[10], y = 10, z = 20;
    y = (z = 30);
    printf("%i\n", y);
}
