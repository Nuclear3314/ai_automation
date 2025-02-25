#include <stdio.h>
#include "hello.h"

void test_hello() {
    hello();
}

int main() {
    test_hello();
    printf("All tests passed.\n");
    return 0;
}