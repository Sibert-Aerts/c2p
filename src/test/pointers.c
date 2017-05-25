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

int main(){
    int a = 10;
    int *b = &a;    // b = 14* (changes with code)
    int c = *b;     // c = 10
    *b = 20;        // a = 20
    
    assertEq(c, 10);
    assertEq(a, 20);
    endTest();
}
