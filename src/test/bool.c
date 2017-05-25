#include <stdio.h>

int errorCount;

void assertEqb(bool x, bool y){
    if(x == y) return;
    errorCount++;
    printf("ASSERTION FAILED: %s does not equal %s\n", x?"true":"false", y?"true":"false");
}

void endTest(){
    if(errorCount > 0)
        printf("TEST FAILED: Encountered %d assertion error%s!", errorCount, errorCount==1?"":"s");
    else
        printf("TEST SUCCESSFUL: No assertion errors encountered!");
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
