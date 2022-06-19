from django.conf import settings

__all__ = [
    'DEFAULTS',
    'app_settings',
]


DEFAULTS = {

    # Miscellaneous
    'DEFAULT_PERMISSION_DENIED_MESSAGE': 'Forbidden',


    # Login 
    'LOGIN_URL': '/login',
    'LOGIN_REDIRECT_URL': '/',


    # Logout 
    'LOGOUT_REDIRECT_URL': '/',

}


class AppSettings:

    user_settings: dict = getattr(settings, 'AUTHME', {})
    default_settings: dict = DEFAULTS

    def __getattr__(self, attr: str):
        if attr not in self.default_settings:
            raise AttributeError(f'Invalid setting: {attr}')
        try:
            value = self.user_settings[attr]
        except KeyError:
            value = self.default_settings[attr]
        return value


app_settings = AppSettings()
