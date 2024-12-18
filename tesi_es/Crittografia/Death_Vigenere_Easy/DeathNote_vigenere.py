###ROT13 and modified vigenere cipher
##DESCRIPTION: L has intercepted a message from Kira that appears to be encrypted using a combination of ROT13 and a modified Vigenère cipher.
# Your task is to help L to decode the message and find the key. Kira, being meticulous, left a hint for the ROT13-transformed key.
# Use the provided hints to decrypt the message and reveal the hidden content. Enter the decrypted message to receive the flag.
#NOTE: ROT13 is a simple substitution cipher that shifts each letter by 13 positions in the alphabet
# The Vigenère cipher uses a keyword to shift letters in the plaintext.
# In this challenge, the Vigenère cipher is modified to include an additional shift based on the position of each character in the plaintext.
#HINT: the first hint is the key used for the modified vigenere cipher. It is encrypted throught ROT13, and is shinigami
#The seconf hint, is the formula used for compute the cyphertext. It is a modified vigenere cipher. In this case, include an additional shift based on the position of each character in the plaintext.
#P_index is the index of the plaintext character in the alphabet, K_index is the index of the key character in the alphabet, position_int is the position of the character in the plaintext.


import signal
import string
from itertools import cycle
signal.alarm(600)

def rot13(text):
    alphabet = string.ascii_uppercase
    rotated = alphabet[13:] + alphabet[:13]
    table = str.maketrans(alphabet, rotated)
    return text.translate(table)

def vigenere_encrypt(plaintext, key):
    alphabet = string.ascii_uppercase
    key_indices = [alphabet.index(k) for k in key]
    ciphertext = []

    for i, p in enumerate(plaintext):
        if p in alphabet:
            P = alphabet.index(p)
            #key_indices mi restituisce l'indice della lettera in posizione i della chiave (la chiave è ciclica), poi sommo 1, e poi sommo la posiozne in cui mi trovo con gli indici (sempre +1 perchè python parte da 0)
            shifted_K = (key_indices[i % len(key)] + 1 + (i + 1)) % 26 #PERCHÈ LE LETTERE PARTONO DA INDICE 0 E NON 1

            #shifted_K = (key_indices[i % len(key)] + (i + 1)) % 26
            C = (P + shifted_K) % 26
            ciphertext.append(alphabet[C])
        else:
            ciphertext.append(p)

    return ''.join(ciphertext)

def vigenere_decrypt(ciphertext, key):
    decrypted_text = []
    alphabet = string.ascii_uppercase
    key_indices = [alphabet.index(k) for k in key]

    for i, char in enumerate(ciphertext):
        if char in alphabet:
            C = alphabet.index(char)
            shifted_K = (key_indices[i % len(key)] + 1  + (i + 1)) % 26
            #shifted_K = (key_indices[i % len(key)] + (i + 1)) % 26

            P = (C - shifted_K + 26) % 26
            decrypted_text.append(alphabet[P])
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)


