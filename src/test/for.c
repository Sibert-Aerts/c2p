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
    int total1 = 0, total2 = 0;
    
    // total1 = 55
    for(int i = 1; i <= 10; i++)
        total1 += i;
        
    assertEq(total1, 55);
    
    // total2 = 55
    int i = 1;
    for(;;)
    {
        if(!(i <= 10))
            break;
        total2 += i++;
    }    
    
    assertEq(total2, 55);
    endTest();
}
