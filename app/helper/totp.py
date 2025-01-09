import pyotp

def get_otp():
    code = pyotp.TOTP(pyotp.random_base32()) 
    return code.secret

def verify_otp():
    pass