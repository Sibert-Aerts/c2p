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

int sum = 0;

void testSum(){
    assertEq(sum, 45);
    sum = 0;
}

int main(){ 
    int x;
    
    for(int x; x < 10; x++)
        sum += x;
        
    testSum();

    for(x = 0; x < 10; x++)
        sum += x;
        
    testSum();

    x = 0;
    for(;x < 10; x++)
        sum += x;
        
    testSum();

    x = 0;
    for(;; x++){
        if( x >= 10) break;
        sum += x;
    }
        
    testSum();

    x = 0;
    for(;;){
        if( x >= 10) break;
        sum += x;
        x++;
    }
        
    testSum();
    
    x = 0;
    for(;x < 10;){
        sum += x;
        x++;
    }
        
    testSum();

    sum = 0;

    for(int x = 0;;x++){
        if( x >= 10) break;
        sum += x;
    }
        
    testSum();

    for(x = 0;;x++){
        if( x >= 10) break;
        sum += x;
    }
        
    testSum();

    sum = 0;

    for(int x = 0;x < 10;){
        sum += x;
        x++;
    }
        
    testSum();

    sum = 0;

    for(x = 0;x < 10;){
        sum += x;
        x++;
    }
        
    testSum();

    for(int x;;){
        if( x >= 10) break;
        sum += x;
        x++;
    }
        
    testSum();

    for(x = 0;;){
        if( x >= 10) break;
        sum += x;
        x++;
    }
        
    testSum();
    endTest();
    
    return 0;
}
