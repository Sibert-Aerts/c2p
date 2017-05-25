#include <stdio.h>

int assertCount, errorCount;

void assertEq(int x, int y){
    assertCount++; if(x == y) return; errorCount++;
    printf("ASSERTION %d FAILED: %d does not equal %d\n", assertCount, x, y);
}

void assertEqc(char x, char y){
    assertCount++; if(x == y) return; errorCount++;
    printf("ASSERTION %d FAILED: '%c' does not equal '%c'\n", assertCount, x, y);
}

void assertEqf(float x, float y){
    assertCount++; if(x - y <= 0.001 && x - y >= -0.001) return; errorCount++;
    printf("ASSERTION %d FAILED: %f does not equal %f\n", assertCount, x, y);
}

void endTest(){
    if(errorCount > 0) printf("TEST FAILED: Encountered %d assertion error%s out of %d!", errorCount, errorCount==1?"":"s", assertCount);
    else printf("TEST SUCCESSFUL: All %d assertions passed!", assertCount);
}

int main(){
    int i, j = 10;
    i = i + j + 10;
    
    assertEq(i, 20);
    assertEq(j, 10);
    
    float x, y = 10.0;
    x = x + y + 10.0;
    
    assertEqf(x, 20.0);
    assertEqf(y, 10.0);
    
    char c;       // 0
    
    assertEqc(c, (char) 0);
    
    //void* p;    // 0?
    
    endTest();
}
