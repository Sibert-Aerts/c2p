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

int sum(int (*x)[10]){
    int out = 0;
    for(int i = 0; i < 10; i++)
        out += (*x)[i];
    return out;    
}

int main(){
    int x[10][20];
    int (*y)[20] = &x[4];
    x[4][15] = 201;
    
    assertEq(x[4][15], (*y)[15]);
    
    int values[10];
    for(int i = 0; i < 10; i++)
        values[i] = i * i - 2 * i + 3;
    assertEq(225, sum(&values));
    
    endTest();
    return 0;
}
