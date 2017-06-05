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

void floatFunc(float x){
    return;
}

void intFunc(int x){
    return;
}

char getChar(){
    return 'd';
}

int getInt(){
    return getChar();
}

int main(){
    assertEqc((char)1, true);

    assertEq(1, true);
    assertEq(100, true + 99);
    assertEq(100, 'd');
    assertEq(100, 'c' + 1);
    assertEq(100, 'b' + 1 + true);
    
    assertEqf(1.0, true);
    assertEqf(100.0, true + 99);
    assertEqf(100.0, 'd');
    assertEqf(100.0, 'c' + 1);
    assertEqf(100.0, 'b' + 1 + true);
    assertEqf(1.0, 1);
    assertEqf(100.0, 99 + 1.0);
    assertEqf(100.0, 'a' + 2 + 1.0);
    assertEqf(100.0, 'a' + 1 + 1.0 + true);
    
    endTest();
}















