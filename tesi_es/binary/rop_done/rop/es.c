#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int wish(char* word1, char* word2) {
    if (word1 == "Appari") {
        if (word2 == "Shenron") {
            printf("CBL{Sparking_Z3r0}");
        }
    } else {
        printf("How dare you");
    }
}


int main() {
    char buffer[40];
    printf("... \n");
    printf(">");
    gets(buffer);
    printf("...");
    return 0;
}