#include <stdio.h>

int assertCount, errorCount;

void assertEq(int x, int y){
    assertCount++; if(x == y) return; errorCount++;
    printf("ASSERTION %d FAILED: %d does not equal %d\n", assertCount, x, y);
}

void assertEqf(float x, float y){
    assertCount++; if(x - y <= 0.001 && x - y >= -0.001) return; errorCount++;
    printf("ASSERTION %d FAILED: %f does not equal %f\n", assertCount, x, y);
}

void endTest(){
    if(errorCount > 0) printf("TEST FAILED: Encountered %d assertion error%s out of %d!", errorCount, errorCount==1?"":"s", assertCount);
    else printf("TEST SUCCESSFUL: All %d assertions passed!", assertCount);
}

int main(){
    int a, b, c, d, e, f;
    float u, v, w, x , y, z;
    
    a = 100;        // a = 100
    
    b = c = d = e = f = 100;     
    b += 100;       // b = 200    
    c -= 50;        // c = 50
    d *= 2;         // d = 200
    e /= 2;         // e = 50 
    
    f += c;
    f *= d;
    f /= 100;
    f -= 200;       // f = 100
    
    assertEq(a, 100);
    assertEq(b, 200);
    assertEq(c, 50);
    assertEq(d, 200);
    assertEq(e, 50);
    assertEq(f, 100);
    
    u = 0.5;        // u = 0.5
    
    v = w = x = y = z = 0.5;
    v += 0.5;       // v = 1.0
    w -= 0.25;      // w = 0.25
    x *= 0.5;       // x = 0.25
    y /= 0.5;       // y = 1.0
    
    z += v;
    z -= w + x;
    z *= ((v - x) / w);
    z /= y + x * 4.0 + v;   // z = 1.0
    
    assertEqf(u, 0.5);
    assertEqf(v, 1.0);
    assertEqf(w, 0.25);
    assertEqf(x, 0.25);
    assertEqf(y, 1.0);
    assertEqf(z, 1.0);
    
    endTest();
}
