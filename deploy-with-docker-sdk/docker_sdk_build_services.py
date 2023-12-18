import docker
from pydantic import BaseModel

class ServiceConfig(BaseModel):
    name: str
    dockerfile_path: str
    docker_image: str
    registry: str

def build_and_push_image(service_config: ServiceConfig):
    print(f"Building Docker image for {service_config.name}")
    image, build_log = client.images.build(
        path=service_config.dockerfile_path, 
        tag=f"{service_config.registry}/{service_config.docker_image}",
        rm=True
    )
    for line in build_log:
        if 'stream' in line:
            print(line['stream'].strip())

    print(f"Pushing {service_config.name} image to registry")
    for line in client.images.push(service_config.docker_image, stream=True, decode=True):
        if 'status' in line:
            print(line['status'])

client = docker.from_env()

flask_config = ServiceConfig(
    name="flaskapp",
    dockerfile_path="../src/flask/",
    docker_image="flaskapp-events-demo",
    registry="cdaprod"
)

minio_config = ServiceConfig(
    name="minio",
    dockerfile_path="../src/minio/",
    docker_image="minio-events-demo",
    registry="cdaprod"
)

if __name__ == "__main__":
    for config in [flask_config, minio_config]:
        build_and_push_image(config)
