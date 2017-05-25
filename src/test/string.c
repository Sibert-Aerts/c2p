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

int main(){

    const char text[] = "abcdefg";    
    assertEqstr((char*)text, (char*)"abcdefg");
    
    char c = text[1];    
    assertEqc(c, 'b');
    
    c = text[7];    
    assertEqc(c, (char)0);
    
    char* s = (char*)((int)text + 3);    
    assertEqstr(s, (char*)"defg");
    
    
    endTest();
}