def print_challenge():
    ascii_art = """
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡀⣿⣼⣼⡆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠐⠤⢄⡀⠀⠐⠤⣄⡠⣄⠀⠀⠀⣿⣿⣿⣿⣿⣿⣷⣷⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠓⠲⠶⢶⣽⣿⣷⣄⣰⣿⣿⣿⣿⣿⣿⣿⣿⡜⣀⣀⡴⣚⣠⣔⣚⠉⠁⠀⠀⠀
⡠⠔⠒⠋⣩⣽⠿⣿⣿⣿⣿⣿⣿⣿⠃⠙⠿⠋⢻⣿⣿⣾⣿⣿⣿⣿⣿⣶⣦⣉⠁⠂⠀⠀
⢀⡠⠖⢋⣵⡾⣿⣿⣿⣿⣿⠟⢹⣻⢶⣄⠀⣠⢼⣿⣻⠿⢻⣿⣿⣿⣿⣿⣻⢯⣛⠻⣖⠒
⠀⠀⢀⠞⢡⢞⣿⣿⣿⣿⣿⣆⠐⢽⣮⡉⠉⠉⣽⠃⠉⠀⣾⣿⣿⣿⣿⣿⡿⣷⡈⠑⢆⠁
⠀⡰⠋⣰⠃⣜⣾⣿⣿⣿⣿⣿⣦⣀⢹⠻⣿⣿⡿⠀⠀⣼⣿⣿⣿⣿⣿⣿⣟⢌⢻⣄⠀⠀
⠊⠀⢠⠃⢀⣿⣿⣿⣿⠏⡟⠹⣯⡟⢿⣧⣤⣽⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡈⠞⠈⠆⠀
⠀⠀⠀⠐⢩⣿⣿⠏⠈⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠉⠉⠉⢻⣿⣿⡆⠀⠀⠀
⠀⠀⢀⣴⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⢻⣿⡿⣄⠀⠀
⠀⠀⣸⣿⣿⡏⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠘⠿⣿⣿⣶⠁
⠀⢠⢿⣿⣿⡅⠀⠀⠀⠀⠀⠀⣼⣻⣿⣾⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⢻⣿⣿⡦
⠀⠁⢾⣿⣿⣷⠀⠀⠀⠀⢀⣴⣧⣽⣿⣿⣫⣩⣿⣿⣿⡿⣿⣿⡄⠀⠀⠀⠀⠀⣿⣿⣿⠱
⠀⠀⠀⢸⣿⣿⠀⠀⠀⣠⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⣿⣿⡟⠀
⠀⠀⠀⠈⣿⣿⠀⠀⣴⣹⣿⣽⣿⣿⣿⣿⣿⣿⣿⣷⣯⣿⣿⣿⣿⣧⣄⠀⠀⠀⢸⣿⠃⠀
⠀⠀⠀⠀⢹⣿⡆⠐⢡⣿⣿⣿⣿⢿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⢸⣿⠆⠀
⠀⠀⠀⠀⠈⣿⣷⠀⣸⣿⣿⣿⠏⢸⡃⡿⠁⠀⢿⠀⢻⠿⣿⣿⣿⣿⣿⡷⠀⠀⣿⣿⠀⠀
⠀⠀⠀⢠⣄⣼⣟⣦⢿⣿⡿⠃⠀⠀⠃⠇⠀⠀⠸⠀⠘⠀⢻⣿⣿⣽⡏⠀⠀⢀⣿⣿⠀⠀
⠀⠀⠀⠀⠙⣿⠿⣷⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣯⢧⠀⠀⣿⣿⣿⠁⠀
⠀⠀⠀⠀⢀⡟⢰⣾⣿⡧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣇⣾⣿⣿⣿⠀⠀
⠀⠀⠀⠀⣼⣷⡞⢻⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⠋⢹⣿⣿⣇⠀
⠀⠀⠀⠀⣿⣯⣿⠈⣧⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⡿⠀⢀⡿⡟⡟⠀
⠀⠀⠀⠀⠈⠻⣾⣿⡽⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣿⣿⠇⢈⣾⣷⡿⠁⠀
⠀⠀⠀⠀⠀⠀⠈⠳⠎⢹⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠈⠡⠟⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⠅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

    KIRA'S SECRET MESSAGE:
    """
    plaintext = ("DEATH NOTE IS MY TOOL AND JUSTICE IS MY DUTY THIS IS MY MESSAGE TO THE WORLD "
                 "I WILL ELIMINATE ALL EVIL AND CREATE A NEW WORLD FREE OF CRIME FEAR ME AS "
                 "I AM KIRA THE GOD OF THE NEW WORLD").replace(' ', '').upper()
    key = "SHINIGAMI"
    ciphertext = vigenere_encrypt(plaintext, key)
    key_cipher=rot13(key)
    hints = """
    Hints:
    1. """+key_cipher+""".
    2. C = (P_index + (K_index + position_int)) % 26

    Message: Alphabet composed only of Uppercase letter, no special characters is present.

    Enter the answer with no spaces and all upper case:
    """

    print(ascii_art)
    print(hints)
    ciphertext = vigenere_encrypt(plaintext, key)
    print("Testo cifrato:", ciphertext)
    plaintext = vigenere_decrypt(ciphertext, key)
    while True:
        response=input('Inserisci la tua risposta > ')
        if response==plaintext:
            print('deathnote{the_second_is_misa_misa}')
            break
        else:
            print('I am smarter than you L')



print_challenge()

#DEATHNOTEISMYTOOLANDJUSTICEISMYDUTYTHISISMYMESSAGETOTHEWORLDIWILLELIMINATEALLEVILANDCREATEANEWWORLDFREEOFCRIMEFEARMEASIAMKIRATHEGODOFTHENEWWORLD