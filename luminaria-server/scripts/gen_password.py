import bcrypt


def gen_hash(password):
    password = password.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed


if __name__ == '__main__':
    pw = input('Password: ')
    print(gen_hash(pw))
