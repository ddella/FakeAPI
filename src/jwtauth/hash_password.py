from passlib.hash import pbkdf2_sha256
print(f'password1={pbkdf2_sha256.hash("Password1")}')
print(f'password2={pbkdf2_sha256.hash("Password2")}')
print(f'password3={pbkdf2_sha256.hash("Password3")}')
print(f'password4={pbkdf2_sha256.hash("Password4")}')
print(f'password5={pbkdf2_sha256.hash("Password5")}')
print(f'password6={pbkdf2_sha256.hash("Password6")}')
