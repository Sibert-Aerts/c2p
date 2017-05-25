#include <stdio.h>
int main() {
    const char foo[] = "hello";
    const int bar = -55;
    const float zip = 12.34;
    printf("Some values: %d, \"%s\", %f, '%c', and %d.\n", 13, foo, zip, 'x', bar);
    printf("A percent sign: %%.\n");
    return 0;
}
