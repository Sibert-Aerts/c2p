#include <stdio.h>

char* compare(int a, int b){

    char text[];
    
    if(a<b)
    {
        text = "a is kleiner dan b\n";
    }
    else if (a == b)
    {
        text = "a en b zijn even groot\n";
    } 
    else
    {
        text = "a is groter dan b\n";
    }
    
    return (char *)text;
}

int main(){
    printf(compare(20, 30));    // out: a is kleiner dan b
    printf(compare(30, 20));    // out: a is groter dan b
    printf(compare(20, 20));    // out: a en b zijn even groot
    
    if(10 > 20)                 // (prints nothing)
        printf("10 > 20");
        
    if(10 < 20)                 // out: 10 < 20
        printf("10 < 20");
        
    return 0;
}
