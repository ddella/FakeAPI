import jwt
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

JWT_SECRET = "my-secret"
JWT_ALGO = "HS256"
JWT_EXPIRATION = 10


# Encode a JWT with a subject claim and an expiration time
expiration = datetime.now(tz=ZoneInfo("America/Montreal")) + timedelta(seconds=JWT_EXPIRATION)
payload = {"sub": "username", "role": "admin", "exp": expiration}
# token is of type 'str'
token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
print(f'JWT Token={token}')

# Decode a JWT and print the subject claim
try:
    decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    # print(f'Decoded token:: sub={decoded["sub"]} - exp={decoded["exp"]}')  # "admin"
    before_encoded = int(expiration.strftime("%s"))
    after_encoded = int(decoded["exp"])
    print(f'Before encoding={before_encoded} - {datetime.fromtimestamp(before_encoded).strftime("%c")}')
    print(f'Decoded        ={after_encoded} - {datetime.fromtimestamp(after_encoded).strftime("%c")}')
except jwt.ExpiredSignatureError as e:
    print(f'Error in decode: {e}')

# Verify a JWT signature
try:
    jwt.decode(token, JWT_SECRET, verify=True, algorithms=[JWT_ALGO])
    print(f'Token is VALID')
except jwt.ExpiredSignatureError as e:
    print(f'Expired: {e}')
except jwt.InvalidSignatureError as e:
    print(f'Invalid: {e}')
