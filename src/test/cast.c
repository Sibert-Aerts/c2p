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
    int a, b, c;
    float x, y, z;
    char j, k, l;
    
    // regular casting
    
    a = (int)100;       // a = 100
    b = (int)100.0;     // b = 100
    c = (int)'d';       // c = 100
    
    assertEq(a, 100);
    assertEq(b, 100);
    assertEq(c, 100);
    
    x = (float)100.0;   // x = 100.0
    y = (float)100;     // y = 100.0
    z = (float)'d';     // z = 100.0
    
    assertEqf(x, 100.0);
    assertEqf(y, 100.0);
    assertEqf(z, 100.0);
    
    j = (char)'d';      // j = 'd'
    k = (char)100;      // k = 'd'
    l = (char)100.0;    // l = 'd'
    
    assertEqc(j, 'd');
    assertEqc(k, 'd');
    assertEqc(l, 'd');
    
    // pointer casting and arithmetic (UB?)
    
    int one = (int)&b - (int)&a;    // one = 1
    int c2 = *(int *)((int)&a + 2); // c2 = c = 100
    
    assertEq(one, 1);
    assertEq(c2, 100);
    
    endTest();    
}
