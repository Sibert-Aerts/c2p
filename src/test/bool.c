#include <stdio.h>

int assertCount, errorCount;

void assertEqb(bool x, bool y){
    assertCount++; if(x == y) return; errorCount++;
    printf("ASSERTION %d FAILED: %s does not equal %s\n", assertCount, x?"true":"false", y?"true":"false");
}

void endTest(){
    if(errorCount > 0) printf("TEST FAILED: Encountered %d assertion error%s out of %d!", errorCount, errorCount==1?"":"s", assertCount);
    else printf("TEST SUCCESSFUL: All %d assertions passed!", assertCount);
}

int main(){
    bool t_, f_, a, b, c, d, e, f;
    t_ = true;          // t_ = true
    f_ = false;         // f_ = false
    
    a = true || t_;     // a = true
    b = true && t_;     // b = true
    c = false || t_;    // c = true
    d = true && f_;     // d = false
    e = !true;          // e = false
    f = !(!(true && false) && (a && (!b || !d)));   // f = false
    
    assertEqb(a, true);
    assertEqb(b, true);
    assertEqb(c, true);
    assertEqb(d, false);
    assertEqb(e, false);
    assertEqb(f, false);
    endTest();
}
