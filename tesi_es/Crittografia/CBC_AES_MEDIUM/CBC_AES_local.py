#############AES WITH CBC--> BIT FLIPPING ATTACK ---------------------------
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

flag='CBL{placeholder}'
BLOCK=16
users=[]

key = os.urandom(16)


def menu():
    while True:
        print('Scegli tra le opzioni:')
        print('1- Registrati')
        print('2- Login')
        print('3- Exit')
        choice=int(input('>'))
        if choice==1:
            print('Inserisci il tuo nome utente')
            user=input('> ')
            if 'admin' in user:
                print('Non puoi spacciarti per admin')
                continue
            if '&' in user:
                print('Cosa stai cercando di fare?')
                continue
            cookie=f'usr={user}&is_admin=F'.encode()
            #print(cookie)
            iv = os.urandom(16)
            #print(iv)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            token=cipher.encrypt(pad(cookie, 16))
            print('Ecco il tuo token:'+iv.hex()+token.hex())
        if choice==2:
                token=input('Inserisci il tuo token: > ')
                #print(token)
                iv=bytes.fromhex(token[:32])
                #print(iv)
                cookie_c=bytes.fromhex(token[32:])
                cipher=AES.new(key,AES.MODE_CBC,iv)
                cookie=unpad(cipher.decrypt(cookie_c),16)
                #print(cookie)
                cookie_part=cookie.split(b'&')
                user= cookie_part[0].decode()
                admin= cookie_part[-1].decode()
                #print(user)
                #print(admin)
                if user=='usr=admin' and admin=='is_admin=T':
                    print('Bentornato admin. Che operazione vuoi svolgere?')
                    print('1 - Dammi la flag')
                    print('2 - Esci')
                    choice=int(input(('>')))
                    if choice == 1:
                        print(flag)
                        break
                    else:
                        continue
                else:
                    print('Bentornato: '+user+' is_admin=F')








if __name__ == "__main__":
    menu()
