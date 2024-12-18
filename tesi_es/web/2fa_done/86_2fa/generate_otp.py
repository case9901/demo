import pyotp

secret = "JBSWY3DPEHPK3PXP"  # Questo è il segreto ottenuto dalla richiesta GET
totp = pyotp.TOTP(secret)
otp = totp.now()
print("Il tuo OTP è:", otp)
