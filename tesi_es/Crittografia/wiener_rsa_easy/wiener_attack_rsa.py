#Soluzione:
#python3 RsaCtfTool.py -n 122308201774583579870292757280324530559866831270193277844578973471235461793576502246230928736093832346162339016463558719644120336647120346796167741893016283070850949578093618903847691113254750672298104132584883883602856442470152269943526756794018630456731770114656853239789086178920368667370647189371489215173 -e 55021796376485630126710425179181971450981314229028304648814298564959919915030210922394251890726978810376105423406038310069286231292289379231676227236998998749375144870962139997289639010341602629106243952742965543432579250376133085115616519567991661478643352422122160605624259309375110118846408331541387490555 --attack wiener --decrypt 85275494785607463826060601091548043551169692902227672792819783334260664587658902145320541556615777277304949730038398567224944339886509930299926914858523829917343613999535273074559986904251442599513001076039447529111608463801466804893891452801174800854724657857828439854822814137775852793428272576191009745510 --private

import base64
import random
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

# Funzione per generare i valori di N, e, d
def generate_rsa_values_for_wiener(bits):
    while True:
        # Step 1: Genera due numeri primi p e q
        p = getPrime(bits)
        q = getPrime(bits)
        N = p * q

        # Step 2: Calcola φ(N)
        phi_N = (p - 1) * (q - 1)

        # Step 3: Scegli un piccolo d tale che gcd(e, φ(N)) = 1 e d < N^(1/4) / 3
        max_d = int(pow(N, 0.25) / 3)
        d = random.randint(1, max_d)

        try:
            # Step 4: Calcola l'esponente pubblico e
            e = inverse(d, phi_N)
            if e < N and (e * d) % phi_N == 1:
                break
        except ValueError:
            continue

    return N, e, d

# Genera i valori con 512 bit
bits = 512
N, e, d = generate_rsa_values_for_wiener(bits)
print('----------------------------------------------------')
print('    Benvenuto, prova a recuperare la flag!')
# Stampa i valori pubblici e privati
print(f"N: {N}")
print(f"e: {e}")
#print(f"d: {d}")

flag = b"CBL{W!eNer_Attack_e_too_big}"
m = bytes_to_long(flag)
c = pow(m, e, N)
print(f"Flag Cifrata: {c}")
print('---------------------------------------------------')

