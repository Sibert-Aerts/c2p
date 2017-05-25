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

int x = 10;

int main(){
    int a = 10, b = 20, c;
    float x = 10.0, y = 20.0, z;
    
    
    c = a + b - a * b / a * -a; // c = 230
    
    assertEq(c, 230);
    
    z = x + y - x * y / x * -x; // z = 230.0
    
    assertEqf(z, 230.0);
    
    360;
    
    {
        int a = 12345;
        assertEq(a, 12345);
        assertEq(b, 20);
    }
    
    assertEq(a, 10);
    assertEq(b, 20);
    
    {
        float x = 5678.9;
        assertEqf(x, 5678.9);
        assertEqf(y, 20.0);
    }
    
    assertEqf(x, 10.0);
    assertEqf(y, 20.0);
    
    endTest();
}
