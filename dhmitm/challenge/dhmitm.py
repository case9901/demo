##########DH MITM#########################
import hashlib
import signal
import sys

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import getStrongPrime
import random
signal.alarm(30)
NBITS=1024
g=2
flag_1='CBL{IT_is_BaD_T0_!nTERRupt'
flag2='_Some0ne_Else_ConverSaTion}'
p=getStrongPrime(NBITS)
a = random.randint(2, p - 1)
b = random.randint(2, p - 1)
try:
    print('Alice -------> Bob: ')
    print('p: ',p,'g: 2')
    A=pow(g,a,p)
    B=pow(g,b,p)
    print('Chiave pubblica:',A)
    A=int(input())

except:
    print('Invalid argument')
    sys.exit()

print('Bob -------> Alice: ')
try:
    print('Chiave pubblica:', B)
    B=int(input())
    keyA=pow(B,a,p)
    keyB=pow(A,b,p)
    key_hash_A = hashlib.sha256(keyA.to_bytes((keyA.bit_length() + 7) // 8, byteorder='big')).digest()
    key_hash_B = hashlib.sha256(keyB.to_bytes((keyB.bit_length() + 7) // 8, byteorder='big')).digest()

    cipherA = AES.new(key_hash_A, AES.MODE_ECB)
    flag_1_enc = cipherA.encrypt(pad(flag_1.encode(), 16))
except:
    print('Invalid argument')
    sys.exit()

print('Alice -------> Bob:')
print('Prima parte del flag:', flag_1_enc.hex())
input()

# Decifra il messaggio per verificare che funzioni correttamente
cipherB = AES.new(key_hash_B, AES.MODE_ECB)
flag_2_enc=cipherB.encrypt(pad(flag2.encode(),16))
print('Bob -------> Alice:')
print('Seconda parte della flag:', flag_2_enc.hex())
input()
