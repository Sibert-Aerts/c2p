#include <stdio.h>

int errorCount;

void assertEq(int x, int y){
    if(x == y) return;
    errorCount++;
    printf("ASSERTION FAILED: %d does not equal %d\n", x, y);
}

void assertEqf(float x, float y){
    if(x - y <= 0.001 && x - y >= -0.001) return;
    errorCount++;
    printf("ASSERTION FAILED: %f does not equal %f\n", x, y);
}

void endTest(){
    if(errorCount > 0)
        printf("TEST FAILED: Encountered %d assertion errors!", errorCount);
    else
        printf("TEST SUCCESSFUL: No assertion errors encountered!");
}

int main(){
    int a, b, c, d, e, f;
    float u, v, w, x, y, z;
        
    // ints
    a = 10;             // a = 10
    b = a + 10;         // b = 20
    c = b + b - 10;     // c = 30
    d = a * 4;          // d = 40
    e = a * a / 2;      // e = 50
    f = ((2 * a + b + - c + e) * d) / ( b * 2 ); // f = 60
    
    assertEq(a, 10);
    assertEq(b, 20);
    assertEq(c, 30);
    assertEq(d, 40);
    assertEq(e, 50);
    assertEq(f, 60);
        
    // floats
    u = 0.125;              // u = 0.125
    v = u + 0.125;          // v = 0.250
    w = v + v - 0.125;      // w = 0.375
    x = v * v * 8.0;        // x = 0.500
    y = x * 5.0 / 4.0;      // y = 0.625
    z = x * x * x + (w - u) * 2.0 + y - 1.0 / 2.0;    // z = 0.750 
    
    assertEqf(u, 0.125);
    assertEqf(v, 0.250);
    assertEqf(w, 0.375);
    assertEqf(x, 0.500);
    assertEqf(y, 0.625);
    assertEqf(z, 0.750);
    
    endTest();
    // TODO: add mixed int/float compatibility & tests
}
