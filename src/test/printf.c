#include <stdio.h>
int main() {
    const char foo[] = "hello";
    const int bar = -55;
    const float zip = 12.3456789;
    printf("Some values: %d, \"%s\", %f, '%c', and %d.\n", 13, foo, zip, 'x', bar);
    printf("Variable f precision: 1: %1f, 2: %2f, 3: %3f\n", zip, zip, zip);
    printf("A percent sign: %%.\n");
    return 0;
}
