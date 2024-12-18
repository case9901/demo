#include <stdio.h>
#include <stdlib.h>

int main() {
  int segreto = 0;
  char buffer[10];

  printf("Indirizzo di segreto: %p\n", &segreto); // Per semplicità, stampiamo l'indirizzo

  printf(buffer); // Vulnerabilità!

  if (segreto == 1337) {
    printf("CTF{geppetto}\n");
  }

  return 0;
}

