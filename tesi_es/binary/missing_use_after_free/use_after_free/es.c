#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct User {
    char *username;
    int auth_level;
} User;

User *loggedIn = NULL;

void login() {
    if (loggedIn) {
        printf("Already logged in!\n");
        return;
    }
    loggedIn = malloc(sizeof(User));
    if (!loggedIn) {
        perror("Failed to allocate memory for user struct");
        exit(1);
    }
    loggedIn->username = malloc(0x10);
    if (!loggedIn->username) {
        perror("Failed to allocate memory for username");
        free(loggedIn);
        exit(1);
    }
    
    printf("Enter username: ");
    scanf("%15s", loggedIn->username);
    
    loggedIn->auth_level = 1;
    printf("Welcome, %s\n", loggedIn->username);
    printf("Your auth level is: %d\n", loggedIn->auth_level);
}

void logout() {
    if (!loggedIn) {
        printf("Not logged in!\n");
        return;
    }

    free(loggedIn->username);
    free(loggedIn);
    loggedIn = NULL;
    
    printf("Logged out!\n");
}

void check() {
    if (!loggedIn) {
        printf("Not logged in!\n");
        return;
    }
    
    printf("Auth level: %d\n", loggedIn->auth_level);
}

int main() {
    char command[16];
    
    while (1) {
        printf("Enter command (login, logout, check): ");
        scanf("%15s", command);
        
        if (strcmp(command, "login") == 0) {
            login();
        } else if (strcmp(command, "logout") == 0) {
            logout();
        } else if (strcmp(command, "check") == 0) {
            check();
        } else {
            printf("Invalid command!\n");
        }
    }
    return 0;
}
