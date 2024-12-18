##La soluzione utilizza pwntool per risolvere l'esercizio, dato il constraint di 30s.
# L' attaccante è in grado di intercettare le chiavi pubbliche A e B scambiate durante DH.
# Quello che fa, è:
#1) Quando ALICE manda a Bob A: prende da parte A, si sceglie una sua chiave privata (in questo caso i = 2), e manda I=g^i mod p a B.
#2) Bob pensa che la chiave pubblica di Alice sia I, e manda la chiave pubblica B=g^b mod p ad Alice (b chiave private di Bob)
#3) All' attacc. arriva B, lo mette da parte e invia ad Alice la sua chiave pubblica I
#4) A questo punto, Alice e Bob calcolano le loro chiavi segreti:
#5) Ka_i=I^a mod p (a chiave privata di Alice)
#6) Kb_i = I^b mod p (b chiave privata di Bob)
#7) L'attaccante, che è nel mezzo, conosce sia A che B, ed è in grado di calcolarsi sia Ka_i=A^i mod p  che Kb_i = B^i mod p
#8) Alice e Bob si calcolano la loro chiave simmetrica a partire dalla chiave segreta, che useranno per cifrare il messaggio, e l'attaccante fa lo stesso
#9) Alice manda la flag cifrata a Bob
#10) L'attaccante intercetta il messaggio, e decifra la flag con la 



from pwn import remote
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long
import hashlib

PORT = 41767
r = remote('127.0.0.1', PORT)

# Ricevi i dati iniziali
r.recvuntil(b'Bob:')
r.recvline()
p_q = r.recvline().decode()
componenti = p_q.split()
print(componenti)
# Ottieni i valori di p e g e convertili in interi
p = int(componenti[1])
g = int(componenti[3])

# Ricevi la chiave pubblica A di Alice
A = r.recvline().decode()
A=int(A.split()[2])
print(A)

# Genera i valori di i e le chiavi intermedie
i = 2
Ka_i = pow(A, i, p)
I = pow(g, i, p)

# Invia la chiave pubblica intermedia I a Bob
r.sendline(str(I))

# Ricevi la chiave pubblica B di Bob e converti in int
r.recvline()
B = r.recvline().decode()

B = int(B.split()[2])
Kb_i = pow(B, i, p)

# Invia nuovamente la chiave pubblica intermedia I a Alice
r.sendline(str(I))

# Ricevi il flag cifrato (prima parte)
r.recvline()
flag_1_enc_hex = r.recvline()
flag_1_enc=flag_1_enc_hex.strip().split()[-1]
flag_1_enc = bytes.fromhex(flag_1_enc.decode())
# Genera l'hash della chiave Ka_i
key_hash = hashlib.sha256(Ka_i.to_bytes((Ka_i.bit_length() + 7) // 8, byteorder='big')).digest()

# Decifra il messaggio
cipher = AES.new(key_hash, AES.MODE_ECB)
flag_1_dec = unpad(cipher.decrypt(flag_1_enc), 16)

# Stampa il flag decifrato
print('Flag decifrato:', flag_1_dec.decode())
r.sendline(flag_1_dec)


#RIcevi il messaggio cifrato (parte 2)
r.recvline()
flag_2_enc_hex = r.recvline()
flag_2_enc=flag_2_enc_hex.strip().split()[-1]
flag_2_enc = bytes.fromhex(flag_2_enc.decode())
# Genera l'hash della chiave Ka_i
key_hash = hashlib.sha256(Kb_i.to_bytes((Kb_i.bit_length() + 7) // 8, byteorder='big')).digest()

# Decifra il messaggio
cipher = AES.new(key_hash, AES.MODE_ECB)
flag_2_dec = unpad(cipher.decrypt(flag_2_enc), 16)

# Stampa il flag decifrato
print('Flag decifrato:', flag_2_dec.decode())
r.sendline(flag_2_dec)
