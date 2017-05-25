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

int integral(int x){
    if(x==1)
        return 1;
    return x * integral(x-1);
}

int sum(int x){
    if(x==0)
        return 0;
    return x + sum(x-1);
}

int fib(int i){
    if(i == 0)
        return 0;
    if(i == 1)
        return 1;
    return fib(i-1) + fib(i-2);    
}

int main(){
    assertEq(integral(10), 3628800);
    assertEq(sum(200), 20100);
    assertEq(fib(20), 6765);
    endTest();
}
