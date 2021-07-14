import os
import json
from flask import request, _request_ctx_stack, abort, redirect, session
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from dotenv import load_dotenv

#----------------------------------------------------------------------------#
# Configure Auth0 constants
#----------------------------------------------------------------------------#

load_dotenv()

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = ['RS256']
API_AUDIENCE=os.environ['API_AUDIENCE']

#----------------------------------------------------------------------------#
# Implement JWT authorization
#----------------------------------------------------------------------------#

class AuthError(Exception):
    '''
    AuthError Exception
    A standardized way to communicate auth failure modes
    '''
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
  '''
  Gets request header, raising AuthError if no header is present
  Splits bearer and token raising AuthError if header is malformed
  Returns the token part of the header if successful
  '''
  auth_header = request.headers.get('Authorization', None)
  if not auth_header:
      raise AuthError({
          'code': 'authorization_header_missing',
          'description': 'Authorization header is missing.'
      }, 401)

  header_parts = auth_header.split()

  if len(header_parts) != 2:
    raise AuthError({
    'code': 'invalid_header',
    'description': 'Header invalid'
    }, 401)
  elif header_parts[0].lower() != 'bearer':
    raise AuthError({
    'code': 'invalid_header',
    'description': 'Authorization header must start with "Bearer".'
    }, 401)

  return header_parts[1]

def check_permissions(permission, payload):
  '''@INPUTS
    permission: string permission (i.e. 'get:movies')
    payload: decoded JWT payload

    Response:
        Raises an AuthError if the permissions are not included in the payload
        Raises an AuthError if the requested permission string is not in the payload permissions array
        Returns True if otherwise
  '''
  if 'permissions' not in payload:
    raise AuthError({
        'code': 'invalid_claims',
        'description': 'Permissions not included in JWT.'
    }, 400)

  if permission not in payload['permissions']:
      raise AuthError({
          'code': 'unauthorized',
          'description': 'Permission not found.'
      }, 403)
  return True

def verify_decode_jwt(token):
  '''@INPUTS
    token: a JSON web token (JWT) string
  
    Request:
        Checks that the Auth0 token has the key id (kid)
        Verifis the token using Auth0 /.well-known/jwks.json
        Decodes the payload from the token
        Validates the claims

    Response:
        Returns the decoded payload
        If not valid, raises AuthError exception
  '''

  # GET THE PUBLIC KEY FROM AUTH0
  jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
  jwks = json.loads(jsonurl.read())
    
  # GET THE DATA IN THE HEADER
  unverified_header = jwt.get_unverified_header(token)

  # CHOOSE OUR KEY
  rsa_key = {}
  if 'kid' not in unverified_header:
      raise AuthError({
          'code': 'invalid_header',
          'description': 'Authorization malformed.'
      }, 401)

  for key in jwks['keys']:
    if key['kid'] == unverified_header['kid']:
      rsa_key = {
          'kty': key['kty'],
          'kid': key['kid'],
          'use': key['use'],
          'n': key['n'],
          'e': key['e']
      }
  if rsa_key:
    try:
      # USE THE KEY TO VALIDATE THE JWT
      payload = jwt.decode(
        token,
        rsa_key,
        algorithms=ALGORITHMS,
        audience=API_AUDIENCE,
        issuer='https://' + AUTH0_DOMAIN + '/'
      )

      return payload

    except jwt.ExpiredSignatureError:
      raise AuthError({
        'code': 'token_expired',
        'description': 'Token expired.'
      }, 401)

    except jwt.JWTClaimsError:
      raise AuthError({
        'code': 'invalid_claims',
        'description': 'Incorrect claims. Please, check the audience and issuer.'
        }, 401)
    except Exception:
      raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to parse authentication token.'
      }, 400)
  raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
        }, 400)

def requires_auth(permission=''):
  '''@INPUTS
    permission: string permission (i.e. get:movies)

    Request:
        The get_token_auth_header method gets the token
        The verify_decode_jwt method decodes the JWT
        The check_permissions method validates the claims and checks the requested permission

    Response:
        Returns the decorator which passes the decoded payload to the decorated method
  '''
  def requires_auth_decorator(f):
      @wraps(f)
      def wrapper(*args, **kwargs):
        try:
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
        except AuthError as err:
            abort(401, err.error)

        return f(payload, *args, **kwargs)

      return wrapper
  return requires_auth_decorator

def requires_signed_in(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'jwt_token' not in session:
            return redirect('/')
        return f(*args, **kwargs)

    return decorated