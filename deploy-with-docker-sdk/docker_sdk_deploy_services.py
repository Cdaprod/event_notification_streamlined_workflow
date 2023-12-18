import docker
from pydantic import BaseModel

# Define the ServiceConfig model
class ServiceConfig(BaseModel):
    name: str
    docker_image: str
    ports: dict
    environment: dict = {}
    command: str = None

# Initialize Docker client
client = docker.from_env()

# Function to deploy a service
def deploy_service(service_config: ServiceConfig):
    print(f"Deploying {service_config.name}")
    container = client.containers.run(
        image=service_config.docker_image,
        detach=True,
        ports=service_config.ports,
        environment=service_config.environment,
        name=service_config.name,
        command=service_config.command
    )
    return container

##### Service configurations #####
flask_config = ServiceConfig(
    name="flaskapp",
    docker_image="flaskapp.dockerfile",  # Replace with your Flask Docker image
    ports={'5000/tcp': 5000},
    # Pass in any environment variables here.
    environment={"FLASK_ENV": "development"}
)

# MinIO Container
minio_config = ServiceConfig(
    name="minio",
    docker_image="minio/minio",
    ports={'9000/tcp': 9000},
    environment={
        "MINIO_ROOT_USER": "minio",
        "MINIO_ROOT_PASSWORD": "minio123",
        "MINIO_NOTIFY_WEBHOOK_ENABLE": "on",
        "MINIO_NOTIFY_WEBHOOK_ENDPOINT": "http://example-webhook-endpoint.com",
        # Add other environment variables as needed
    },
    command=(
        'server /data && '
        'mc alias set myminio http://minio:9000 minio minio123 && '
        'mc event add myminio/mybucket arn:minio:sqs::1:webhook --event put,get,delete'
    )
)

# Postgres Container
postgres_config = ServiceConfig(
    name="postgres",
    docker_image="postgres",
    ports={'5432/tcp': 5432},
    # Pass your credentials as environment variables here.
    environment={"POSTGRES_USER":"myuser", "POSTGRES_PASSWORD": "mypassword"} 
)

# Redis Container is a simpler service configuration not requiring auth credentials.
redis_config = ServiceConfig(
    name="redis",
    docker_image="redis",
    ports={'6379/tcp': 6379}
)

##### Deploy all services ###
if __name__ == "__main__":
    deploy_service(flask_config)
    deploy_service(minio_config)
    deploy_service(postgres_config)
    deploy_service(redis_config)