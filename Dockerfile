# Use the official JupyterHub base image
FROM jupyterhub/jupyterhub:latest

# Install additional JupyterHub extensions (native authenticator & idle culler)
RUN pip install --no-cache-dir jupyterhub-nativeauthenticator jupyterhub-idle-culler

# Create directory for JupyterHub configuration and spawner code
RUN mkdir -p /srv/jupyterhub

# Copy the custom ECS Spawner source code into the container
COPY jupyter-ecs-spawner /srv/jupyter-ecs-spawner

# Install dependencies from requirements.txt (for the spawner)
RUN pip install -r /srv/jupyter-ecs-spawner/requirements.txt

# Install the ECS Spawner package itself
RUN pip install /srv/jupyter-ecs-spawner

# Copy the JupyterHub configuration file into the container
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

# Expose the default JupyterHub port
EXPOSE 8000

# Start JupyterHub using the specified configuration file
CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
