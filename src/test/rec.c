#include <stdio.h>

int main(int argc){
    if(argc > 0){
        int a = argc * main(argc - 1);
        printf("%i\n", a);
        return a;
    }
    return 1;
}
