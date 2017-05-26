#include <stdio.h>

int assertCount, errorCount;

void assertEq(int x, int y){
    assertCount++; if(x == y) return; errorCount++;
    printf("ASSERTION %d FAILED: %d does not equal %d\n", assertCount, x, y);
}

void endTest(){
    if(errorCount > 0) printf("TEST FAILED: Encountered %d assertion error%s out of %d!", errorCount, errorCount==1?"":"s", assertCount);
    else printf("TEST SUCCESSFUL: All %d assertions passed!", assertCount);
}

// Functions

void method(){
    int x = 10;
    int y = 20;
    int z = x + y;
}

int getter(){
    int x = 10;
    int y = 20;
    return x * y;
}

int function(int x){
    int y = 20;
    return x * y;
}

int mul(int x, int y){
    return x * y;
}

int ten(int x){
    return mul(x, 10);
}

int square(int x){
    return mul(x, x);
}

int sum(int a, int b, int c, int d, int e, int f){
    int total = a + b + c + d + e + f;
    return total;
}


int main(){
    int a = 10;
    method();
    int b = getter();                       // b = 200
    int c = function(a);                    // c = 200
    int d = mul(square(ten(ten(7))), 2);    // d = 980000
    int e = sum(10, 20, 30, 40, 50, 60);    // e = 210
    
    assertEq(a, 10);
    assertEq(b, 200);
    assertEq(c, 200);
    assertEq(d, 980000);
    assertEq(e, 210);
    endTest();
}
