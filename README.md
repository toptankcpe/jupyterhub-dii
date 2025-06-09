
# JupyterHub ECS Spawner

A custom JupyterHub Spawner that dynamically launches dedicated EC2 instances in an ECS cluster and starts a Jupyter notebook server inside ECS tasks.

This project is intended for advanced deployments where each user gets their own isolated EC2 instance and Jupyter container environment, with support for spot instances, and S3-backed storage.

---

## Features

- Spawn JupyterHub users as **ECS tasks** on dedicated **EC2 instances**
- Supports **spot** or **on-demand** EC2 launch
- Supports **S3-backed** notebook storage via `S3ContentsManager`
- Supports **Inactive** notebook session via `idle-culler`

---

## Project Structure

```
├── jupyterhub_config.py           # JupyterHub configuration
├── jupyter-ecs-spawner/          # Custom ECS Spawner module
│   ├── __init__.py
│   ├── ecsspawner.py             # Main ECS Spawner logic
│   ├── instances.json            # Available EC2 instance types
│   ├── amis.json                 # AMI IDs per region
│   ├── regions.json              # Supported AWS regions
│   └── form_template.html        # Spawn form (dropdown UI)
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker image for JupyterHub
└── README.md
```

## Environment Variables

| Variable               | Description                                 |
|------------------------|---------------------------------------------|
| `DOCKER_IMAGE`         | Docker image to use in ECS task             |
| `ECS_CLUSTER`          | ECS cluster name                            |
| `SUBNET_ID`            | Subnet ID for EC2                           |
| `SECURITY_GROUP_ID`    | Comma-separated security groups             |
| `INSTANCE_ROLE_ARN`    | EC2 IAM role                                |
| `TASK_ROLE_ARN`        | IAM role for ECS task                       |
| `EXECUTION_ROLE_ARN`   | IAM role for ECS task execution             |
| `KEY_PAIR_NAME`        | (optional) EC2 SSH key pair                 |
| `S3_BUCKET`            | (optional) S3 bucket for notebook storage   |
| `S3_PREFIX`            | (optional) S3 path prefix                   |

---
