import itertools
import string

def password_generator():
    for password in itertools.combinations(string.ascii_letters + string.digits, 1):
        yield password[0]

for password in password_generator():
    print(password)