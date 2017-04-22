#include <stdio.h>

int global_x;

void set_global_x(int x){
    global_x = x;
    return;
}

int square(int x){
    return x * x;
}

float invProd(float x, float y){
    return x + y - x * y;
}

bool isEven(int x){
    return (x/2 == 0);
}

int main(){
    int a, *b, c = 10, d = 10 + 10, e = c + d, f[];
    
    float u, *v, w = 10.0, x = 10.0 * 2.0, y = w + x, z[];
    
    bool wrong = false, right = true;

    char character = 'c';
    
    10;    
    square(10);
    square(a);
    set_global_x(100);
    a = square(10);
    b = &a;   
    *(&u) = invProd(w, x);
    
    if(10 < 20 && 100 > 50 || 10.0 == 10.0 && 'a' <= 'b')
        if(40 >= 30 && 60 != 50)
            printf("Yes!\n");
        if(!right)
            printf("No!\n");
        else
            printf("Yes!\n");
            
    {
        int i = 1000, j = 0;
        while(i > 0){
            i--;
            --i;
            j++;
            ++j;
            j += 1;
            i -= j;    
            j *= 3;
            j /= 2;    
        }
    }
    
    {
        int a = 1, b = 2, c = 3, d = 4;
        a = b + c / d * a - a;
        float x = 1.0, y = 2.0, z = 3.0;
        x = x * y + z - x / z;
    }
    
    int k;
    for(int i=10;i>0;i--){
        if(isEven(i))
            continue;
        k += i;
        if(i == 3)
            break;
    }

    const char text[] = "abcdefg";
    printf(text);
}



















