#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#ifdef SERVER
#define FLAG "CTF{FLAG_SERVER}"
#else
#define FLAG "CTF{FLAG_LOCALE}"
#endif
void win() {
    // Funzione che vogliamo raggiungere tramite buffer overflow
    printf(FLAG);
    fflush(stdout); 
    exit(0);
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
