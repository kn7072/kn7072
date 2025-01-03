#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    uint32_t i;
    uint32_t r = 0;
    for (i = 0; i < 10; ++i) {
        r += i*i + 13*r*i + 17;   /* LINE 10. */
    }
    printf("%" PRIu32 "\n", r);
    return EXIT_SUCCESS;
}

