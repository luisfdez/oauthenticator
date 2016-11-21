# Configuration file for Jupyter Hub

c = get_config()

c.JupyterHub.log_level = 10
c.JupyterHub.authenticator_class = 'oauthenticator.openshift.OpenShiftOAuthenticator'
