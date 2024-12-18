#text="pikachubelloforte"
################SOLUZIONE######################
#######NOTA : il simbolo + indica lo xor
# Mettendo come text quello sottostante, essendo il blocco di 16 bytes, alla fine avrai 4 blocchi così suddivisi:
#    iv | c1 | c2 | c3
# dove iv è l'inizialization vector (16 bytes)
# c1 è il ciphertext del primo blocco: usr=bdminbelloer
# c2 è il ciphertext del secondo blocco: forte&is_admin=F
#c3 è totalmente padding
#Il tuo obbiettivo è quello di fare in modo che il quello che lui assegna alla variabile user sia usr=admin e quello che assegna alla variabile admin sia is_admin=T
#Non puoi passare come input & o la parola admin (lui usa la & per splittare le parole), per cui devi fare in modo di riuscire a modificare alcuni bit del plaintext originale quando viene decifrato il ciphertext.
#Per fare questo, basandoci sullo schema di CBC encryption / decryption :
#1) escludiamo il terzo blocco, in quanto è solo padding
# 2) partendo dal secondo blocco, il corrispettivo plaintext (b2) è forte&is_admin=F. Devo cambiarlo in forte&is_admin=T (b2_m). So che b2 = D(p2) + c1.
# analogmanete so che b2_m deve essere: b2_m= D(p2) + c1.
# Non conosco D(p2) (è quello che esce dalla funzione di decifratura dal blocco di AES), ma posso ricavarlo, e posso modificare c1 (c1_m), per fare in modo che l'operazione di xor restituisca b2_m
# Quindi: D(p2) = b2 + c1 e c1_m = b2_m + D(p2)
#Ripeto il procedimento analogamente per il primo blocco. In questo caso, il primo blocco deve essere usr=admin&belloe
#Perchè poi lui userà la & per dividere, e prenderà usr=admin e lo inserirà in user.
#Per fare questo, posso modificare l'iv.
#So che b1=D(p1) + c1 e b1_m=D(p1) + iv. Analogamente a prima, posso modificare l'iv e ricavarmi D(p1) --> D(p1) = c1 + b1 e iv= b1_m + D(p1)
# Ora ho tutto quello che mi serve per ottenere la flag e comporre il ciphertext corretto:
#iv_m + c1 (che verrà modificato dall'iv) + c2 + c1_m + c2 (che verrà modificato da c1_m) + c3 (il blocco di padding)

#Per utilizzare lo script, basta inserire la flag che viene restituita quando si inserisce text, far partire lo script, e poi mettere il valore restituito nell' oracolo che decifra. In questo modo, si potrà poi ricevere la flag.

text='bdminbelloerforte'
#flag='9576effe894e4734b02130ffc4cc7d203aeeaf5337a70fffc1879da7d606193e7fb009792736f07a29a8f714b6008d458e407613fcb780b154bba80890b1994e'
flag='cb47d543523ef578cebd66068aaa884b59182eee3bbe135ff86c06bd4b3f87ed2251780ea5d4190a0209c83b7bca5c3f59fae7fec96cb442f11106fe8b6d0069'
iv=flag[:32]
c1=flag[32:64]
c2=flag[64:96]
c3=flag[96:]

#b1='usr=pikachubello'
b1='usr=bdminbelloer'
b2='forte&is_admin=F'
b2_m='forte&is_admin=T'

b1_hex=b1.encode().hex()
b2_hex=b2.encode().hex()
b2_m_hex=b2_m.encode().hex()

enc=int(b2_hex,16) ^ int(c1,16)

c1_m=int(b2_m_hex,16) ^ enc
c1_m=hex(c1_m)[2:]
#print(c1_m)

#b1_m=';usr=pikachubell'
b1_m='usr=admin&belloe'
b1_m_hex=b1_m.encode().hex()

enc0=int(b1_hex,16) ^ int(iv,16)
iv_m=enc0 ^ int(b1_m_hex,16)
iv_m=hex(iv_m)[2:]

block=iv_m+c1+c2+c1_m+c2+c3
print(block)
