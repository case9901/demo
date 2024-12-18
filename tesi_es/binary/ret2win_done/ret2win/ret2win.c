#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void win() {
    // Funzione che vogliamo raggiungere tramite buffer overflow
    printf("CTF{RET2W!N_W1N}\n");
}

void vuln() {
    char buffer[64];  // Buffer vulnerabile
    printf("Inserisci il tuo input: ");
    gets(buffer);     // Funzione insicura, vulnerabile al buffer overflow
    printf("Hai inserito: %s\n", buffer);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0); // Disabilita il buffering per output immediato
    vuln();  // Chiama la funzione vulnerabile
    printf("Programma terminato senza incidenti!\n");
    return 0;
}
