from Crypto.Util.number import getStrongPrime, getPrime

BLOCK_SIZE=16
NBITS=16


p=65537
def stringa_a_ascii_intero(stringa):
    # Crea una lista dei valori ASCII dei caratteri nella stringa
    valori_ascii = [ord(carattere) for carattere in stringa]

    # Concatena i valori ASCII in una singola stringa
    stringa_ascii = ''.join(map(str, valori_ascii))

    # Converte la stringa concatenata in un intero
    numero_intero = int(stringa_ascii)
    return numero_intero
flag='CBL{il_summit_e_tra_5_giorni}'
print('3, ',p)
print('Naruto: Rasengaaan')
print('Sasuke: Mille Falchi')
A=stringa_a_ascii_intero('Rasengaaan')
B=stringa_a_ascii_intero('Mille Falchi')
#A=8297115101110103979797110
#B=7710510810810132709710899104105
a=34538
b=60040
iv=os.urandom(BLOCK_SIZE)
key=pow(A,b,p)
key2=pow(B,a,p)
if key2==key:
    key_bytes = hashlib.sha256(str(key).encode()).digest()
    cipher=AES.new(key_bytes,AES.MODE_CBC,iv)
    flag_encrypted=cipher.encrypt(pad(flag.encode(), 16))
    print('Naruto:'+iv.hex()+flag_encrypted.hex())
