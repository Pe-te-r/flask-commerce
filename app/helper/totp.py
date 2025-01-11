import pyotp

def get_otp():
    code = pyotp.TOTP(pyotp.random_base32()) 
    return code.secret

def verify_otp(secret,code):
    try:
        totp = pyotp.TOTP(str(secret))
        return totp.verify(code)
    except Exception:
        return False
