La challenge è completamente funzionante.
Ai partecipanti va dato il file .py in modo che possano vedere come funziona l'algoritmo
modificato e recuperare la flag.

Nel file .py ci sono 2 modifiche da fare:
1) Il testo plaintext va scritto in un file .txt esterno e caricato da lì 
(per nasconderlo ai giocatori)
2) La chiave va caricata da un file esterno key.txt (SHINIGAMI)
2) la flag va caricata da un secondo file .txt (flag.txt) che contiene il vero valore della flag

Per risolvere l' esercizio:
1) Decifrare la key di vigenere cifrata con ROT13 usando tool online come https://www.dcode.fr/rot-13-cipher, da cui si ottiene SHINIGAMI
2) Reverse Engineering l'algoritmo di cifratura, da cui si ottiene il Plaintext da inserire 
per ottenere la flag