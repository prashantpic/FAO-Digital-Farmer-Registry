# -*- coding: utf-8 -*-
import jwt 
import datetime
import logging
from odoo import api, models, fields, SUPERUSER_ID
from odoo.exceptions import AccessDenied

_logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, env):
        self.env = env
        config_param = self.env['ir.config_parameter'].sudo()
        
        self._jwt_secret_key = config_param.get_param(
            'dfr_api.jwt_secret_key', 
            'default-super-secret-key-replace-me' # Fallback default, should be overridden
        )
        if self._jwt_secret_key == 'default-super-secret-key-replace-me' or \
           self._jwt_secret_key == '!!REPLACE_THIS_IN_PRODUCTION_WITH_A_STRONG_RANDOM_SECRET_KEY!!':
            _logger.warning(
                "CRITICAL SECURITY WARNING: Using default JWT secret key. "
                "This key MUST be changed in production via ir.config_parameter "
                "or environment variables for security."
            )
            
        self._jwt_algorithm = 'HS256' # Standard algorithm

        try:
            self._access_token_expiry_seconds = int(
                config_param.get_param('dfr_api.access_token_expiry_seconds', 3600) # 1 hour default
            )
        except ValueError:
            _logger.warning("Invalid 'dfr_api.access_token_expiry_seconds' in ir.config_parameter, using default 3600s.")
            self._access_token_expiry_seconds = 3600
        
        try:
            self._refresh_token_expiry_seconds = int(
                config_param.get_param('dfr_api.refresh_token_expiry_seconds', 86400 * 7) # 7 days default
            )
        except ValueError:
            _logger.warning("Invalid 'dfr_api.refresh_token_expiry_seconds' in ir.config_parameter, using default 7 days.")
            self._refresh_token_expiry_seconds = 86400 * 7

    def _generate_jwt_token(self, user_id, user_login, user_groups_xml_ids, expiry_seconds, token_type='access'):
        """Generates a JWT token for a given user ID."""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        payload = {
            'iat': now,
            'exp': now + datetime.timedelta(seconds=expiry_seconds),
            'sub': user_id,         # Subject (user ID)
            'login': user_login,    # User login
            'groups': user_groups_xml_ids, # List of group XML IDs
            'type': token_type,     # 'access' or 'refresh'
            # Add other claims as needed, e.g., company_id
            'iss': 'DFR API Gateway' # Issuer claim
        }
        return jwt.encode(payload, self._jwt_secret_key, algorithm=self._jwt_algorithm)

    def generate_jwt_tokens_for_user(self, user):
        """Generates access and refresh tokens for a user."""
        if not user or not hasattr(user, 'id') or not hasattr(user, 'login') or not hasattr(user, 'groups_id'):
            _logger.error("Invalid user object passed to generate_jwt_tokens_for_user.")
            return None, None, 0

        user_groups_xml_ids = [group.xml_id for group in user.groups_id if group.xml_id]

        access_token = self._generate_jwt_token(
            user.id, user.login, user_groups_xml_ids, self._access_token_expiry_seconds, 'access'
        )
        # Refresh token usually has fewer claims and is primarily used to get a new access token.
        # It might not need groups, or could have a specific 'refresh' scope/claim.
        refresh_token_groups = [] # Typically, refresh tokens don't carry extensive permissions like groups.
        refresh_token = self._generate_jwt_token(
            user.id, user.login, refresh_token_groups, self._refresh_token_expiry_seconds, 'refresh'
        )
        return access_token, refresh_token, self._access_token_expiry_seconds

    def validate_and_decode_jwt_token(self, token, token_type='access'):
        """Validates and decodes a JWT token. Returns payload or None."""
        try:
            # leeway accounts for clock skew between servers
            payload = jwt.decode(token, self._jwt_secret_key, algorithms=[self._jwt_algorithm], leeway=10) 
            
            if payload.get('type') != token_type:
                _logger.warning(f"Invalid token type. Expected '{token_type}', got '{payload.get('type')}' for token sub {payload.get('sub')}")
                return None
            
            # Additional checks can be added here (e.g., check against a token blacklist if implemented)
            return payload
        except jwt.ExpiredSignatureError:
            _logger.info(f"Token has expired for sub {jwt.decode(token, algorithms=[self._jwt_algorithm], options={'verify_signature': False}).get('sub', 'unknown') if token else 'unknown'}.")
            return None
        except jwt.InvalidTokenError as e:
            _logger.warning(f"Invalid token: {e}")
            return None
        except Exception as e:
            _logger.error(f"Unexpected error during token decoding: {e}")
            return None


    def authenticate_user_credentials(self, login, password):
        """Authenticates Odoo user credentials."""
        if not login or not password:
            _logger.warning("Attempt to authenticate with empty login or password.")
            return None
        try:
            # Odoo's _login method attempts to log in the user and returns the UID on success.
            # It handles password hashing and checking.
            # `{'interactive': False}` is important for non-UI logins.
            uid = self.env['res.users']._login(self.env.cr.dbname, login, password, {'interactive': False})
            if uid:
                user = self.env['res.users'].browse(uid)
                if user.exists() and user.active:
                    # audit_log_service.log_login_success(login, user.id)
                    return user
                else:
                    _logger.warning(f"Authentication successful for user {login} but user inactive or does not exist (UID: {uid}).")
                    # audit_log_service.log_login_failure(login, reason="User inactive or not found post-login")
                    return None
        except AccessDenied:
            _logger.info(f"Authentication failed for user {login}: Invalid credentials (AccessDenied).")
            # audit_log_service.log_login_failure(login, reason="Invalid credentials")
        except Exception as e:
            _logger.error(f"Error during credential authentication for {login}: {e}")
            # audit_log_service.log_login_failure(login, reason=f"Server error: {str(e)}")
        return None

    def get_user_from_token(self, env_for_user, token_string, token_type='access'):
        """Validates token and returns the Odoo user record using the provided environment."""
        payload = self.validate_and_decode_jwt_token(token_string, token_type)
        if payload and 'sub' in payload:
            user_id = payload['sub']
            try:
                # Use the environment passed, which should be correctly set up by the caller (e.g., request.env)
                user = env_for_user['res.users'].browse(user_id).exists() 
                if user and user.active: # Ensure user is active
                    # Potentially check if token is revoked (if such a mechanism exists)
                    return user
                elif user and not user.active:
                     _logger.warning(f"User ID {user_id} from token found but is inactive (Login: {user.login}).")
                else: # user is False (record does not exist)
                    _logger.warning(f"User ID {user_id} from token not found in the database.")

            except Exception as e:
                _logger.error(f"Error retrieving user {user_id} from token: {e}")
        return None