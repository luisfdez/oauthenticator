# Configuration file for Jupyter Hub

c = get_config()

c.JupyterHub.log_level = 10
c.JupyterHub.authenticator_class = 'oauthenticator.openshift.OpenShiftOAuthenticator'

c.JupyterHub.spawner_class = 'kubernetes_spawner.KubernetesSpawner'
c.KubernetesSpawner.verify_ssl = False
#c.KubernetesSpawner.hub_ip_from_service = 'jupyterhub'
#c.KubernetesSpawner.container_image = 'danielfrg/jupyterhub-kube-ldap-nfs-singleuser:0.1'
#c.Spawner.default_url = '/lab'
#c.Spawner.notebook_dir = '/mnt/notebooks/%U'
#c.KubernetesSpawner.persistent_volume_claim_name = 'jupyterhub-volume'
#c.KubernetesSpawner.persistent_volume_claim_path = '/mnt'
