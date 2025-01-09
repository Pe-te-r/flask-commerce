from random import sample


def get_random_code():
    letters = "ABCDEFGHJKLMNOPQRSTUVWXYZ1234567890"
    code_str=''
    code = sample(letters,k=5)

    for i in code:
        code_str += i
    
    return code_str

def verify_random_code(saved,user):
    return saved == user