FROM python:3.8-slim
WORKDIR /usr/src/app
COPY deployment/deploy_services.py ./
RUN pip install --no-cache-dir docker pydantic
CMD ["python", "./docker_sdk_deploy_services.py"]