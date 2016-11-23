import json

from flask import url_for, request, redirect
from rauth import OAuth2Service

from ... import app


class OAuthSignIn(object):
    """Sign in using OAuth."""

    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['CLIENT_ID']
        self.consumer_secret = credentials['CLIENT_SECRET']

    def authorize(self):
        """Authorize the user."""
        pass

    def callback(self):
        """Create a callback."""
        pass

    def get_callback_url(self):
        """Get a callback."""
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        """Return the provider."""

        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class BeamSignIn(OAuthSignIn):
    """Sign in for Beam."""

    def __init__(self):
        super(BeamSignIn, self).__init__("beam")
        self.service = OAuth2Service(
            name="beam",
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url="https://beam.pro/oauth/authorize",
            access_token_url="https://beam.pro/api/v1/oauth/token"
        )

    def authorize(self):
        """Authorize a user."""
        params = {
            "redirect_uri": self.get_callback_url(),
            "response_type": "code",
            "scope": "user:details:self chat:chat chat:connect "
                     "chat:remove_message chat:bypass_slowchat "
                     "chat:bypass_links"
        }
        return redirect(self.service.get_authorize_url(**params))

    def callback(self):
        """Create a callback."""
        if "code" not in request.args:
            return None, None, None

        oauth_session = self.service.get_auth_session(
            data={
                "code": request.args["code"],
                "grant_type": "authorization_code",
                "redirect_uri": self.get_callback_url(),
                "client_id": self.consumer_id,
                "client_secret": self.consumer_secret
            },
            decoder=lambda b: json.loads(b.decode('utf-8'))
        )

        return oauth_session.get(
            "https://beam.pro/api/v1/users/current").json()
