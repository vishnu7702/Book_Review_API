import datetime
import jwt
from fastapi import Request,HTTPException
from connection import token_time,secret_key



# Function to add expiry Date To The Token


def adding_expiry_jwt(data: dict):
    expiry = datetime.datetime.utcnow()+datetime.timedelta(minutes=int(token_time))
    data.update({"exp": expiry})
    encoded_jwt = jwt.encode(data,secret_key, "HS256")
    return encoded_jwt


# Function To Remove Bearer From JWT
def remove_bearer(result: str):
    try:
        return result.replace("Bearer ", "")
    except Exception as e:
        return None

# Function To Get Headers
def get_headers(request: Request):
    headers_dict = dict(request.headers)
    if "authorization" not in headers_dict:
        return False
    my_jwt = headers_dict["authorization"]
    if not my_jwt.startswith("Bearer "):
        return False
    final_jwt = remove_bearer(my_jwt)
    try:
        result = jwt.decode(final_jwt, "secret", "HS256")
        return result["user_name"]
    except:
        raise HTTPException(status_code=401, detail="Token Expired")
    
