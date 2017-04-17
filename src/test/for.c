#include <stdio.h>

int main(){
    int total1 = 0, total2 = 0;
    
    // total1 = 55
    for(int i = 1; i <= 10; i++)
        total1 += i;
    
    // total2 = 55
    int i = 1;
    for(;;)
    {
        if(!(i <= 10))
            break;
        total2 += i++;
    }    
}
