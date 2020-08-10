import hashlib
from anna.settings import SECRET_KEY

def make_password(password:str):
    m = hashlib.md5((password+SECRET_KEY).encode())
    return m.hexdigest()

print(make_password("123"))