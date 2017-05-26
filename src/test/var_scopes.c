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

int a = 100;
int b = 100;
int c = 100;
int d = 100;
int e = 100;

int main(){
    assertEq(a, 100);
    assertEq(b, 100);
    assertEq(c, 100);
    assertEq(d, 100);
    assertEq(e, 100);    

    int x = 200;
    int y = 200;
    int z = 200;
    
    int b = 200;
    
    d = 200;
        
    assertEq(x, 200);
    assertEq(y, 200);
    assertEq(z, 200);
    assertEq(b, 200);
    
    assertEq(d, 200);
    
    {
        assertEq(a, 100);
        assertEq(b, 200);
        assertEq(c, 100);
        assertEq(d, 200);
        assertEq(e, 100);  
        assertEq(x, 200);
        assertEq(y, 200);
        assertEq(z, 200);
        
        int i = 300;
        
        int c = 300;
        int y = 300;
        
        z = 300;
        e = 300;
        
        assertEq(i, 300);
        assertEq(c, 300);
        assertEq(y, 300);
        
        assertEq(e, 300);
        assertEq(z, 300);
    }
    assertEq(a, 100);
    assertEq(b, 200);
    assertEq(c, 100);
    assertEq(d, 200);
    assertEq(e, 300);  
    assertEq(x, 200);
    assertEq(y, 200);
    assertEq(z, 300);
    
    endTest();
}

/*
    This gives the following structure in the p-machine:
	[9]	        [i]	100     // global a
	[10]		[i]	100     // global b
	[11]		[i]	100     // global c
	[12]		[i]	200     // global d
	[13]		[i]	300     // global e
    ...
	[19]		[i]	200     // main x
	[20]		[i]	200     // main y
	[21]		[i]	300     // main z
	[22]		[i]	200     // main b
	[23]		[i]	300     // scoped i
	[24]		[i]	300     // scoped c
	[25]		[i]	300     // scoped y

*/
