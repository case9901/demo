#####Exercise number 1###########
#### RSA CHOSEN CIPHERTEXT ATTACK #############
import signal
import sys

from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long

TIMEOUT = 600
flag='CBL{Welc0mE_T0_RsA_!}'

def menu():
    print()
    print('Scegli l" operazione da fare:')
    print('0: Aiuto')
    print('1: Cifra un messaggio')
    print('2: Decifra un messaggio')
    print('3: Esci')
    return input('Inserisci il comando: >')


def encrypt(m, rsa):
    return pow(m, rsa.e, rsa.n)

def decrypt(c,n,rsa):
    return pow(c, rsa.d, n)

def oracle():
    rsa = RSA.generate(1024)
    print('DA RIMUOVERE:', rsa.n)
    print('Pubblico esponente:', rsa.e)
    sys.set_int_max_str_digits(0)
    print(pow(49,rsa.e))
    flag_cipher = pow(bytes_to_long(flag.encode()), rsa.e, rsa.n)
    print('==================================================================')
    print('                    Try to decrypt the flag                       ')
    print('  You can Encrypt and Decrypt whatever you want, except the flag  ')
    print('==================================================================')
    print()
    print("Encrypted Flag:", flag_cipher)
    while True:
        choice = menu()

        # Exit
        if choice == '0':
            print("Prova a cercare attack on RSA Oracle o CTF RSA Oracle!")

        # Encrypt
        elif choice == '1':
            m = int(input('\nPlaintext > ').strip())
            print('\nEncrypted: ' + str(encrypt(m, rsa)))

        # Decrypt
        elif choice == '2':
            n = int(input('\nModulo > ').strip())

            c = int(input('\nCiphertext > ').strip())

            if c == flag_cipher:
                print("Non puoi decifrare la flag!!")
            else:
                m = decrypt(c,n,rsa)
                print('\nDecrypted: ' + str(m))
        else:
            print('bye!')
            break


if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    oracle()
