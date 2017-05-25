#include <stdio.h>

bool isPositive(int a){
    if (a < 0)
        return false;
    return true;
}

char* compare(int a, int b){

    char text[];
    
    if(a<b)
    {
        text = "a is smaller than b\n";
    }
    else if (a == b)
    {
        text = "a and b are equal\n";
    } 
    else
    {
        text = "a is larger than b\n";
    }
    
    return (char *)text;
}

int main(){
    printf("%s", compare(20, 30));    // out: a is smaller than b
    printf("%s", compare(30, 20));    // out: a is larger than b
    printf("%s", compare(20, 20));    // out: a and b are equal
            
    // out: 10 is positive
    if(isPositive(10))
        printf("10 is positive\n"); 
        
    // out: -10 is negative
    if(isPositive(-10))
        printf("-10 is positive\n");
    else
        printf("-10 is negative\n");
        
    return 0;
}
