#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Canary fisso
unsigned int __stack_chk_guard = 0x12345678;

void __stack_chk_fail() {
    // Funzione che si attiva se il canary viene violato
    printf("Protezione canary violata!\n");
    exit(1);
}

void get_flag() {
    #ifdef SERVER
        printf("Flag: CTF{Real_Server_Flag}\n");
    #else
        printf("Flag: CTF{Placeholder_Flag}\n");
    #endif
}

void vulnerable_function() {
    char buffer[64];
    
    printf("Inserisci il tuo input: ");
    gets(buffer);  // Uso intenzionale di gets() per generare un buffer overflow
}

int main() {
    printf("Benvenuto al CTF! Prova a bypassare la protezione canary!\n");
    vulnerable_function();
    printf("Uscita sicura. Nessuna violazione rilevata.\n");
    return 0;
}

