#include <stdio.h>
#include <string.h>

void win() {
    printf("Congratulazioni! Hai trovato la flag: FLAG{buffer_overflow_success}\n");
}

void vuln() {
    char buffer[64];

    printf("Inserisci il tuo input: ");
    gets(buffer);  // Funzione vulnerabile, non controlla la lunghezza dell'input.
}

int main() {
    printf("Benvenuto alla sfida di Buffer Overflow!\n");
    vuln();
    printf("Grazie per aver partecipato!\n");
    return 0;
}
