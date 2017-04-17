#include <stdio.h>

// returns x % y
int mod(int x, int y){
    return x - ((x/y) * y);
}

// returns whether or not a number is prime
bool isPrime(int x){
    if(x <= 1)
        return false;
    
    for(int i = 2; i < x/2; i++)
        if(mod(x, i) == 0)
            return false;   
   
    return true;    
}

int main(){
    int count = 0;
    int odds = 0;
    int primes = 0;
    int i = 100;

    while( true ){
        i--;
        count++;
        
        if(i <= 0)
            break;
       
        if(isPrime(count))
            primes++;
       
        if(mod(count, 2) == 0)
            continue;
        odds++;
    }        
    // count = 100
    // odds = 50
    // primes = 27
    // i = 0
}
