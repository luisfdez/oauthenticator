"""
Custom Authenticator to use OpenShift OAuth with JupyterHub
"""


import json
import os

from tornado.auth import OAuth2Mixin
from tornado import gen, web

from tornado.httputil import url_concat
from tornado.httpclient import HTTPRequest, AsyncHTTPClient

from jupyterhub.auth import LocalAuthenticator

from traitlets import Unicode

from .oauth2 import OAuthLoginHandler, OAuthenticator

OPENSHIFT_URL = os.environ.get('OPENSHIFT_URL') or 'https://localhost:8443'

class OpenShiftMixin(OAuth2Mixin):
    _OAUTH_AUTHORIZE_URL = "%s/oauth/authorize" % OPENSHIFT_URL
    _OAUTH_ACCESS_TOKEN_URL = "%s/oauth/token" % OPENSHIFT_URL


class OpenShiftLoginHandler(OAuthLoginHandler, OpenShiftMixin):
    pass


class OpenShiftOAuthenticator(OAuthenticator):

    login_service = "OpenShift"

    login_handler = OpenShiftLoginHandler

    @gen.coroutine
    def authenticate(self, handler, data=None):
        code = handler.get_argument("code", False)
        if not code:
            raise web.HTTPError(400, "oauth callback made without a token")

        # TODO: Configure the curl_httpclient for tornado
        http_client = AsyncHTTPClient()

        # Exchange the OAuth code for a OpenShift Access Token
        #
        # See: https://docs.openshift.org/latest/architecture/additional_concepts/authentication.html#api-authentication

        # OpenShift specifies a POST request yet requires URL parameters
        params = dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type="authorization_code",
            code=code
        )

        url = url_concat("%s/oauth/token" % OPENSHIFT_URL, params)

        req = HTTPRequest(url,
                          method="POST",
                          validate_cert=False,
                          headers={"Accept": "application/json"},
                          body='' # Body is required for a POST...
                          )

        resp = yield http_client.fetch(req)

        resp_json = json.loads(resp.body.decode('utf8', 'replace'))

        access_token = resp_json['access_token']

        # Determine who the logged in user is
        headers={"Accept": "application/json",
                 "User-Agent": "JupyterHub",
                 "Authorization": "Bearer {}".format(access_token)
        }

        req = HTTPRequest("%s/oapi/v1/users/~" % OPENSHIFT_URL,
                          method="GET",
                          validate_cert=False,
                          headers=headers)

        resp = yield http_client.fetch(req)
        resp_json = json.loads(resp.body.decode('utf8', 'replace'))

        return resp_json["metadata"]["name"]
