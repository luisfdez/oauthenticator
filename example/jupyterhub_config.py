# Configuration file for Jupyter Hub
import os

c = get_config()

c.JupyterHub.log_level = 10
c.JupyterHub.authenticator_class = 'oauthenticator.openshift.OpenShiftOAuthenticator'

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.hub_ip = '0.0.0.0'

# Don't try to cleanup servers on exit - since in general for k8s, we want
# the hub to be able to restart without losing user containers
c.JupyterHub.cleanup_servers = False

# First pulls can be really slow, so let's give it a big timeout
c.KubeSpawner.start_timeout = 60 * 5 

# Our simplest user image! Optimized to just... start, and be small!
c.KubeSpawner.singleuser_image_spec = 'yuvipanda/simple-singleuser:v1'

# The spawned containers need to be able to talk to the hub through the proxy!
c.KubeSpawner.hub_connect_ip = os.environ['HUB_CONNECT_IP']

c.KubeSpawner.mem_limit = '100Mi'
c.KubeSpawner.mem_guarantee='100Mi'
c.KubeSpawner.cpu_limit = 0.5
c.KubeSpawner.cpu_guarantee = 0.5

# Old class names
#c.JupyterHub.spawner_class = 'kubernetes_spawner.KubernetesSpawner'
#c.KubernetesSpawner.verify_ssl = False
#c.KubernetesSpawner.hub_ip_from_service = 'jupyterhub'
#c.KubernetesSpawner.container_image = 'danielfrg/jupyterhub-kube-ldap-nfs-singleuser:0.1'
#c.Spawner.default_url = '/lab'
#c.Spawner.notebook_dir = '/mnt/notebooks/%U'
#c.KubernetesSpawner.persistent_volume_claim_name = 'jupyterhub-volume'
#c.KubernetesSpawner.persistent_volume_claim_path = '/mnt'
