#include <stdio.h>

int assertCount, errorCount;

void assertTrue(bool x){
    assertCount++; if(x) return; errorCount++;
    printf("ASSERTION %d FAILED: False is not true!", assertCount);
}

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

bool strcmp(const char* x, const char* y){
    while((int)*x != 0 || (int)*y != 0) 
        { if(*x != *y) return false; x++; y++; }
    return true;
}

void assertEqstr(const char* x, const char* y){
    assertCount++; if(strcmp(x,y)) return; errorCount++;
    printf("ASSERTION %d FAILED: \"%s\" does not equal \"%s\"\n", assertCount, x, y);
}

void endTest(){
    if(errorCount > 0) printf("TEST FAILED: Encountered %d assertion error%s out of %d!", errorCount, errorCount==1?"":"s", assertCount);
    else printf("TEST SUCCESSFUL: All %d assertions passed!", assertCount);
}

void ifun(int x){}
void cfun(char x){}
void bfun(bool x){}

int main(){
    // Demote to int
    int x = 20.0;    
    assertEq(x, 20);
    
    x = 30.0;
    assertEq(x, 30);
    
    assertEq(40, 40.0);
    
    // Demote to char
    char c = 99.0;
    char d = 100;
    assertEqc(c, 'c');
    assertEqc(d, 'd');
    
    c = 67.0;
    d = 68;
    assertEqc(c, 'C');
    assertEqc(d, 'D');    
    
    assertEqc(101.0, 'e');
    assertEqc(102, 'f');
    
    // Demote to bool
    bool b1 = 10.0;
    bool b2 = 20;
    bool b3 = 'q';
    assertTrue(b1);
    assertTrue(b2);
    assertTrue(b3);
    
    b1 = 200.0;
    b2 = 300;
    b3 = 'z';
    assertTrue(b1);
    assertTrue(b2);
    assertTrue(b3);
    
    assertTrue(999.9);
    assertTrue(99);
    assertTrue('9');
    
    endTest();
}


























