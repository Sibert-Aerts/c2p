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

int a = 5;

int f(int b) {
    return a * b;
}

int main() {
    assertEq(f(4), 20);
    a = 3;
    assertEq(f(4), 12);
    endTest();
}
