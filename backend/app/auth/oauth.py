from authlib.integrations.starlette_client import OAuth
from fastapi import HTTPException
import os

oauth = OAuth()

oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

oauth.register(
    name='apple',
    client_id=os.getenv('APPLE_CLIENT_ID'),
    client_secret=os.getenv('APPLE_CLIENT_SECRET'),
    authorize_url='https://appleid.apple.com/auth/authorize',
    access_token_url='https://appleid.apple.com/auth/token',
    client_kwargs={'scope': 'name email'}
)

async def get_user_info(provider: str, token: dict):
    if provider == 'google':
        client = oauth.google
        resp = await client.parse_id_token(token)
        return {
            'email': resp['email'],
            'name': resp['name'],
            'provider_id': resp['sub']
        }
    elif provider == 'apple':
        # Apple ID token parsing
        resp = token.get('id_token')
        if not resp:
            raise HTTPException(status_code=400, detail="Invalid Apple token")
        # Decode Apple JWT token here
        return {
            'email': resp.get('email'),
            'name': resp.get('name', 'Apple User'),
            'provider_id': resp.get('sub')
        }
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")