#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>


// Struttura di dati degli utenti
typedef struct {
    char nome_utente[20];
    char password[20];
    char email[30];
    bool is_admin;
} utente;

// Funzione per registrare un nuovo utente
void registrazione_utente(utente **utenti, int *num_utenti) {

    utente *nuovo_utente = (utente *)malloc(sizeof(utente));
    nuovo_utente->is_admin = false;

    printf("Inserisci il nome utente: ");
    gets(nuovo_utente->nome_utente); // **VULNERABILITÀ: Heap Overflow**
    printf("Inserisci la password: ");
    gets(nuovo_utente->password);
    printf("Inserisci l'email: ");
    gets(nuovo_utente->email);

    // Aggiungi il nuovo utente alla lista
    *utenti = (utente *)realloc(*utenti, (*num_utenti + 1) * sizeof(utente));
    (*utenti)[*num_utenti] = *nuovo_utente;
    (*num_utenti)++;

    free(nuovo_utente); // **Nota:** non è necessario, ma per buona pratica
}

// Funzione per eseguire il login
void login(utente *utenti, int num_utenti) {
    char nome_utente[20];
    char password[20];

    printf("Inserisci il nome utente: ");
    gets(nome_utente);
    printf("Inserisci la password: ");
    gets(password);

    for (int i = 0; i < num_utenti; i++) {
        if (strcmp(utenti[i].nome_utente, nome_utente) == 0 &&
            strcmp(utenti[i].password, password) == 0) {
            if (utenti[i].is_admin) {
                printf("Benvenuto, amministratore!\n");
                // **FLAG:** HHC{4dm1n_f14g_1534}
                printf("Flag: HHC{4dm1n_f14g_1534}\n");
            } else {
                printf("Benvenuto, utente!\n");
            }
            return;
        }
    }
    printf("Credenziali errate.\n");
}

int main() {
    utente *utenti = NULL;
    int num_utenti = 0;

    // Registra l'amministratore (con credenziali hardcodate per semplicità)
    utente admin;
    strcpy(admin.nome_utente, "admin");
    strcpy(admin.password, "password123");
    admin.is_admin = true;
    admin.email[0] = '\0'; // Non utilizzato in questo esempio

    utenti = (utente *)malloc(sizeof(utente));
    *utenti = admin;
    num_utenti = 1;

    while (1) {
        printf("1. Registra utente\n");
        printf("2. Esegui login\n");
        printf("3. Esci\n");
        int scelta;
        scanf("%d", &scelta);
        getchar(); // Consumi il carattere di newline

        switch (scelta) {
            case 1:
                registrazione_utente(&utenti, &num_utenti);
                break;
            case 2:
                login(utenti, num_utenti);
                break;
            case 3:
                return 0;
            default:
                printf("Scelta errata. Riprova.\n");
        }
    }

    return 0;
}