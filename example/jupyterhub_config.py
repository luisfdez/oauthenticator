# Configuration file for Jupyter Hub
import os
import codecs

c = get_config()

c.JupyterHub.log_level = 10

c.JupyterHub.authenticator_class = 'oauthenticator.openshift.LocalOpenShiftOAuthenticator'
c.LocalOpenShiftOAuthenticator.create_system_users = True

with codecs.open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r', encoding='utf-8') as secret:
    c.OpenShiftOAuthenticator.client_secret = secret.read()

# put the JupyterHub cookie secret and state db
# in /var/run/jupyterhub
c.JupyterHub.cookie_secret_file = '/srv/jupyterhub/cookie_secret'
c.JupyterHub.db_url = '/srv/jupyterhub/jupyterhub.sqlite'

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.hub_ip = '0.0.0.0'

c.JupyterHub.port = 8000
# The spawned containers need to be able to talk to the hub through the proxy!
c.KubeSpawner.hub_connect_ip = os.environ['HUB_CONNECT_IP']

# Don't try to cleanup servers on exit - since in general for k8s, we want
# the hub to be able to restart without losing user containers
c.JupyterHub.cleanup_servers = os.environ['CLEANUP_SERVERS']

# First pulls can be really slow, so let's give it a big timeout
c.KubeSpawner.start_timeout = 60 * 5 
c.KubeSpawner.mem_limit = '100M'
c.KubeSpawner.mem_guarantee='100M'
c.KubeSpawner.cpu_limit = 0.5
c.KubeSpawner.cpu_guarantee = 0.5
