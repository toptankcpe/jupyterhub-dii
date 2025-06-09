# Import the ECS Spawner and Native Authenticator
from ecsspawner import ECSSpawner
import nativeauthenticator
import os

# Parse security group list from environment variable (comma-separated)
sgs = os.environ.get("SECURITY_GROUP_ID", "sg-0ad307929306dbf9b").split(",")

# Get JupyterHub configuration object
c = get_config()

# Use ECS Spawner for spawning single-user servers
c.JupyterHub.spawner_class = ECSSpawner

# ECS and EC2 configuration from environment variables (with defaults)
c.ECSSpawner.ecs_cluster = os.environ.get("ECS_CLUSTER", "spark-cluster-ec2")
c.ECSSpawner.default_docker_image = os.environ.get("DOCKER_IMAGE", "096020056038.dkr.ecr.ap-southeast-7.amazonaws.com/bdi-dii/jupyter-image:latest")
c.ECSSpawner.instance_role_arn = os.environ.get("INSTANCE_ROLE_ARN", "arn:aws:iam::096020056038:instance-profile/ecsInstanceRole")
c.ECSSpawner.task_role_arn = os.environ.get("TASK_ROLE_ARN", "arn:aws:iam::096020056038:role/ecsTaskExecutionRole")
c.ECSSpawner.execution_role_arn = os.environ.get("EXECUTION_ROLE_ARN", "arn:aws:iam::096020056038:role/ecsTaskExecutionRole")
c.ECSSpawner.subnet_id = os.environ.get("SUBNET_ID", "subnet-0377381f728c7c962")
c.ECSSpawner.security_groups_ids = [sg.strip() for sg in sgs if sg.strip()]
c.ECSSpawner.key_pair_name = os.environ.get("KEY_PAIR_NAME", "key-pantawat")
c.ECSSpawner.ec2_ami = os.environ.get("EC2_AMI", "ami-00744bf9d3518c038")
c.ECSSpawner.use_public_ip = False

# Custom environment variables passed to each Jupyter server
c.ECSSpawner.custom_env = {
    "JUPYTER_ENABLE_LAB": "yes",
    "S3_BUCKET": os.environ.get("S3_BUCKET", "dii-dev"),
    "S3_PREFIX": os.environ.get("S3_PREFIX", "notebooks"),
    "AWS_REGION": os.environ.get("AWS_REGION", "ap-southeast-7"),
    "S3_ENDPOINT_URL": os.environ.get("S3_ENDPOINT_URL", "https://s3.ap-southeast-7.amazonaws.com")
}

# Timeout settings for spawning and HTTP requests
c.Spawner.http_timeout = 900
c.Spawner.start_timeout = 900

# JupyterHub binding configuration
c.JupyterHub.hub_ip = '0.0.0.0'  # Bind to all interfaces inside the container
c.JupyterHub.hub_port = 8081     # Internal port used by hub
c.JupyterHub.hub_connect_ip = os.environ.get("HUB_CONNECT_IP", "10.0.3.19")  # External IP used by spawned servers to reach hub

# Set Native Authenticator as the authentication mechanism
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
c.JupyterHub.db_url = 'sqlite:////srv/jupyterhub/jupyterhub.sqlite'

# Path to custom signup/login templates from nativeauthenticator
c.JupyterHub.template_paths = [f"{os.path.dirname(nativeauthenticator.__file__)}/templates/"]

# Admin users who can manage the JupyterHub UI
c.Authenticator.admin_users = {'pantawat.pr', 'chayasin.sa', 'bhudith.as', 'kasidit.ma', 'titirat.bo'}
c.Authenticator.allow_all = True  # Allow all known users to log in
c.NativeAuthenticator.open_signup = False  # Disable auto authorize signup requests

# Register idle-culler service to shut down idle notebooks
c.JupyterHub.services = [
    {
        'name': 'idle-culler',
        'admin': True,
        'command': 'python3 -m jupyterhub_idle_culler --timeout=3600'.split(),
    }
]

# Set logging level to DEBUG for detailed logs
c.Application.log_level = 'DEBUG'
