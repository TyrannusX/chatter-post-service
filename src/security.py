import json
from typing import Annotated
from urllib.request import urlopen
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes
from jose import jwt
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

security = HTTPBearer()

async def verify_jwt(encoded: Annotated[HTTPAuthorizationCredentials, Depends(security)], scopes: SecurityScopes) -> str:
    try:
        jwks = get_jwks_json()
        rsa_key = get_rsa_key(jwks, encoded)        
        decoded_jwt = jwt.decode(encoded.credentials, rsa_key, algorithms=[os.getenv("ALGORITHM")], audience=os.getenv("API_AUDIENCE"))
        scope_found = validate_permissions(decoded_jwt, scopes.scopes[0])
        
        if not scope_found:
            raise HTTPException(status_code=403, detail="Unauthorized access to resource!")
        
        current_user = decoded_jwt["sub"]
        return current_user
    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=401, detail="Invalid token!")

def get_jwks_json():
    jwks_url = httpx.get(f'{os.getenv("AUTH0_DOMAIN")}/.well-known/jwks.json')
    jwks = json.loads(jwks_url.read())
    return jwks

def get_rsa_key(jwks, encoded):
    unverified_header = jwt.get_unverified_header(encoded.credentials)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    return rsa_key

def validate_permissions(decoded_jwt, required_scope):
    scope_found = False
    permissions = decoded_jwt["permissions"]
    for permission in permissions:
        if permission == required_scope:
            scope_found = True
            break
    return scope_found